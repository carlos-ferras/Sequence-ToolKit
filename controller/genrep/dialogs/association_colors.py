#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from PyQt5 import QtWidgets, QtGui, QtCore

from functools import partial

from controller.dialogs.colors import Colors


class AssociationColors(Colors):
    show_error_message = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        Colors.__init__(self, parent)

        self.color1_palette = self.getConfiguration('association_color_1', 'GENREP')
        self.color2_palette = self.getConfiguration('association_color_2', 'GENREP')
        self.color3_palette = self.getConfiguration('association_color_3', 'GENREP')
        self.color1.mouseDoubleClickEvent = partial(self.colorClicked, 'association_color_1')
        self.color2.mouseDoubleClickEvent = partial(self.colorClicked, 'association_color_2')
        self.color3.mouseDoubleClickEvent = partial(self.colorClicked, 'association_color_3')

        self.fillValues()

    def colorClicked(self, color_name, event):
        color = QtGui.QColor(self.getConfiguration(color_name, 'GENREP'))
        dialog = QtWidgets.QColorDialog(color, self.parent())
        dialog.setOption(QtWidgets.QColorDialog.DontUseNativeDialog)
        palette = (
            '#ffffff', '#f48fb1', '#e91e63', '#f44336', '#d32f2f', '#b71c1c', '#ce93d8', '#9c27b0',
            '#673ab7', '#3f51b5', '#303f97', '#311b92', '#81d4fa', '#03a9f4', '#2196f3', '#1976d2',
            '#0077bd', '#0d47a1', '#80deea', '#00bcd4', '#4db6ac', '#0097a7', '#009688', '#00695c',
            '#c5e1a5', '#9ccc65', '#81c784', '#4caf50', '#689f38', '#2e7d32', '#e6ee9c', '#d4e157',
            '#cddc39', '#c0ca33', '#9e9d24', '#827717', '#ffee58', '#ffeb3b', '#ffca28', '#ffc107',
            '#fbc02d', '#ff8f00', '#ffbf4d', '#ff9800', '#ff5722', '#795348', '#455a64', '#000000',
        )
        for i in range(len(palette)):
            dialog.setStandardColor(i, QtGui.QColor(palette[i]))
        action = dialog.exec_()

        if action:
            color = dialog.selectedColor()
            pm = QtGui.QPixmap(500, 500)
            pm.fill(color)
            if not color.name() in [self.color1_palette, self.color2_palette, self.color3_palette]:
                if color_name == 'association_color_1':
                    self.color1.setPixmap(pm)
                    self.color1_palette = color.name()
                elif color_name == 'association_color_2':
                    self.color2.setPixmap(pm)
                    self.color2_palette = color.name()
                elif color_name == 'association_color_3':
                    self.color3.setPixmap(pm)
                    self.color3_palette = color.name()
            else:
                self.show_error_message.emit(
                    QtCore.QCoreApplication.translate(
                        'color_dialog',
                        "Association colors must be different."
                    )
                )

    def saveData(self):
        self.setConfiguration('association_color_1', self.color1_palette, 'GENREP')
        self.setConfiguration('association_color_2', self.color2_palette, 'GENREP')
        self.setConfiguration('association_color_3', self.color3_palette, 'GENREP')
