#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from PyQt5 import QtGui, QtCore, QtWidgets
import pyqtgraph as pg
import pyqtgraph.exporters
import numpy as np
from pyqtgraph.Point import Point
from functools import partial

import img_rc
from model.handle_config import ConfigHandler
from model.handle_theme import ThemeHandler
from controller.widgets.box_item import BoxItem


class PlotToolBar(QtWidgets.QToolBar):
    def __init__(self, parent=None):
        super(PlotToolBar, self).__init__(parent)

        self.home = QtWidgets.QAction(parent)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/resources/img/icons/home.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.home.setIcon(icon)

        self.export = QtWidgets.QAction(parent)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/resources/img/icons/save_plot.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.export.setIcon(icon)

        self.addAction(self.home)
        self.addAction(self.export)

        self.retranslateUi()

    def retranslateUi(self):
        self.home.setText('Home')
        self.export.setText('Save as image')

        self.home.setStatusTip('Reset original view.')
        self.export.setStatusTip('Save the figure as image.')

class PlotWidget(pg.GraphicsView):
    signal_change = QtCore.pyqtSignal(float, float)
    background_change = QtCore.pyqtSignal(float, float)

    def __init__(self, parent=None):
        super(PlotWidget, self).__init__(parent)

        self.config_handler = ConfigHandler()
        self.theme_handler = ThemeHandler()

        self.signal_plot = None
        self.background_plot = None
        self.x_values = []
        self.y_values = []
        self.main_plot_column = 1

        path = QtGui.QPainterPath()
        path.addEllipse(
            QtCore.QRectF(-0.25, -0.25, 0.5, 0.5)
        )
        pg.graphicsItems.ScatterPlotItem.Symbols['h'] = path

        self.main_layout = pg.GraphicsLayout()
        self.setCentralItem(self.main_layout)

        self.position_label = pg.LabelItem(justify='right')
        bi = BoxItem(
            (300, 30),
            (-4, -4)
        )
        bi.setParentItem(self.main_layout)
        bi.addItem(self.position_label)

        self.vertical_axis_label = pg.LabelItem(angle=-90)
        self.main_layout.addItem(
            self.vertical_axis_label,
            col=0,
            row=0
        )

        self.initMainPlot()
        self.initSignalPlot()
        self.initBackgrounPlot()

    def initMainPlot(self):
        if self.getConfiguration('signal_active'):
            self.main_plot_column = 2
        self.main_plot = self.main_layout.addPlot(
            col=self.main_plot_column,
            row=0
        )
        self.main_plot.scene().sigMouseMoved.connect(
            partial(self.mouseMoved, plot=self.main_plot)
        )
        self.main_plot.showGrid(True, True, 0.4)
        self.main_plot.setMenuEnabled(False)

        self.horizontal_axis_label = pg.LabelItem()
        self.main_layout.addItem(
            self.horizontal_axis_label,
            col=1,
            row=1,
            colspan=self.main_plot_column + 1
        )

    def initSignalPlot(self):
        if self.getConfiguration('signal_active'):
            self.signal_plot = self.main_layout.addPlot(
                col=1,
                row=0
            )
            self.signal_plot.setYLink(self.main_plot.getViewBox())
            self.signal_plot.scene().sigMouseMoved.connect(
                partial(self.mouseMoved, plot=self.signal_plot)
            )
            self.signal_plot.showGrid(True, True, 0.4)
            self.signal_plot.setMenuEnabled(False)
            self.signal_area = pg.LinearRegionItem(bounds=(0, 0))
            self.signal_area.setZValue(10)
            self.main_plot.addItem(self.signal_area, ignoreBounds=True)
            self.signal_area.sigRegionChangeFinished.connect(
                self.updateSignalPlot)

            self.main_layout.layout.setColumnFixedWidth(1, 240)
            self.main_layout.layout.setColumnMaximumWidth(1, 240)
            self.main_layout.layout.setColumnMinimumWidth(1, 240)
            self.main_layout.layout.setColumnSpacing(1, 30)

    def initBackgrounPlot(self):
        if self.getConfiguration('background_active'):
            self.background_plot = self.main_layout.addPlot(
                col=self.main_plot_column + 1,
                row=0
            )
            self.background_plot.setYLink(self.main_plot.getViewBox())
            self.background_plot.scene().sigMouseMoved.connect(
                partial(self.mouseMoved, plot=self.background_plot)
            )
            self.background_plot.showGrid(True, True, 0.4)
            self.background_plot.setMenuEnabled(False)
            self.background_area = pg.LinearRegionItem(bounds=(1, 1))
            self.background_area.setZValue(10)
            self.main_plot.addItem(self.background_area, ignoreBounds=True)
            self.background_area.sigRegionChangeFinished.connect(
                self.updateBackgroundPlot)

            self.main_layout.layout.setColumnFixedWidth(
                self.main_plot_column + 1, 200)
            self.main_layout.layout.setColumnMaximumWidth(
                self.main_plot_column + 1, 200)
            self.main_layout.layout.setColumnMinimumWidth(
                self.main_plot_column + 1, 200)
            self.main_layout.layout.setColumnSpacing(self.main_plot_column, 30)

    def updateSignalPlot(self, force=False):
        if self.x_values:
            self.signal_area.setZValue(10)
            min_x, max_x = self.signal_area.getRegion()
            if self.getConfiguration('horizontal_scale') == 'log':
                min_x, max_x = round(10 ** min_x), round(10 ** max_x)
            elif self.getConfiguration('horizontal_scale') == 'ln':
                min_x, max_x = round(np.e ** min_x), round(np.e ** max_x)

            positions = tuple(np.where(np.logical_and(np.array(self.x_values)>=min_x, np.array(self.x_values)<=max_x))[0])
            if positions:
                current_xdata = self.x_values[positions[0]: positions[-1] + 1]
                current_ydata = self.y_values[positions[0]: positions[-1] + 1]
                self.signal_change.emit(float(min(current_xdata)), float(max(current_xdata)))
            else:
                current_xdata = []
                current_ydata = []

            if not force:
                data = self.signal_plot.listDataItems()
                if data:
                    xdata, ydata = data[0].getData()
                    if tuple(xdata) == tuple(current_xdata):
                        return
            self.updatePlot(current_xdata, current_ydata, self.signal_plot)

    def updateBackgroundPlot(self, force=False):
        if self.x_values:
            self.background_area.setZValue(10)
            min_x, max_x = self.background_area.getRegion()

            if self.getConfiguration('horizontal_scale') == 'log':
                min_x, max_x = round(10 ** min_x), round(10 ** max_x)
            elif self.getConfiguration('horizontal_scale') == 'ln':
                min_x, max_x = round(np.e ** min_x), round(np.e ** max_x)

            positions = tuple(np.where(np.logical_and(np.array(self.x_values) >= min_x, np.array(self.x_values) <= max_x))[0])
            if positions:
                current_xdata = self.x_values[positions[0]: positions[-1] + 1]
                current_ydata = self.y_values[positions[0]: positions[-1] + 1]
                self.background_change.emit(float(min(current_xdata)), float(max(current_xdata)))
            else:
                current_xdata = []
                current_ydata = []

            if not force:
                data = self.background_plot.listDataItems()
                if data:
                    xdata, ydata = data[0].getData()
                    if tuple(xdata) == tuple(current_xdata):
                        return
            self.updatePlot(current_xdata, current_ydata, self.background_plot)

    def updatePlot(self, x_values, y_values, plot=None, ls=0, hs=0,
                   lb=0, hb=0, default=True):
        color = self.theme_handler.skin_keys['plot_color']
        force = False

        if plot is None:
            plot = self.main_plot
            force = self.updetAxisScales()
            self.x_values = x_values
            self.y_values = y_values
        else:
            if plot is self.signal_plot:
                color = self.theme_handler.skin_keys['plot_signal_area_color']
            elif plot is self.background_plot:
                color = self.theme_handler.skin_keys['plot_background_area_color']

        if self.getConfiguration('vertical_scale') == 'log':
            y_values = tuple(np.log10(y_values))
        elif self.getConfiguration('vertical_scale') == 'ln':
            y_values = tuple(np.log(y_values))

        if self.getConfiguration('horizontal_scale') == 'log':
            x_values = tuple(np.log10(x_values))
        elif self.getConfiguration('horizontal_scale') == 'ln':
            x_values = tuple(np.log(x_values))

        if plot.listDataItems():
            plot.listDataItems()[0].setData(
                x_values,
                y_values
            )
        else:
            plot.plot(
                x_values,
                y_values,
                symbol='h',
                symbolBrush=0.5,
                pen=color,
                symbolPen=color,
            )

        if plot is self.main_plot:
            if self.getConfiguration('signal_active'):
                if x_values:
                    self.signal_area.setBounds((x_values[0], x_values[-1]))
                    if default:
                        low_signal = ls
                        high_signal = hs
                        if low_signal == 0 and high_signal == 0:
                            low_signal = self.x_values[0]
                            high_signal = self.x_values[int(self.getConfiguration('high_signal', 'GENREP') - 1)]
                        else:
                            if low_signal < self.x_values[0]:
                                low_signal = self.x_values[0]
                        high_signal = self.x_values[int(high_signal) - 1]
                    else:
                        low_signal = self.x_values[tuple(self.x_values).index(ls)]
                        high_signal = self.x_values[tuple(self.x_values).index(hs)]

                    if self.getConfiguration('horizontal_scale') == 'log':
                        low_signal, high_signal = tuple(np.log10([low_signal, high_signal]))
                    elif self.getConfiguration('horizontal_scale') == 'ln':
                        low_signal, high_signal = tuple(np.log([low_signal, high_signal]))
                else:
                    low_signal = high_signal = 0

                self.signal_area.setRegion((
                    low_signal, high_signal
                ))
                self.updateSignalPlot(force)

            if self.getConfiguration('background_active'):
                if x_values:
                    self.background_area.setBounds((x_values[0], x_values[-1]))
                    if default:
                        low_background = lb
                        high_background = hb
                        if low_background == 0 and high_background == 0:
                            low_background = self.x_values[int(self.getConfiguration('low_background', 'GENREP') - 1)]
                            high_background = self.x_values[-1]
                        else:
                            if low_background == 0:
                                low_background = self.x_values[-1]
                            else:
                                low_background = self.x_values[int(low_background) - 1]
                            if high_background == 0:
                                high_background = self.x_values[-1]
                            else:
                                high_background = self.x_values[int(high_background)]
                    else:
                        low_background = self.x_values[tuple(self.x_values).index(lb)]
                        high_background = self.x_values[tuple(self.x_values).index(hb)]

                    if self.getConfiguration('horizontal_scale') == 'log':
                        low_background, high_background = tuple(np.log10([low_background, high_background]))
                    elif self.getConfiguration('horizontal_scale') == 'ln':
                        low_background, high_background = tuple(np.log([low_background, high_background]))
                else:
                    low_background = high_background = 0
                self.background_area.setRegion((
                    low_background, high_background
                ))
                self.updateBackgroundPlot(force)

            self.home()

    def updetAxisScales(self):
        force = self.main_plot.getAxis('bottom').scale_type != self.getConfiguration('horizontal_scale') or \
                self.main_plot.getAxis('left').scale_type != self.getConfiguration('vertical_scale')

        if self.getConfiguration('signal_active'):
            self.signal_plot.getAxis('top').scale_type = self.getConfiguration('horizontal_scale')
            self.signal_plot.getAxis('bottom').scale_type = self.getConfiguration('horizontal_scale')
            self.signal_plot.getAxis('left').scale_type = self.getConfiguration('vertical_scale')
            self.signal_plot.getAxis('right').scale_type = self.getConfiguration('vertical_scale')

        self.main_plot.getAxis('top').scale_type = self.getConfiguration('horizontal_scale')
        self.main_plot.getAxis('bottom').scale_type = self.getConfiguration('horizontal_scale')
        self.main_plot.getAxis('left').scale_type = self.getConfiguration('vertical_scale')
        self.main_plot.getAxis('right').scale_type = self.getConfiguration('vertical_scale')

        if self.getConfiguration('background_active'):
            self.background_plot.getAxis('top').scale_type = self.getConfiguration('horizontal_scale')
            self.background_plot.getAxis('bottom').scale_type = self.getConfiguration('horizontal_scale')
            self.background_plot.getAxis('left').scale_type = self.getConfiguration('vertical_scale')
            self.background_plot.getAxis('right').scale_type = self.getConfiguration('vertical_scale')

        return force

    def mouseMoved(self, pos, plot):
        if plot.sceneBoundingRect().contains(pos):
            data = plot.listDataItems()
            if data:
                mousePoint = plot.vb.mapSceneToView(pos)

                if self.getConfiguration('horizontal_scale') == 'lineal':
                    xpoint = round(mousePoint.x(), 0)
                elif self.getConfiguration('horizontal_scale') == 'log':
                    xpoint = round(10 ** mousePoint.x(), 0)
                elif self.getConfiguration('horizontal_scale') == 'ln':
                    xpoint = round(np.e**mousePoint.x(), 0)

                if self.getConfiguration('vertical_scale') == 'lineal':
                    ypoint = round(mousePoint.y(), 0)
                elif self.getConfiguration('vertical_scale') == 'log':
                    ypoint = round(10 ** mousePoint.y(), 0)
                elif self.getConfiguration('vertical_scale') == 'ln':
                    ypoint = round(np.e**mousePoint.y(), 0)

                label = ("<span style='font-size: 10pt; color:grey'>{0}: <span style='color: "
                         "{1}'>x={2} ({3})</span>, <span style='color: {1}'>y={4} ({5})</span></span>")
                color = "red"

                if xpoint in self.x_values:
                    index = tuple(self.x_values).index(xpoint)
                    if ypoint == self.y_values[index]:
                        color = "green"

                if self.getConfiguration('horizontal_scale') == 'log':
                    real_x = "%0.1g" % xpoint
                elif self.getConfiguration('horizontal_scale') == 'ln':
                    real_x = "%0.1g" % xpoint
                else:
                    real_x = round(mousePoint.x(), 2)

                if self.getConfiguration('vertical_scale') == 'log':
                    real_y = "%0.1g" % ypoint
                elif self.getConfiguration('vertical_scale') == 'ln':
                    real_y = "%0.1g" % ypoint
                else:
                    real_y = round(mousePoint.y(), 2)

                self.position_label.setText(
                    label.format(
                        plot.titleLabel.text,
                        color,
                        real_x,
                        xpoint,
                        real_y,
                        ypoint
                    )
                )

    def home(self):
        if self.getConfiguration('signal_active'):
            self.signal_plot.getViewBox().autoRange()
            self.signal_plot.getViewBox().enableAutoRange(
                self.signal_plot.getViewBox().XAxis)
        if self.getConfiguration('background_active'):
            self.background_plot.getViewBox().autoRange()
            self.background_plot.getViewBox().enableAutoRange(
                self.background_plot.getViewBox().XAxis)
        self.main_plot.getViewBox().autoRange()

        if self.x_values:
            horizontal_minimun = self.getConfiguration('horizontal_minimun')
            horizontal_maximun = self.getConfiguration('horizontal_maximun')
            vertical_minimun = self.getConfiguration('vertical_minimun')
            vertical_maximun = self.getConfiguration('vertical_maximun')

            if self.getConfiguration('horizontal_scale') == 'log':
                if horizontal_minimun != -1:
                    horizontal_minimun = np.log10(horizontal_minimun)
                if horizontal_maximun != -1:
                    horizontal_maximun = np.log10(horizontal_maximun)
                if vertical_minimun != -1:
                    vertical_minimun = np.log10(vertical_minimun)
                if vertical_maximun != -1:
                    vertical_maximun = np.log10(vertical_maximun)
            elif self.getConfiguration('horizontal_scale') == 'ln':
                if horizontal_minimun != -1:
                    horizontal_minimun = np.log(horizontal_minimun)
                if horizontal_maximun != -1:
                    horizontal_maximun = np.log(horizontal_maximun)
                if vertical_minimun != -1:
                    vertical_minimun = np.log(vertical_minimun)
                if vertical_maximun != -1:
                    vertical_maximun = np.log(vertical_maximun)

            if horizontal_minimun != -1 and horizontal_maximun != -1:
                self.main_plot.setRange(
                    xRange=(horizontal_minimun, horizontal_maximun))

            if vertical_minimun != -1 and vertical_maximun != -1:
                self.main_plot.setRange(
                    yRange=(vertical_minimun, vertical_maximun))

    def export(self, path=False, toBytes=None):
        selected_filter = '.png'

        if (toBytes is None) and not path:
            path, selected_filter = QtWidgets.QFileDialog.getSaveFileName(
                self,
                QtCore.QCoreApplication.translate('main_window', "Save figure as..."),
                self.getConfiguration('default_file_location', 'COMMON'),
                QtCore.QCoreApplication.translate(
                    'main_window', 'File {0}').format(' PNG (*.png);; ') +
                QtCore.QCoreApplication.translate(
                    'main_window', 'File {0}').format(' SVG (*.svg);; ') +
                QtCore.QCoreApplication.translate(
                    'main_window', 'File {0}').format(' JPG (*.jpg);; ') +
                QtCore.QCoreApplication.translate(
                    'main_window', 'File {0}').format(' JPEG (*.jpeg);; ') +
                QtCore.QCoreApplication.translate(
                    'main_window', 'File {0}').format(' ICO (*.ico)')
            )
            selected_filter = selected_filter.split('*')[-1][:-1]

            if not path:
                return None

            if not path.endswith(selected_filter):
                path += selected_filter
        elif not path:
            path = None

        text = self.position_label.text
        self.position_label.setText('')
        if selected_filter == '.svg':
            exporter = pg.exporters.SVGExporter(self.sceneObj)
        else:
            exporter = pg.exporters.ImageExporter(self.sceneObj)

        img = exporter.export(fileName=path, toBytes=toBytes)
        self.position_label.setText(text)

        return img

    def drawTheme(self):
        plot_color = self.theme_handler.skin_keys['plot_color']
        plot_background = self.theme_handler.skin_keys['plot_background']

        self.vertical_axis_label.opts['color'] = plot_color
        self.horizontal_axis_label.opts['color'] = plot_color
        self.vertical_axis_label.opts['size'] = '16px'
        self.horizontal_axis_label.opts['size'] = '16px'

        self.main_plot.titleLabel.opts['color'] = plot_color
        self.main_plot.titleLabel.opts['size'] = '20px'

        self.vertical_axis_label.setText('Count')
        self.horizontal_axis_label.setText('Channel')
        self.setBackground(plot_background)

        self.main_plot.setTitle('Main')
        self.main_plot.getAxis('bottom').setPen(pg.mkPen(color=plot_color, width=1))
        self.main_plot.getViewBox().border = QtGui.QColor(plot_color)

        if self.main_plot.listDataItems():
            self.main_plot.listDataItems()[0].setPen(plot_color)
            self.main_plot.listDataItems()[0].setSymbolPen(plot_color)

        if self.getConfiguration('signal_active'):
            plot_signal_area_color = self.theme_handler.skin_keys['plot_signal_area_color']

            self.signal_plot.titleLabel.opts['color'] = plot_signal_area_color
            self.signal_plot.titleLabel.opts['size'] = '20px'
            color = QtGui.QColor(plot_signal_area_color)
            color.setAlpha(100)
            self.signal_area.setBrush(color)
            self.signal_plot.setTitle("Signal (SG)")
            self.signal_plot.getAxis('left').setPen(pg.mkPen(color=plot_color, width=1))
            self.signal_plot.getAxis('bottom').setPen(pg.mkPen(color=plot_color, width=1))
            self.signal_plot.getViewBox().border = QtGui.QColor(plot_signal_area_color)

            if self.signal_plot.listDataItems():
                self.signal_plot.listDataItems()[0].setPen(plot_signal_area_color)
                self.signal_plot.listDataItems()[0].setSymbolPen(plot_signal_area_color)

            self.main_plot.getAxis('left').setStyle(showValues=False)
        else:
            self.main_plot.getAxis('left').setPen(pg.mkPen(color=plot_color, width=1))

        if self.getConfiguration('background_active'):
            plot_background_area_color = self.theme_handler.skin_keys['plot_background_area_color']

            self.background_plot.titleLabel.opts['color'] = plot_background_area_color
            self.background_plot.titleLabel.opts['size'] = '20px'
            color = QtGui.QColor(plot_background_area_color)
            color.setAlpha(100)
            self.background_area.setBrush(color)
            self.background_plot.setTitle("Background (BG)")
            self.background_plot.getAxis('left').setStyle(showValues=False)
            self.background_plot.getAxis('bottom').setPen(pg.mkPen(color=plot_color, width=1))
            self.background_plot.getViewBox().border = QtGui.QColor(plot_background_area_color)

            if self.background_plot.listDataItems():
                self.background_plot.listDataItems()[0].setPen(plot_background_area_color)
                self.background_plot.listDataItems()[0].setSymbolPen(plot_background_area_color)

        horizontal_greater_unit = self.getConfiguration('horizontal_greater_unit')
        horizontal_smallest_unit = self.getConfiguration('horizontal_smallest_unit')
        vertical_greater_unit = self.getConfiguration('vertical_greater_unit')
        vertical_smallest_unit = self.getConfiguration('vertical_smallest_unit')

        if self.getConfiguration('horizontal_scale') == 'log':
            if horizontal_greater_unit!= -1:
                horizontal_greater_unit = np.log10(horizontal_greater_unit)
            if horizontal_smallest_unit != -1:
                horizontal_smallest_unit = np.log10(horizontal_smallest_unit)
            if vertical_greater_unit != -1:
                vertical_greater_unit = np.log10(vertical_greater_unit)
            if vertical_smallest_unit != -1:
                vertical_smallest_unit = np.log10(vertical_smallest_unit)
        elif self.getConfiguration('horizontal_scale') == 'ln':
            if horizontal_greater_unit != -1:
                horizontal_greater_unit = np.log(horizontal_greater_unit)
            if horizontal_smallest_unit != -1:
                horizontal_smallest_unit = np.log(horizontal_smallest_unit)
            if vertical_greater_unit != -1:
                vertical_greater_unit = np.log(vertical_greater_unit)
            if vertical_smallest_unit != -1:
                vertical_smallest_unit = np.log(vertical_smallest_unit)

        if horizontal_greater_unit != -1:
            if horizontal_smallest_unit == -1:
                horizontal_smallest_unit = horizontal_greater_unit * 5/100
        else:
            horizontal_greater_unit = None
            horizontal_smallest_unit = None

        if self.getConfiguration('signal_active'):
            self.signal_plot.getAxis('top').setTickSpacing(horizontal_greater_unit, horizontal_smallest_unit)
            self.signal_plot.getAxis('bottom').setTickSpacing(horizontal_greater_unit, horizontal_smallest_unit)

        if self.getConfiguration('background_active'):
            self.background_plot.getAxis('top').setTickSpacing(horizontal_greater_unit, horizontal_smallest_unit)
            self.background_plot.getAxis('bottom').setTickSpacing(horizontal_greater_unit, horizontal_smallest_unit)

        self.main_plot.getAxis('top').setTickSpacing(horizontal_greater_unit, horizontal_smallest_unit)
        self.main_plot.getAxis('bottom').setTickSpacing(horizontal_greater_unit, horizontal_smallest_unit)

        if vertical_greater_unit != -1:
            if vertical_smallest_unit == -1:
                vertical_smallest_unit = vertical_greater_unit * 5 / 100
        else:
            vertical_greater_unit = None
            vertical_smallest_unit = None

        if self.getConfiguration('signal_active'):
            self.signal_plot.getAxis('left').setTickSpacing(vertical_greater_unit, vertical_smallest_unit)
            self.signal_plot.getAxis('right').setTickSpacing(vertical_greater_unit, vertical_smallest_unit)

        if self.getConfiguration('background_active'):
            self.background_plot.getAxis('left').setTickSpacing(vertical_greater_unit, vertical_smallest_unit)
            self.background_plot.getAxis('right').setTickSpacing(vertical_greater_unit, vertical_smallest_unit)

        self.main_plot.getAxis('left').setTickSpacing(vertical_greater_unit, vertical_smallest_unit)
        self.main_plot.getAxis('right').setTickSpacing(vertical_greater_unit, vertical_smallest_unit)

    def getConfiguration(self, key, file='GENREP'):
        return self.config_handler.configurations[file][key]
