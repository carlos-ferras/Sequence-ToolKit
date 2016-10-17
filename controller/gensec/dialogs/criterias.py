#!/usr/bin/python3
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from functools import partial

from view.gensec.dialogs.ui_criterias import Ui_criteria
from view.dialogs.base_dialog import BaseDialog


class Criterias(BaseDialog, Ui_criteria):
    def __init__(self, windows_title, parent=None):
        BaseDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle(windows_title)

        self.push_button_accept.clicked.connect(self.accept)
        self.push_button_cancel.clicked.connect(self.close)

        self.condition_1.currentIndexChanged.connect(partial(self.conditionChange, self.condition_1))
        self.condition_2.currentIndexChanged.connect(partial(self.conditionChange, self.condition_2))
        self.condition_3.currentIndexChanged.connect(partial(self.conditionChange, self.condition_3))

    def conditionChange(self, condition):
        if condition.currentIndex() == 2:
            enabled = True
        else:
            enabled = False
        if condition == self.condition_1:
            self.value_1.setEnabled(enabled)
        elif condition == self.condition_2:
            self.value_2.setEnabled(enabled)
        elif condition == self.condition_3:
            self.value_3.setEnabled(enabled)

    def getData(self):
        filters = []
        levels = (
            (self.condition_1, self.value_1),
            (self.condition_2, self.value_2),
            (self.condition_3, self.value_3),
        )
        for level in range(3):
            condition = levels[level][0]
            value = levels[level][1]

            if condition.currentIndex() == 1:
                filters.append((
                    level,
                    None
                ))
            elif condition.currentIndex() == 2:
                if value.text() and value.text() is not None:
                    filters.append((
                        level,
                        value.text()
                        ))
        return tuple(filters)
