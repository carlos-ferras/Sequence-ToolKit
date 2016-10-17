#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from functools import partial

from model.handle_config import ConfigHandler
from view.genrep.dialogs.ui_apply_this_to import Ui_apply_to
from view.dialogs.base_dialog import BaseDialog


class ApplyThisTo(BaseDialog, Ui_apply_to):
    def __init__(self, profile_parameters, parent=None):
        BaseDialog.__init__(self, parent)
        self.setupUi(self)

        self.config_handler = ConfigHandler()

        self.push_button_accept.clicked.connect(self.accept)
        self.push_button_cancel.clicked.connect(self.close)

        for parameter in self.getConfiguration('parameters', 'GENREP'):
            self.criterion_1.addItem(profile_parameters[parameter])
            self.criterion_2.addItem(profile_parameters[parameter])
            self.criterion_3.addItem(profile_parameters[parameter])
            self.criterion_4.addItem(profile_parameters[parameter])

        self.criterion_1.currentIndexChanged.connect(partial(self.criterionChange, self.criterion_1))
        self.criterion_2.currentIndexChanged.connect(partial(self.criterionChange, self.criterion_2))
        self.criterion_3.currentIndexChanged.connect(partial(self.criterionChange, self.criterion_3))
        self.criterion_4.currentIndexChanged.connect(partial(self.criterionChange, self.criterion_4))

        self.condition_1.currentIndexChanged.connect(partial(self.conditionChange, self.condition_1))
        self.condition_2.currentIndexChanged.connect(partial(self.conditionChange, self.condition_2))
        self.condition_3.currentIndexChanged.connect(partial(self.conditionChange, self.condition_3))
        self.condition_4.currentIndexChanged.connect(partial(self.conditionChange, self.condition_4))

        self.value_1.textChanged.connect(partial(self.valueChange, self.value_1))
        self.value_2.textChanged.connect(partial(self.valueChange, self.value_2))
        self.value_3.textChanged.connect(partial(self.valueChange, self.value_3))

    def criterionChange(self, criterion):
        enabled = False
        if criterion.currentIndex() > 0:
            enabled = True
        if criterion == self.criterion_1:
            condition = self.condition_1
        elif criterion == self.criterion_2:
            condition = self.condition_2
        elif criterion == self.criterion_3:
            condition = self.condition_3
        else:
            condition = self.condition_4
        condition.setEnabled(enabled)
        if not enabled:
            condition.setCurrentIndex(0)

    def conditionChange(self, condition):
        enabled_value = False
        criterion = False
        enabled_criterion = False
        if 0 < condition.currentIndex() < 3:
            enabled_criterion = True
        elif condition.currentIndex() == 3:
            enabled_value = True

        if condition == self.condition_1:
            value = self.value_1
            criterion = self.criterion_2
        elif condition == self.condition_2:
            value = self.value_2
            criterion = self.criterion_3
        elif condition == self.condition_3:
            value = self.value_3
            criterion = self.criterion_4
        else:
            value = self.value_4
        value.setEnabled(enabled_value)
        if not enabled_value:
            value.setText('')
        if criterion:
            criterion.setEnabled(enabled_criterion)
            if not enabled_criterion:
                criterion.setCurrentIndex(0)

    def valueChange(self, value):
        criterion = False
        enabled = False
        if value.text() and value.text() is not None:
            enabled = True
        if value == self.value_1:
            criterion = self.criterion_2
        elif value == self.value_2:
            criterion = self.criterion_3
        elif value == self.value_3:
            criterion = self.criterion_4
        if criterion:
            criterion.setEnabled(enabled)
            if not enabled:
                criterion.setCurrentIndex(0)

    def getData(self):
        filters = []
        levels = (
            (self.criterion_1, self.condition_1, self.value_1),
            (self.criterion_2, self.condition_2, self.value_2),
            (self.criterion_3, self.condition_3, self.value_3),
            (self.criterion_4, self.condition_4, self.value_4),
        )
        for level in levels:
            criterion = level[0]
            condition = level[1]
            value = level[2]

            if criterion.isEnabled():
                if 0 < condition.currentIndex() < 3:
                    filters.append((
                        criterion.currentIndex() - 1,
                        condition.currentIndex(),
                        None
                    ))
                elif condition.currentIndex() == 3:
                    if value.text() and value.text() is not None:
                        filters.append((
                            criterion.currentIndex() - 1,
                            condition.currentIndex(),
                            value.text()
                        ))
        return tuple(filters)

    def getConfiguration(self, key, file):
        return self.config_handler.configurations[file][key]

    def setConfiguration(self, key, value, file):
        self.config_handler.configurations[file][key] = value
        self.config_handler.save(file)
