#!/usr/bin/python3
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from PyQt5 import QtWidgets, QtCore

from view.dialogs.ui_xml_preview import Ui_main_window


class XMLPreview(QtWidgets.QMainWindow, Ui_main_window):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        width = self.width()
        height = self.height()
        widget = QtWidgets.QDesktopWidget()
        main_screen_size = widget.availableGeometry(widget.primaryScreen())
        pos_x = (main_screen_size.width() / 2) - (width / 2)
        pos_y = (main_screen_size.height() / 2) - (height / 2)
        self.setGeometry(QtCore.QRect(pos_x, pos_y, width, height))

