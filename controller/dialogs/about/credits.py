#!/usr/bin/python3
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from PyQt5 import QtWidgets

from view.dialogs.about.ui_credits import Ui_credits


class Credits(QtWidgets.QWidget, Ui_credits):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)
