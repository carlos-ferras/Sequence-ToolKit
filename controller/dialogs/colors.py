#!/usr/bin/python3
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from PyQt5 import QtGui, QtCore

from view.dialogs.ui_colors import Ui_color_dialog
from view.dialogs.base_dialog import BaseDialog
from model.handle_config import ConfigHandler


class Colors(BaseDialog, Ui_color_dialog):
    show_error_message = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        BaseDialog.__init__(self, parent)
        self.setupUi(self)

        self.config_handler = ConfigHandler()

        self.push_button_accept.clicked.connect(self.accept)
        self.push_button_cancel.clicked.connect(self.close)

    def colorClicked(self, color_name, event):
        pass

    def saveData(self):
        pass

    def fillValues(self):
        pm = QtGui.QPixmap(500, 500)
        pm.fill(QtGui.QColor(self.color1_palette))
        self.color1.setPixmap(pm)

        pm = QtGui.QPixmap(500, 500)
        pm.fill(QtGui.QColor(self.color2_palette))
        self.color2.setPixmap(pm)

        pm = QtGui.QPixmap(500, 500)
        pm.fill(QtGui.QColor(self.color3_palette))
        self.color3.setPixmap(pm)

    def getConfiguration(self, key, file):
        return self.config_handler.configurations[file][key]

    def setConfiguration(self, key, value, file):
        self.config_handler.configurations[file][key] = value
        self.config_handler.save(file)
