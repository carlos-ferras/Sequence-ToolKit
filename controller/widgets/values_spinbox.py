#!/usr/bin/python3
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from PyQt5 import QtWidgets


class ValuesSpinBox(QtWidgets.QSpinBox):
    def __init__(self, parent=None):
        super(ValuesSpinBox, self).__init__(parent)

        self.setEnabled(False)

    def strings(self):
        return self._strings

    def setStrings(self, strings):
        if strings:
            self._strings = tuple(strings)
            self._values = dict(zip(strings, range(len(strings))))
            self.setRange(0, len(strings) - 1)
            self.setEnabled(True)
            self.setValue(self.value())
        else:
            self.clear()
            self.setEnabled(False)

    def textFromValue(self, value):
        try:
            return self._strings[value]
        except:
            return '         '

    def valueFromText(self, text):
        return self._values[text]
