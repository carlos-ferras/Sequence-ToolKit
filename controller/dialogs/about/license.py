#!/usr/bin/python3
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from PyQt5 import QtWidgets

from view.dialogs.about.ui_license import Ui_license


class License(QtWidgets.QWidget, Ui_license):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)
