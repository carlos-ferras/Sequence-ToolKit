#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from PyQt5 import QtWidgets, QtCore

class BaseDialog(QtWidgets.QDialog):
    closed = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(BaseDialog, self).__init__(parent)

    def closeEvent(self, event):
        self.closed.emit()
        return event.accept()

    def keyPressEvent(self, event):
        if not event.key() == QtCore.Qt.Key_Escape:
            return super(BaseDialog, self).keyPressEvent(event)
        else:
            self.close()
            return event.ignore()
