#!/usr/bin/python3
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import os
import subprocess
from functools import partial
import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui, QtNetwork

from controller.dialogs.xml_preview import XMLPreview
from controller.genrep.dialogs.about import AboutGenRep
from controller.genrep.dialogs.apply_this_to import ApplyThisTo
from controller.genrep.dialogs.association_by_criterion import AssociationByCriterion
from controller.genrep.dialogs.association_colors import AssociationColors
from controller.genrep.dialogs.profile import Profile
from controller.genrep.dialogs.setup import Setup
from controller.genrep.genrep_tab import GenRepTab
from controller.genrep.plot import PlotWidget, PlotToolBar
from controller.stk.dialogs.about import AboutSTK
from controller.stk.dialogs.settings import Settings
from model.custom_data_type import CustomIndex
from model.handle_config import ConfigHandler
from model.handle_recent_files import RecentFilesHandler
from model.handle_theme import ThemeHandler
from view.genrep.ui_genrep import Ui_main_window
from controller.decorators import loadingCursor
from controller.genrep.undo_framework_commands import ApplyTo, ApplyToAll, UpdateSignalArea, \
    UpdateBackgroundArea, UpdateSignalLimits, UpdateBackgroundLimits


class GenRep(Ui_main_window):
    def __init__(self, appname, dirs=None):
        self.appname = appname
        self.main_window = QtWidgets.QMainWindow()
        self.setupUi(self.main_window)

        self.theme_handler = ThemeHandler()
        self.config_handler = ConfigHandler()
        self.recent_files_handler = RecentFilesHandler()
        self.translator = []
        self.lock_plot = False

        if self.getConfiguration('pos_x') is None or 'None':
            widget = QtWidgets.QDesktopWidget()
            main_screen_size = widget.availableGeometry(widget.primaryScreen())
            pos_x = (main_screen_size.width() / 2) - (int(self.getConfiguration('width')) / 2)
            pos_y = (main_screen_size.height() / 2) - (int(self.getConfiguration('height')) / 2)

            self.geometryUpdate(
                pos_x,
                pos_y
            )

        self.main_window.setGeometry(QtCore.QRect(
            int(self.getConfiguration('pos_x')),
            int(self.getConfiguration('pos_y')),
            int(self.getConfiguration('width')),
            int(self.getConfiguration('height'))
        ))

        self.animator = QtCore.QPropertyAnimation(self.animation_area, b'pos', self.main_window)
        self.animator.finished.connect(self.animatorFinished)
        self.animator_state = False
        self.animation_handler.mouseDoubleClickEvent = self.showHidePlot
        self.main_window.resizeEvent = self.onResize

        self.action_undo.setEnabled(False)
        self.action_redo.setEnabled(False)
        self.action_group.setEnabled(False)
        self.action_ungroup.setEnabled(False)

        # file
        self.action_open.triggered.connect(self.openSLF)
        self.action_save.triggered.connect(self.save)
        self.action_save_as.triggered.connect(self.saveAs)
        self.action_save_all.triggered.connect(self.saveAll)
        self.action_print.triggered.connect(self.print)
        self.main_window.setAcceptDrops(True)
        self.main_window.dropEvent = self.onDrop
        self.main_window.dragEnterEvent = self.onDrag
        self.main_window.dragMoveEvent = self.onDrag

        # open dialog
        self.action_settings.triggered.connect(self.settings)
        self.action_help.triggered.connect(self.help)
        self.action_about_genrep.triggered.connect(self.aboutGenRep)
        self.action_preview.triggered.connect(self.xmlPreview)
        self.action_about.triggered.connect(self.aboutSTK)
        self.action_association_colors.triggered.connect(self.associationColors)
        self.action_association_by_criteria.triggered.connect(self.associationByCriteria)
        self.action_profile.triggered.connect(self.profile)
        self.action_setup.triggered.connect(self.setup)
        self.apply_all.clicked.connect(self.applyToAll)
        self.apply_to.clicked.connect(self.applyTo)

        # edit
        self.action_undo.triggered.connect(partial(self.execInCurrentTab, 'undo'))
        self.action_redo.triggered.connect(partial(self.execInCurrentTab, 'redo'))
        self.action_group.triggered.connect(partial(self.execInCurrentTab, 'group'))
        self.action_ungroup.triggered.connect(partial(self.execInCurrentTab, 'ungroup'))
        self.action_ungroup_all.triggered.connect(partial(self.execInCurrentTab, 'ungroupAll'))

        self.action_exec_gensec.triggered.connect(self.execGenSec)
        self.action_exec_genvis.triggered.connect(self.execGenVis)

        # close events
        self.action_close.triggered.connect(self.closeTab)
        self.tab_widget.tabCloseRequested.connect(self.closeTab)
        self.action_quit.triggered.connect(self.main_window.close)
        self.main_window.closeEvent = self.quit

        self.tab_widget.currentChanged.connect(self.tabContentChanged)
        self.recent_files_handler.signals.recent_file_added.connect(self.fillRecentFiles)
        self.columns_list.itemSelectionChanged.connect(self.updatePlot)

        self.setting_watsh = QtNetwork.QLocalServer(self.main_window)
        self.setting_watsh.newConnection.connect(self.settingTrigger)
        self.setting_watsh.listen(os.path.join(self.config_handler.config_path, 'listening', self.appname))

        self.settingsChange()

        # plot handlers
        self.signal_low.valueChanged.connect(self.updateSignalArea)
        self.signal_high.valueChanged.connect(self.updateSignalArea)
        self.background_low.valueChanged.connect(self.updateBackgroundArea)
        self.background_high.valueChanged.connect(self.updateBackgroundArea)
        self.tool_button_next.clicked.connect(partial(self.execInCurrentTab, 'goNextRow'))
        self.tool_button_previous.clicked.connect(partial(self.execInCurrentTab, 'goPreviousRow'))
        self.push_button_go.clicked.connect(partial(self.execInCurrentTab, 'goCustomRow'))

        self.plot_toolbar = PlotToolBar(self.main_window)
        self.plot_toolbar.setOrientation(QtCore.Qt.Vertical)
        self.plot_toolbar.setMaximumWidth(60)
        self.verticalLayout.addWidget(self.plot_toolbar)
        self.verticalLayout.setAlignment(QtCore.Qt.AlignVCenter)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.plot_toolbar.home.triggered.connect(self.plot_area.home)
        self.plot_toolbar.export.triggered.connect(self.plot_area.export)
        self.plot_area.signal_change.connect(self.updateSignalLimits)
        self.plot_area.background_change.connect(self.updateBackgroundLimits)

        if dirs and dirs is not None:
            self.openSLF(dirs)
        else:
            self.new()

        self.fillRecentFiles(True)

    # --------------------------------------------------------------------------------

    def execGenSec(self):
        command = None
        if os.sys.platform in ('linux', 'linux2'):
            if os.path.exists('gensec.py'):
                command = 'python3 gensec.py '
        elif os.path.exists('GenSec.exe'):
            command = 'GenSec.exe '
        if command is not None:
            subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE
            )
        else:
            self.showErrorMessage(
                QtCore.QCoreApplication.translate(
                    'main_window',
                    'Unable to launch {0}').format('GenSec')
            )

    def execGenVis(self):
        command = None
        if os.sys.platform in ('linux', 'linux2'):
            if os.path.exists('genvis.py'):
                command = 'python3 genvis.py '
        elif os.path.exists('GenVis.exe'):
            command = 'GenVis.exe '
        if command is not None:
            subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE
            )
        else:
            self.showErrorMessage(
                QtCore.QCoreApplication.translate(
                    'main_window',
                    'Unable to launch {0}').format('GenVis')
            )

    def updateSignalCount(self):
        if self.getConfiguration('signal_active', 'GENREP'):
            count = 0
            region = self.plot_area.signal_area.getRegion()

            if self.getConfiguration('horizontal_scale') == 'log':
                region = round(10 ** region[0]), round(10 ** region[1])
            elif self.getConfiguration('horizontal_scale') == 'ln':
                region = round(np.e ** region[0]), round(np.e ** region[1])

            if region[0]:
                region = [int(((0 - (region[0] % int(region[0]))) * -1) + region[0]), int(region[1])]
                for i in self.plot_area.y_values[region[0] - 1:region[1]]:
                    count += i
                count = int(count)
            self.signal.setText(str(count) if count else '')
        else:
            self.signal.clear()

    def updateBackgroundCount(self):
        if self.getConfiguration('background_active', 'GENREP'):
            count = 0
            region = self.plot_area.background_area.getRegion()

            if self.getConfiguration('horizontal_scale') == 'log':
                region = round(10 ** region[0]), round(10 ** region[1])
            elif self.getConfiguration('horizontal_scale') == 'ln':
                region = round(np.e ** region[0]), round(np.e ** region[1])

            if region[0]:
                region = [int(((0 - (region[0] % int(region[0]))) * -1) + region[0]), int(region[1])]
                for i in self.plot_area.y_values[region[0] - 1:region[1]]:
                    count += i
                count = int(count)
            self.background.setText(str(count) if count else '')
        else:
            self.background.clear()

    def updateSignalLimits(self, low, high):
        if low !=self.signal_low.value() + 1 or high !=self.signal_high.value() + 1:
            self.runCommand('UpdateSignalLimits', self, low, high)

    def updateBackgroundLimits(self, low, high):
        if low != self.background_low.value() + 1 or high != self.background_high.value() + 1:
            self.runCommand('UpdateBackgroundLimits', self, low, high)

    def updateSignalArea(self):
        region = self.plot_area.signal_area.getRegion()

        if self.getConfiguration('horizontal_scale') == 'log':
            region = round(10 ** region[0]), round(10 ** region[1])
        elif self.getConfiguration('horizontal_scale') == 'ln':
            region = round(np.e ** region[0]), round(np.e ** region[1])

        if region[0] != self.signal_low.value() + 1 or region[1] != self.signal_high.value() + 1:
            self.runCommand('UpdateSignalArea', self)

    def updateBackgroundArea(self):
        region = self.plot_area.background_area.getRegion()

        if self.getConfiguration('horizontal_scale') == 'log':
            region = round(10 ** region[0]), round(10 ** region[1])
        elif self.getConfiguration('horizontal_scale') == 'ln':
            region = round(np.e ** region[0]), round(np.e ** region[1])

        if region[0] != self.background_low.value() + 1 or region[1] !=self.background_high.value() + 1:
            self.runCommand('UpdateBackgroundArea', self)

    def saveSignalBackgroundInPos(self, position=None):
        if self.plot_area.x_values:
            if self.getConfiguration('signal_active', 'GENREP'):
                signal_low = self.plot_area.x_values[self.signal_low.value()]
                signal_high = self.plot_area.x_values[self.signal_high.value()]
            else:
                signal_low = self.plot_area.x_values[0]
                signal_high = self.plot_area.x_values[int(self.getConfiguration('high_signal', 'GENREP') - 1)]

            if self.getConfiguration('background_active', 'GENREP'):
                background_low = self.plot_area.x_values[self.background_low.value()]
                background_high = self.plot_area.x_values[self.background_high.value()]
            else:
                background_low = self.plot_area.x_values[int(self.getConfiguration('low_background', 'GENREP') - 1)]
                background_high = self.plot_area.x_values[-1]

            correct = True
            if position is None:
                position = self.tab_widget.currentWidget().ploting_pos
            else:
                row, column, curve = position.split(',')
                x_values, _ = self.tab_widget.currentWidget().valuesOf(row, column, curve)

                if background_high > x_values[-1]:
                    background_low -= background_high - x_values[-1]
                    background_high = x_values[-1]

                if (signal_low > x_values[-1]) or (signal_high > x_values[-1]) or (background_low > x_values[-1]) or (background_high > x_values[-1]):
                    correct = False

            if correct:
                self.tab_widget.currentWidget().signal_values[position] = (
                    signal_low,
                    signal_high
                )
                self.tab_widget.currentWidget().background_values[position] = (
                    background_low,
                    background_high
                )

    @loadingCursor(empty=True)
    def updatePlot(self):
        if not self.lock_plot:
            x_values = []
            y_values = []

            old_ploting_pos = self.tab_widget.currentWidget().ploting_pos

            if self.columns_list.selectedItems():
                item = self.columns_list.selectedItems()[0]
                curve = str(item.text(0))
                column_header = item.parent().text(0)

                for column in range(self.tab_widget.currentWidget().column_count)[2:]:
                    if self.tab_widget.currentWidget().tree_widget.header().model().headerData(column, QtCore.Qt.Horizontal) == column_header:
                        x_values, y_values = self.tab_widget.currentWidget().valuesOf(self.current_row.value() - 1, column, curve)
                        self.tab_widget.currentWidget().ploting_pos = str(self.current_row.value() - 1) + ',' + str(column) + ',' + str(curve)
                        break

            low_signal, high_signal, low_background, high_background, default = self.tab_widget.currentWidget().getLowHigh()

            spin_values = ['%.4f' % i for i in x_values]
            if self.getConfiguration('signal_active', 'GENREP'):
                self.signal_low.setStrings(spin_values)
                self.signal_high.setStrings(spin_values)
            else:
                self.signal_low.setStrings(False)
                self.signal_high.setStrings(False)
            if self.getConfiguration('background_active', 'GENREP'):
                self.background_low.setStrings(spin_values)
                self.background_high.setStrings(spin_values)
            else:
                self.background_low.setStrings(False)
                self.background_high.setStrings(False)

            self.plot_area.updatePlot(
                x_values,
                y_values,
                ls=low_signal,
                hs=high_signal,
                lb=low_background,
                hb=high_background,
                default=default
            )

            self.updateSignalCount()
            self.updateBackgroundCount()

            if old_ploting_pos != self.tab_widget.currentWidget().ploting_pos and \
                    self.tab_widget.currentWidget().undo_stack.count():
                self.tab_widget.currentWidget().undo_stack.clear()
                self.tab_widget.currentWidget().undo_stack_macro = 0

    def onResize(self, event):
        if self.animator_state:
            self.animator.setStartValue(QtCore.QPointF(0, self.central_widget.height()))
            self.animator.setEndValue(QtCore.QPointF(0, self.central_widget.height() - 16))
            self.animator.start()

    def animatorFinished(self):
        if not self.animator_state:
            self.gridLayout.addWidget(self.animation_area, 1, 0, 1, -1)
            self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.animation_area.setEnabled(True)

    def showHidePlot(self, event):
        self.animation_area.setEnabled(False)
        self.animator.setDuration(400)
        self.animator.setLoopCount(1)
        if not self.animator_state:
            self.gridLayout.removeWidget(self.animation_area)
            self.gridLayout.setContentsMargins(0, 0, 0, 16)
            self.animation_aria_height = self.central_widget.height()-self.animation_area.height()
            self.animator.setStartValue(QtCore.QPointF(0, self.animation_aria_height))
            self.animator.setEndValue(QtCore.QPointF(0, self.central_widget.height()-16))
        else:
            self.animator.setStartValue(QtCore.QPointF(QtCore.QPointF(0, self.central_widget.height()-16)))
            self.animator.setEndValue(QtCore.QPointF(0, self.animation_aria_height))
        self.animator_state = not self.animator_state
        self.animator.start()

    def onDrag(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def onDrop(self, event):
        paths = []
        path_list = event.mimeData().text().split('\r\n')
        for path in path_list:
            path = os.path.normpath(path).split(':')[-1]
            if path and path != '.':
                paths.append(path)
        self.openSLF(paths)

    @loadingCursor()
    def new(self, path=False):
        current_tab = GenRepTab(self.profile_parameters, self.main_window)
        current_tab.document_changed.connect(self.tabChanged)
        current_tab.document_saved.connect(self.tabSaved)
        current_tab.show_success_message.connect(self.showSuccessMessage)
        current_tab.show_info_message.connect(self.showInfoMessage)
        current_tab.show_error_message.connect(self.showErrorMessage)

        index = self.tab_widget.addTab(
            current_tab,
            str(self.tab_widget.count() + 1) + '. ' +
            QtCore.QCoreApplication.translate('main_window', 'Untitled')
        )
        self.tab_widget.setTabToolTip(index, QtCore.QCoreApplication.translate('main_window', 'Untitled'))
        self.tab_widget.setCurrentIndex(index)

        if path:
            current_tab.open(path)
            current_tab.working_slf = path
            self.changeWindowsTitle(path)
            self.statusbar.showMessage(
                QtCore.QCoreApplication.translate('main_window',
                                                  '"{0}" is ready to use.').format(path),
                3000
            )
        else:
            self.statusbar.showMessage(
                QtCore.QCoreApplication.translate('main_window',
                                                  'New document is ready.'),
                3000
            )
        return index

    def openInCurrent(self, path):
        self.tab_widget.currentWidget().open(path)
        self.tab_widget.currentWidget().working_slf = path
        self.changeWindowsTitle(path)

    def openSLF(self, paths=False):
        if not paths:
            dialog = QtWidgets.QFileDialog(
                self.main_window,
                QtCore.QCoreApplication.translate('main_window', "Choose one or more files to open"),
                self.getConfiguration('default_file_location', 'COMMON'),
                QtCore.QCoreApplication.translate('main_window', 'File {0}').format(' SLF (*.slf)')
            )
            dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
            dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
            dialog.setViewMode(QtWidgets.QFileDialog.List)

            action = dialog.exec_()
            paths = []
            if action:
                paths = dialog.selectedFiles()

        for path in paths:
            if os.path.exists(path) and os.path.isfile(path):
                if os.path.splitext(path)[-1] == '.slf':
                    self.recent_files_handler.appendPath(path, 'GENREP')
                    if (self.tab_widget.currentWidget() is not None) and self.tab_widget.currentWidget().isEmpty():
                        self.openInCurrent(path)
                    else:
                        self.new(path)
                    self.tab_widget.currentWidget().selectRow(0)
                else:
                    self.showErrorMessage(
                        QtCore.QCoreApplication.translate('main_window', 'The file "{0}" is not valid, must be an slf.').format(path))
            else:
                self.showErrorMessage(QtCore.QCoreApplication.translate('main_window', 'The file "{0}" does not exist.').format(path))
        if self.tab_widget.count() == 0:
            self.new()

    def save(self, index=None):
        if (index is None) or (index is False):
            index = self.tab_widget.currentIndex()
        path = self.tab_widget.tabToolTip(index)
        if os.path.exists(path) and os.path.isfile(path) and (path.endswith('.rlf') or path.endswith('.xml') or path.endswith('.txt')):
            self.tab_widget.widget(index).save(path)
            if path.endswith('.rlf'):
                self.recent_files_handler.appendPath(path, 'GENVIS')
            self.statusbar.showMessage(
                QtCore.QCoreApplication.translate('main_window',
                                                  '"{0}" has been saved.').format(path),
                3000
            )
        else:
            self.saveAs()

    def saveAs(self):
        root = self.getConfiguration('default_file_location', 'COMMON')
        working_slf = self.tab_widget.currentWidget().working_slf
        if working_slf is not None:
            working_slf = os.path.splitext(working_slf)[0]
            root = os.path.join(root, working_slf)
        path, selected_filter = QtWidgets.QFileDialog.getSaveFileName(
            self.main_window,
            QtCore.QCoreApplication.translate('main_window', "Save report as..."),
            root,
            QtCore.QCoreApplication.translate(
                'main_window', 'File {0}').format(' RLF (*.rlf);; ') +
            QtCore.QCoreApplication.translate(
                'main_window', 'File {0}').format(' XML (*.xml);; ') +
            QtCore.QCoreApplication.translate(
                'main_window', 'File {0}').format(' TXT (*.txt)')
        )

        if path:
            if ('xml' in selected_filter) and (not path.endswith('.xml')):
                path += '.xml'
            elif ('rlf' in selected_filter) and (not path.endswith('.rlf')):
                path += '.rlf'
            elif ('txt' in selected_filter) and (not path.endswith('.txt')):
                path += '.txt'

            title = str(self.tab_widget.currentIndex() + 1) + '. '

            if len(path) > 10:
                title += os.path.basename(path)
            else:
                title += path
            self.tab_widget.setTabText(self.tab_widget.currentIndex(), title)
            self.tab_widget.setTabToolTip(self.tab_widget.currentIndex(), path)
            self.tab_widget.currentWidget().save(path)
            if path.endswith('.rlf'):
                self.recent_files_handler.appendPath(path, 'GENVIS')
            self.statusbar.showMessage(
                QtCore.QCoreApplication.translate('main_window',
                                                  '"{0}" has been saved.').format(path),
                3000
            )

    def saveAll(self):
        for index in range(self.tab_widget.count()):
            self.save(index)
        self.statusbar.showMessage(
            QtCore.QCoreApplication.translate('main_window',
                                              'All reports has been saved.'),
            3000
        )

    def xmlPreview(self):
        dialog = XMLPreview(self.main_window)
        report = self.tab_widget.currentWidget().createRLF()
        dialog.xml_content.setText(report.preview())
        if self.action_save.isEnabled():
            dialog.action_save.triggered.connect(self.save)
        else:
            dialog.action_save.setEnabled(False)
        dialog.action_save_as.triggered.connect(self.saveAs)
        dialog.show()

    def print(self):
        self.statusbar.showMessage(
            QtCore.QCoreApplication.translate('main_window', 'Preparing for print.'),
        )
        self.tab_widget.widget(self.tab_widget.currentIndex()).print()
        self.statusbar.showMessage(
            QtCore.QCoreApplication.translate('main_window',
                                              'Table view has been printed.'),
            3000
        )

    # --------------------------------------------------------------------------------

    def settings(self):
        dialog = Settings(self.main_window)
        #dialog.accepted.connect(self.settingsChange)
        dialog.exec_()

    def associationColors(self):
        dialog = AssociationColors(self.main_window)
        dialog.accepted.connect(partial(self.associationColorsChange, dialog))
        dialog.show_error_message.connect(self.showErrorMessage)
        dialog.exec_()

    def associationByCriteria(self):
        self.association_by_criterion_dialog = AssociationByCriterion(self.profile_parameters, self.main_window)
        self.association_by_criterion_dialog.accepted.connect(self.associationByCriteriaAccepted)
        self.association_by_criterion_dialog.exec_()

    @loadingCursor(empty=True)
    def associationByCriteriaAccepted(self):
        filters = self.association_by_criterion_dialog.getData()
        for row in range(self.tab_widget.currentWidget().tree_widget.topLevelItemCount()):
            item = self.tab_widget.currentWidget().tree_widget.topLevelItem(row)
            sample = item.text(1)
            to_associate = []
            if sample:
                for column in range(self.tab_widget.currentWidget().column_count)[2:]:
                    if item.text(column):
                        current_data = None
                        if to_associate:
                            if ((self.getConfiguration('consecutive', 'GENREP') and to_associate[-1].column() + 1 == column) or
                                    not self.getConfiguration('consecutive', 'GENREP')):
                                current_data = self.tab_widget.currentWidget().process_data[
                                    str(to_associate[-1].row()) +
                                    ',' +
                                    str(to_associate[-1].column())
                                ]
                            else:
                                if len(to_associate) > 1:
                                    self.tab_widget.currentWidget().group(to_associate)
                                to_associate = []
                        data = self.tab_widget.currentWidget().process_data[str(row) + ',' + str(column)]
                        match = True
                        for filter_ in filters:
                            if match:
                                match = False
                                data_in_criterion = self.tab_widget.currentWidget().getData(
                                    filter_[0],
                                    data,
                                    sample
                                )
                                current_data_in_criterion = None
                                if current_data is not None:
                                    current_data_in_criterion = self.tab_widget.currentWidget().getData(
                                        filter_[0],
                                        current_data,
                                        sample
                                    )
                                if data_in_criterion is not None:
                                    if filter_[1] == 1:
                                        if current_data is not None:
                                            if data_in_criterion == current_data_in_criterion:
                                                match = True
                                        else:
                                            match = True
                                    elif filter_[1] == 2:
                                        if current_data is not None:
                                            if data_in_criterion != current_data_in_criterion:
                                                match = True
                                        else:
                                            match = True
                                    else:
                                        value = filter_[2]
                                        if '*' in value:
                                            while '*' in value:
                                                position = value.find('*')
                                                if str(data_in_criterion)[:position] != value[:position]:
                                                    break
                                                value = value[position + 1:]
                                                data_in_criterion = data_in_criterion[position + 1:]
                                                if data == data_in_criterion:
                                                    match = True
                                        else:
                                            if str(value) == str(data_in_criterion):
                                                match = True
                            break
                        if match:
                            to_associate.append(CustomIndex(row, column))
                if len(to_associate) > 1:
                    self.tab_widget.currentWidget().group(to_associate)

    def profile(self):
        dialog = Profile(self.profile_parameters, self.main_window)
        if self.tab_widget.currentWidget().process_data:
            dialog.accepted.connect(self.tabChanged)
        dialog.exec_()
        self.statusbar.showMessage(
            QtCore.QCoreApplication.translate('main_window',
                                              'New profile has been applied.'),
            3000
        )

    def setup(self):
        dialog = Setup(self.main_window)
        dialog.accepted.connect(self.setupAccepted)
        dialog.exec_()

    @loadingCursor(empty=True)
    def setupAccepted(self):
        self.lock_plot = True

        widget = self.tab_widget.currentWidget()
        if widget.ploting_pos is not None:
            widget.clearColumnList()
            widget.fillColumnsList()
            column = int(widget.ploting_pos.split(',')[1])
            curve = widget.ploting_pos.split(',')[2]
            if int(curve) in self.getConfiguration('curve_to_show'):
                for i in range(self.columns_list.topLevelItemCount()):
                    item = self.columns_list.topLevelItem(i)
                    if (not item.isHidden()) and item.text(0) == widget.tree_widget.header().model().headerData(column, QtCore.Qt.Horizontal):
                        for child in range(item.childCount()):
                            item_child = item.child(child)
                            if item_child.text(0) == curve:
                                item_child.setSelected(True)
                        break
            else:
                find = False
                for i in range(self.columns_list.topLevelItemCount()):
                    item = self.columns_list.topLevelItem(i)
                    if not item.isHidden():
                        item.child(0).setSelected(True)
                        find = True
                        break
                if not find and self.columns_list.selectedItems():
                    self.columns_list.selectedItems()[0].setSelected(False)
            self.tabChanged()
        self.statusbar.showMessage(
            QtCore.QCoreApplication.translate('main_window',
                                              'New configurations has been applied.'),
            3000
        )

        self.lock_plot = False

        if ((self.plot_area.signal_plot is None) and self.getConfiguration('signal_active')) or \
           ((self.plot_area.background_plot is None) and self.getConfiguration('background_active')) or \
           ((self.plot_area.signal_plot is not None) and not self.getConfiguration('signal_active')) or \
           ((self.plot_area.background_plot is not None) and not self.getConfiguration('background_active')):
            self.horizontalLayout.removeWidget(self.plot_area)
            self.plot_area.deleteLater()

            self.plot_area = PlotWidget(self.plot_and_tool_bar_area)
            self.plot_area.setMinimumSize(QtCore.QSize(0, 350))
            self.plot_area.setFrameShape(QtWidgets.QFrame.NoFrame)
            self.plot_area.setFrameShadow(QtWidgets.QFrame.Plain)
            self.plot_area.setLineWidth(0)
            self.horizontalLayout.addWidget(self.plot_area)

            self.plot_toolbar.home.triggered.connect(self.plot_area.home)
            self.plot_toolbar.export.triggered.connect(self.plot_area.export)
            self.plot_area.signal_change.connect(self.updateSignalLimits)
            self.plot_area.background_change.connect(self.updateBackgroundLimits)

            self.updatePlot()
        elif self.plot_area.y_values:
            self.updatePlot()
        self.plot_area.drawTheme()

    @loadingCursor(empty=True)
    def applyToAll(self):
        self.runCommand('ApplyToAll', self)

    def applyTo(self):
        self.apply_to_dialog = ApplyThisTo(self.profile_parameters, self.main_window)
        self.apply_to_dialog.accepted.connect(self.applyToAccepted)
        self.apply_to_dialog.push_button_apply_to_all.clicked.connect(self.applyToAll)
        self.apply_to_dialog.exec_()

    @loadingCursor(empty=True)
    def applyToAccepted(self):
        filters = self.apply_to_dialog.getData()
        self.runCommand('ApplyTo', self, filters)

    def help(self):
        subprocess.Popen('python3 assistant.py genrep', shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, stdin=subprocess.PIPE)

    def aboutGenRep(self):
        dialog = AboutGenRep(self.main_window)
        dialog.exec_()

    def aboutSTK(self):
        dialog = AboutSTK(self.main_window)
        dialog.exec_()

    # --------------------------------------------------------------------------------

    def showSuccessMessage(self, message_text, title=QtCore.QCoreApplication.translate('main_window', 'Successfully!')):
        self.showMessage('success', title, message_text)

    def showInfoMessage(self, message_text, title=QtCore.QCoreApplication.translate('main_window', 'Information')):
        self.showMessage('information', title, message_text)

    def showErrorMessage(self, message_text, title=QtCore.QCoreApplication.translate('main_window', 'Error!')):
        self.showMessage('error', title, message_text)

    def showWarningMessage(self, message_text, title=QtCore.QCoreApplication.translate('main_window', 'Warning!')):
        message = QtWidgets.QMessageBox(self.main_window)
        message.setIconPixmap(QtGui.QPixmap(':/resources/img/icons/warning.svg'))
        message.setWindowTitle(title)
        message.setText(message_text)
        message.addButton(QtWidgets.QApplication.translate('main_window', 'Discard'), QtWidgets.QMessageBox.RejectRole)
        message.addButton(QtWidgets.QApplication.translate('main_window', 'Continue'), QtWidgets.QMessageBox.AcceptRole)
        return message.exec_()

    def showQuestionMessage(self, message_text, title=QtCore.QCoreApplication.translate('main_window', 'Attention!')):
        message = QtWidgets.QMessageBox(self.main_window)
        message.setIconPixmap(QtGui.QPixmap(':/resources/img/icons/question.svg'))
        message.setWindowTitle(title)
        message.setText(message_text)
        message.addButton(QtWidgets.QMessageBox.Cancel)
        message.addButton(QtWidgets.QMessageBox.Yes)
        message.addButton(QtWidgets.QMessageBox.No)
        return message.exec_()

    def showMessage(self, type_, title, message_text):
        message = QtWidgets.QMessageBox(self.main_window)
        message.setIconPixmap(QtGui.QPixmap(':/resources/img/icons/' + type_ + '.svg'))
        message.setWindowTitle(title)
        message.setText(message_text)
        message.setStandardButtons(QtWidgets.QMessageBox.Ok)
        message.exec_()

    def associationColorsChange(self, dialog):
        old_color1_palette = self.getConfiguration('association_color_1', 'GENREP')
        old_color2_palette = self.getConfiguration('association_color_2', 'GENREP')
        old_color3_palette = self.getConfiguration('association_color_3', 'GENREP')

        color1_palette = dialog.color1_palette
        color2_palette = dialog.color2_palette
        color3_palette = dialog.color3_palette

        self.setConfiguration('association_color_1', color1_palette)
        self.setConfiguration('association_color_2', color2_palette)
        self.setConfiguration('association_color_3', color3_palette)

        for tab in range(self.tab_widget.count()):
            for row in range(self.tab_widget.widget(tab).tree_widget.topLevelItemCount()):
                item = self.tab_widget.widget(tab).tree_widget.topLevelItem(row)
                for column in range(item.columnCount()):
                    current_background = item.background(column).color().name()
                    if current_background == old_color1_palette:
                        item.setBackground(column, QtGui.QColor(color1_palette))
                    elif current_background == old_color2_palette:
                        item.setBackground(column, QtGui.QColor(color2_palette))
                    elif current_background == old_color3_palette:
                        item.setBackground(column, QtGui.QColor(color3_palette))

    def fillRecentFiles(self, initial=False):
        self.menu_recent_files.clear()

        if not self.recent_files_handler.recent_files['GENREP']:
            self.menu_recent_files.setEnabled(False)
        else:
            self.menu_recent_files.setEnabled(True)
        for date_path in self.recent_files_handler.recent_files['GENREP']:
            self.setRecentFile(date_path)

        if not initial:
            socket = QtNetwork.QLocalSocket(self.main_window)
            socket.connectToServer(
                os.path.join(self.config_handler.config_path, 'listening', 'STK'),
                QtCore.QIODevice.WriteOnly
            )
            if socket.state() == QtNetwork.QLocalSocket.ConnectedState:
                if not socket.waitForConnected(1000):
                    raise Exception(str(socket.errorString()))
                socket.write(b'refresh_recent_files')
                if not socket.waitForBytesWritten(1000):
                    raise Exception(str(socket.errorString()))
            socket.disconnectFromServer()

    def setRecentFile(self, date_path):
        action_file = QtWidgets.QAction(self.main_window)
        action_file.setStatusTip(date_path[0])
        action_file.setText(date_path[1])
        action_file.triggered.connect(partial(self.openSLF, [date_path[1]]))
        self.menu_recent_files.addAction(action_file)

    def tabChanged(self, widget=None):
        if (widget is None) or (widget is False):
            index = self.tab_widget.currentIndex()
        else:
            index = self.tab_widget.indexOf(widget)
        title = self.tab_widget.tabText(index)
        if not title.endswith('*'):
            title += '*'
        self.tab_widget.setTabText(index, title)

        if self.tab_widget.widget(index) is not None:
            self.tab_widget.widget(index).is_saved = False
            if index == self.tab_widget.currentIndex():
                self.action_save.setEnabled(True)

    def tabSaved(self, widget=None):
        if (widget is None) or (widget is False):
            index = self.tab_widget.currentIndex()
        else:
            index = self.tab_widget.indexOf(widget)
        title = self.tab_widget.tabText(index)
        if title.endswith('*'):
            title = title[:-1]
        self.tab_widget.setTabText(index, title)
        if self.tab_widget.widget(index) is not None:
            self.tab_widget.widget(index).is_saved = True
            if index == self.tab_widget.currentIndex():
                self.action_save.setEnabled(False)

    def tabContentChanged(self, index):
        widget = self.tab_widget.currentWidget()
        if widget is not None:
            self.changeWindowsTitle(widget.working_slf)
            widget.undoRedoChange()
            widget.itemSelectionChanged()
            self.action_save.setEnabled(not widget.is_saved)

            if widget.selected_row is not None:
                self.current_row.setValue(widget.selected_row + 1)
                widget.clearColumnList()
                widget.fillColumnsList()
                column = int(widget.ploting_pos.split(',')[1])
                curve = widget.ploting_pos.split(',')[2]
                for i in range(self.columns_list.topLevelItemCount()):
                    item = self.columns_list.topLevelItem(i)
                    if (not item.isHidden()) and item.text(0) == widget.tree_widget.header().model().headerData(column, QtCore.Qt.Horizontal):
                        for child in range(item.childCount()):
                            item_child = item.child(child)
                            if item_child.text(0) == curve:
                                item_child.setSelected(True)
                        break

    def settingTrigger(self):
        if self.setting_watsh.hasPendingConnections():
            self.setting_watsh.nextPendingConnection()
        self.settingsChange()

    @loadingCursor()
    def settingsChange(self):
        self.config_handler.load()

        lang = self.getConfiguration('lang', 'GLOBALS')
        theme = self.getConfiguration('theme', 'GLOBALS')
        skin = self.getConfiguration('skin', 'GLOBALS')

        opacity = self.getConfiguration('opacity', 'COMMON')
        font_style = self.getConfiguration('font-style', 'COMMON')

        font = [
            self.getConfiguration('font-family', 'COMMON'),
            self.getConfiguration('font-size', 'COMMON'),
            'normal',
            'normal',
        ]

        if font_style == 'Bold':
            font[3] = 'bold'
        elif font_style == 'Light':
            font[3] = '100'
        elif font_style == 'Book':
            font[3] = '300'
        elif font_style == 'Oblique':
            font[2] = 'oblique'

        qapp = QtCore.QCoreApplication.instance()

        self.theme_handler.load(theme, skin, font)
        qapp.setStyleSheet(self.theme_handler.theme)
        self.setConfiguration('widget_color', self.theme_handler.skin_keys['widget_color'], 'COMMON')
        old_tree_widget_item_background = ''
        try:
            old_tree_widget_item_background = self.getConfiguration('tree_widget_item_background', 'COMMON').lower()
            old_tree_widget_item_alternate_background = self.getConfiguration('tree_widget_item_alternate_background', 'COMMON').lower()
        except:
            pass
        self.setConfiguration('tree_widget_item_background', self.theme_handler.skin_keys['tree_widget_item_background'], 'COMMON')
        self.setConfiguration('tree_widget_item_alternate_background', self.theme_handler.skin_keys['tree_widget_item_alternate_background'], 'COMMON')
        self.main_window.setWindowOpacity(opacity)

        if self.translator:
            for translator in self.translator:
                QtCore.QCoreApplication.instance().removeTranslator(translator)
            self.translator = []
        if (not lang) or (lang is None) or (lang == 'locale') or (lang == 'None'):
            lang = QtCore.QLocale.system().name()

        translator = QtCore.QTranslator()
        if translator.load("resources/i18n/i18n_genrep." + lang):
            qapp.installTranslator(translator)
            self.translator.append(translator)

        stk_translator = QtCore.QTranslator()
        if stk_translator.load("resources/i18n/i18n_stk." + lang):
            qapp.installTranslator(stk_translator)
            self.translator.append(stk_translator)

        qt_translator = QtCore.QTranslator()
        if qt_translator.load("resources/i18n/i18n_qt." + lang):
            qapp.installTranslator(qt_translator)
            self.translator.append(qt_translator)

        qtbase_translator = QtCore.QTranslator()
        if qtbase_translator.load("resources/i18n/i18n_qtbase." + lang):
            qapp.installTranslator(qtbase_translator)
            self.translator.append(qtbase_translator)

        self.retranslateUi(self.main_window)

        self.profile_parameters = (
            QtCore.QCoreApplication.translate('profile', 'Beta Irradiation Time (s)'),
            QtCore.QCoreApplication.translate('profile', 'Beta Dose (Gy)'),
            QtCore.QCoreApplication.translate('profile', 'External Irradiation Time (s)'),
            QtCore.QCoreApplication.translate('profile', 'External Dose (Gy)'),
            QtCore.QCoreApplication.translate('profile', 'Preheating Temperature (°C)'),
            QtCore.QCoreApplication.translate('profile', 'Measuring Temperature (°C)'),
            QtCore.QCoreApplication.translate('profile', 'Preheating Rate (°C/s)'),
            QtCore.QCoreApplication.translate('profile', 'Heating Rate (°C/s)'),
            QtCore.QCoreApplication.translate('profile', 'Light Source'),
            QtCore.QCoreApplication.translate('profile', 'Optical Power (%)'),
            QtCore.QCoreApplication.translate('profile', 'Time of Beta irradiation'),
            QtCore.QCoreApplication.translate('profile', 'Time of External irradiation'),
            QtCore.QCoreApplication.translate('profile', 'Time of Measurement'),
            QtCore.QCoreApplication.translate('profile', 'Illumination Source'),
            QtCore.QCoreApplication.translate('profile', 'Illumination Power'),
            QtCore.QCoreApplication.translate('profile', 'Illumination Temperature'),
            # QtCore.QCoreApplication.translate('profile', 'Electric Stimulation (V)'),
            # QtCore.QCoreApplication.translate('profile', 'Electric Frequency (KHz)'),
        )

        if int(self.getConfiguration('font-size', 'COMMON')) > 12:
            height = int(int(self.getConfiguration('font-size', 'COMMON')) * 2.3333)
        else:
            height = 28
        for tab_index in range(self.tab_widget.count()):
            tab = self.tab_widget.widget(tab_index)
            tab.tree_widget.setStyleSheet('QTreeWidget::item{{height:{0}}}'.format(height))
            tab.tree_widget.headerItem().setText(
                0,
                QtCore.QCoreApplication.translate('tree_widget_tab', "Group")
            )
            tab.tree_widget.headerItem().setText(
                1,
                QtCore.QCoreApplication.translate('tree_widget_tab', "Sample")
            )
            for i in range(tab.column_count)[2:]:
                tab.tree_widget.headerItem().setText(
                    i,
                    QtCore.QCoreApplication.translate('tree_widget_tab', "Command {0}").format(i - 1)
                )
                for j in range(tab.tree_widget.topLevelItemCount()):
                    item = tab.tree_widget.topLevelItem(j)
                    tool_button_header = tab.tree_widget.itemWidget(item, 0)
                    tool_button_header.setToolTip(QtCore.QCoreApplication.translate('tree_widget_tab', 'Select Row'))
            if old_tree_widget_item_background:
                for i in range(tab.tree_widget.topLevelItemCount()):
                    if i % 2 == 0:
                        color = self.getConfiguration('tree_widget_item_background', 'COMMON')
                    else:
                        color = self.getConfiguration('tree_widget_item_alternate_background', 'COMMON')
                    for j in range(tab.column_count):
                        item = tab.tree_widget.topLevelItem(i)
                        background = item.background(j).color().name().lower()
                        if background in (old_tree_widget_item_background, old_tree_widget_item_alternate_background,):
                            item.setBackground(j, QtGui.QColor(color))


        self.plot_area.drawTheme()

        self.statusbar.showMessage(
            QtCore.QCoreApplication.translate('main_window',
                                              'New settings has been applied.'),
            3000
        )

    def execInCurrentTab(self, function_name):
        exec('self.tab_widget.currentWidget().' + function_name + '()')

    def changeWindowsTitle(self, path):
        title = 'GenRep'
        if path is not None:
            title += QtCore.QCoreApplication.translate('main_window', ' | Working on [{0}]').format(path)
        self.main_window.setWindowTitle(title)

    def closeTab(self, index=None):
        if index is None:
            index = self.tab_widget.currentIndex()

        action = QtWidgets.QMessageBox.NoRole
        if not self.tab_widget.widget(index).is_saved:
            action = self.showQuestionMessage(
                'Save changes to "' +
                self.tab_widget.tabToolTip(index) +
                '" before closing?'
            )

        if action == QtWidgets.QMessageBox.Yes:
            self.save(index)

        if action != QtWidgets.QMessageBox.Cancel:
            self.tab_widget.widget(index).undo_stack.clear()
            self.tab_widget.removeTab(index)
            if self.tab_widget.count() == 0:
                self.main_window.close()
            else:
                self.tab_widget.currentWidget().undoRedoChange()
                self.tab_widget.currentWidget().itemSelectionChanged()

                for i in range(self.tab_widget.count()):
                    title = self.tab_widget.tabText(i)
                    title = str(i+1) + '.' + '.'.join(title.split('.')[1:])
                    self.tab_widget.setTabText(i, title)

            return True
        return False

    def quit(self, event):
        for i in range(self.tab_widget.count())[::-1]:
            forward = self.closeTab(i)
            if not forward:
                return event.ignore()
        self.geometryUpdate(
            self.main_window.pos().x(),
            self.main_window.pos().y(),
            self.main_window.width(),
            self.main_window.height()
        )
        self.setConfiguration('running_state', 0)
        os.remove(os.path.join(self.config_handler.config_path, 'listening', self.appname))
        os.remove(os.path.join(self.config_handler.config_path, 'share_memory', self.appname))
        return event.accept()

    def geometryUpdate(self, pos_x, pos_y, width=None, height=None):
        self.setConfiguration('pos_x', pos_x)
        self.setConfiguration('pos_y', pos_y)
        if (width is not None) and (height is not None):
            self.setConfiguration('width', width)
            self.setConfiguration('height', height)

    def runCommand(self, command, *args):
        commands = {
            'ApplyTo': ApplyTo,
            'ApplyToAll': ApplyToAll,
            'UpdateSignalLimits': UpdateSignalLimits,
            'UpdateSignalArea': UpdateSignalArea,
            'UpdateBackgroundLimits': UpdateBackgroundLimits,
            'UpdateBackgroundArea': UpdateBackgroundArea,
        }
        current_tab = self.tab_widget.currentWidget()
        current_tab.undo_stack.beginMacro(str(current_tab.undo_stack_macro))
        current_tab.undo_stack.push(commands[command](*args))
        current_tab.undo_stack.endMacro()
        current_tab.undo_stack_macro += 1

    def getConfiguration(self, key, file='GENREP'):
        return self.config_handler.configurations[file][key]

    def setConfiguration(self, key, value, file='GENREP'):
        self.config_handler.configurations[file][key] = value
        self.config_handler.save(file)
