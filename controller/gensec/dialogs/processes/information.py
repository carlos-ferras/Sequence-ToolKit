#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from PyQt5 import QtWidgets, QtCore

from view.dialogs.base_dialog import BaseDialog
from view.gensec.dialogs.processes.ui_information import Ui_process


class Information(BaseDialog, Ui_process):
    def __init__(self, date_type, comments, parent=None):
        BaseDialog.__init__(self, parent)
        self.setupUi(self)

        self.push_button_accept.clicked.connect(self.accept)
        self.push_button_cancel.clicked.connect(self.close)

        width = self.sizeHint().width()
        height = self.sizeHint().height()
        widget = QtWidgets.QDesktopWidget()
        main_screen_size = widget.availableGeometry(widget.primaryScreen())
        pos_x = (main_screen_size.width() / 2) - (width / 2)
        pos_y = (main_screen_size.height() / 2) - (height / 2)
        self.setGeometry(QtCore.QRect(pos_x, pos_y, width, height))

        self.fill(date_type, comments)

    def fill(self, date_type, comments):
        if date_type and date_type is not None and date_type != 'None':
            self.date_type.setText(date_type)
        if comments and comments is not None and comments != 'None':
            self.comments.setText(comments)

    def getData(self):
        return self.date_type.text(), self.comments.text()
