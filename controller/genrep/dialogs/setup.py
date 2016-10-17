#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from model.handle_config import ConfigHandler
from view.genrep.dialogs.ui_setup import Ui_setup
from view.dialogs.base_dialog import BaseDialog


class Setup(BaseDialog, Ui_setup):
    def __init__(self, parent=None):
        BaseDialog.__init__(self, parent)
        self.setupUi(self)
        self.adjustSize()

        self.config_handler = ConfigHandler()

        self.push_button_accept.clicked.connect(self.accept)
        self.push_button_cancel.clicked.connect(self.close)
        self.accepted.connect(self.saveData)

        self.automatic_minimum.clicked.connect(self.actveFormatAxis)
        self.fixed_minimum.clicked.connect(self.actveFormatAxis)
        self.automatic_maximum.clicked.connect(self.actveFormatAxis)
        self.fixed_maximum.clicked.connect(self.actveFormatAxis)
        self.automatic_greater.clicked.connect(self.actveFormatAxis)
        self.fixed_greater.clicked.connect(self.actveFormatAxis)
        self.automatic_smallest.clicked.connect(self.actveFormatAxis)
        self.fixed_smallest.clicked.connect(self.actveFormatAxis)

        self.automatic_minimum_2.clicked.connect(self.actveFormatAxis)
        self.fixed_minimum_2.clicked.connect(self.actveFormatAxis)
        self.automatic_maximum_2.clicked.connect(self.actveFormatAxis)
        self.fixed_maximum_2.clicked.connect(self.actveFormatAxis)
        self.automatic_greater_2.clicked.connect(self.actveFormatAxis)
        self.fixed_greater_2.clicked.connect(self.actveFormatAxis)
        self.automatic_smallest_2.clicked.connect(self.actveFormatAxis)
        self.fixed_smallest_2.clicked.connect(self.actveFormatAxis)

        self.fillValues()

    def fillValues(self):
        for curve in self.getConfiguration('curve_to_show', 'GENREP'):
            if curve == 1:
                self.curve_1.setChecked(True)
            elif curve == 2:
                self.curve_2.setChecked(True)
            elif curve == 3:
                self.curve_3.setChecked(True)

        if self.getConfiguration('show_tl', 'GENREP'):
            self.curve_vs_temperature.setChecked(True)
        else:
            self.curve_vs_time.setChecked(True)

        self.units.setCurrentIndex(self.getConfiguration('unit', 'GENREP'))
        if self.getConfiguration('horizontal_scale', 'GENREP') == 'lineal':
            self.lineal.setChecked(True)
        elif self.getConfiguration('horizontal_scale', 'GENREP') == 'log':
            self.log10.setChecked(True)
        else:
            self.ln.setChecked(True)
        if self.getConfiguration('horizontal_minimun', 'GENREP') == -1:
            self.automatic_minimum.setChecked(True)
        else:
            self.fixed_minimum.setChecked(True)
            self.fixed_minimum_value.setValue(self.getConfiguration('horizontal_minimun', 'GENREP'))
        if self.getConfiguration('horizontal_maximun', 'GENREP') == -1:
            self.automatic_maximum.setChecked(True)
        else:
            self.fixed_maximum.setChecked(True)
            self.fixed_maximum_value.setValue(self.getConfiguration('horizontal_maximun', 'GENREP'))
        if self.getConfiguration('horizontal_greater_unit', 'GENREP') == -1:
            self.automatic_greater.setChecked(True)
        else:
            self.fixed_greater.setChecked(True)
            self.fixed_greater_value.setValue(self.getConfiguration('horizontal_greater_unit', 'GENREP'))
        if self.getConfiguration('horizontal_smallest_unit', 'GENREP') == -1:
            self.automatic_smallest.setChecked(True)
        else:
            self.fixed_smallest.setChecked(True)
            self.fixed_smallest_value.setValue(self.getConfiguration('horizontal_smallest_unit', 'GENREP'))

        if self.getConfiguration('vertical_scale', 'GENREP') == 'lineal':
            self.lineal_2.setChecked(True)
        elif self.getConfiguration('vertical_scale', 'GENREP') == 'log':
            self.log10_2.setChecked(True)
        else:
            self.ln_2.setChecked(True)
        if self.getConfiguration('vertical_minimun', 'GENREP') == -1:
            self.automatic_minimum_2.setChecked(True)
        else:
            self.fixed_minimum_2.setChecked(True)
            self.fixed_minimum_value_2.setValue(self.getConfiguration('vertical_minimun', 'GENREP'))
        if self.getConfiguration('vertical_maximun', 'GENREP') == -1:
            self.automatic_maximum_2.setChecked(True)
        else:
            self.fixed_maximum_2.setChecked(True)
            self.fixed_maximum_value_2.setValue(self.getConfiguration('vertical_maximun', 'GENREP'))
        if self.getConfiguration('vertical_greater_unit', 'GENREP') == -1:
            self.automatic_greater_2.setChecked(True)
        else:
            self.fixed_greater_2.setChecked(True)
            self.fixed_greater_value_2.setValue(self.getConfiguration('vertical_greater_unit', 'GENREP'))
        if self.getConfiguration('vertical_smallest_unit', 'GENREP') == -1:
            self.automatic_smallest_2.setChecked(True)
        else:
            self.fixed_smallest_2.setChecked(True)
            self.fixed_smallest_value_2.setValue(self.getConfiguration('vertical_smallest_unit', 'GENREP'))

        self.actveFormatAxis()

        self.signal.setChecked(self.getConfiguration('signal_active', 'GENREP'))
        self.signal_low.setValue(self.getConfiguration('low_signal', 'GENREP'))
        self.signal_high.setValue(self.getConfiguration('high_signal', 'GENREP'))
        self.background.setChecked(self.getConfiguration('background_active', 'GENREP'))
        self.background_low.setValue(self.getConfiguration('low_background', 'GENREP'))
        self.background_high.setValue(self.getConfiguration('high_background', 'GENREP'))

    def actveFormatAxis(self):
        if self.automatic_minimum.isChecked():
            self.fixed_minimum_value.setEnabled(False)
            self.fixed_maximum.setEnabled(False)
            self.automatic_maximum.setChecked(True)
            self.fixed_maximum_value.setEnabled(False)
        else:
            self.fixed_minimum_value.setEnabled(True)
            self.fixed_maximum.setEnabled(True)
            self.fixed_maximum.setChecked(True)
            self.fixed_maximum_value.setEnabled(True)
        if self.automatic_greater.isChecked():
            self.fixed_greater_value.setEnabled(False)
            self.fixed_smallest.setEnabled(False)
            self.automatic_smallest.setChecked(True)
            self.fixed_smallest_value.setEnabled(False)
        else:
            self.fixed_greater_value.setEnabled(True)
            self.fixed_smallest.setEnabled(True)
            if self.automatic_smallest.isChecked():
                self.fixed_smallest_value.setEnabled(False)
            else:
                self.fixed_smallest_value.setEnabled(True)

        if self.automatic_minimum_2.isChecked():
            self.fixed_minimum_value_2.setEnabled(False)
            self.fixed_maximum_2.setEnabled(False)
            self.automatic_maximum_2.setChecked(True)
            self.fixed_maximum_value_2.setEnabled(False)
        else:
            self.fixed_minimum_value_2.setEnabled(True)
            self.fixed_maximum_2.setEnabled(True)
            self.fixed_maximum_2.setChecked(True)
            self.fixed_maximum_value_2.setEnabled(True)
        if self.automatic_greater_2.isChecked():
            self.fixed_greater_value_2.setEnabled(False)
            self.fixed_smallest_2.setEnabled(False)
            self.automatic_smallest_2.setChecked(True)
            self.fixed_smallest_value_2.setEnabled(False)
        else:
            self.fixed_greater_value_2.setEnabled(True)
            self.fixed_smallest_2.setEnabled(True)
            if self.automatic_smallest_2.isChecked():
                self.fixed_smallest_value_2.setEnabled(False)
            else:
                self.fixed_smallest_value_2.setEnabled(True)

    def saveData(self):
        curve_to_show = []
        if self.curve_1.isChecked():
            curve_to_show.append(1)
        if self.curve_2.isChecked():
            curve_to_show.append(2)
        if self.curve_3.isChecked():
            curve_to_show.append(3)
        self.setConfiguration('curve_to_show', curve_to_show, 'GENREP')

        show_tl = True
        if self.curve_vs_time.isChecked():
            show_tl = False
        self.setConfiguration('show_tl', show_tl, 'GENREP')

        self.setConfiguration('unit', self.units.currentIndex(), 'GENREP')
        horizontal_scale = 'lineal'
        if self.log10.isChecked():
            horizontal_scale = 'log'
        elif self.ln.isChecked():
            horizontal_scale = 'ln'
        self.setConfiguration('horizontal_scale', horizontal_scale, 'GENREP')
        horizontal_minimun = -1
        if self.fixed_minimum.isChecked():
            horizontal_minimun = self.fixed_minimum_value.value()
        self.setConfiguration('horizontal_minimun', horizontal_minimun, 'GENREP')
        horizontal_maximun = -1
        if self.fixed_maximum.isChecked():
            horizontal_maximun = self.fixed_maximum_value.value()
        self.setConfiguration('horizontal_maximun', horizontal_maximun, 'GENREP')
        horizontal_greater_unit = -1
        if self.fixed_greater.isChecked():
            horizontal_greater_unit = self.fixed_greater_value.value()
        self.setConfiguration('horizontal_greater_unit', horizontal_greater_unit, 'GENREP')
        horizontal_smallest_unit = -1
        if self.fixed_smallest.isChecked():
            horizontal_smallest_unit = self.fixed_smallest_value.value()
        self.setConfiguration('horizontal_smallest_unit', horizontal_smallest_unit, 'GENREP')

        vertical_scale = 'lineal'
        if self.log10_2.isChecked():
            vertical_scale = 'log'
        elif self.ln_2.isChecked():
            vertical_scale = 'ln'
        self.setConfiguration('vertical_scale', vertical_scale, 'GENREP')
        vertical_minimun = -1
        if self.fixed_minimum_2.isChecked():
            vertical_minimun = self.fixed_minimum_value_2.value()
        self.setConfiguration('vertical_minimun', vertical_minimun, 'GENREP')
        vertical_maximun = -1
        if self.fixed_maximum_2.isChecked():
            vertical_maximun = self.fixed_maximum_value_2.value()
        self.setConfiguration('vertical_maximun', vertical_maximun, 'GENREP')
        vertical_greater_unit = -1
        if self.fixed_greater_2.isChecked():
            vertical_greater_unit = self.fixed_greater_value_2.value()
        self.setConfiguration('vertical_greater_unit', vertical_greater_unit, 'GENREP')
        vertical_smallest_unit = -1
        if self.fixed_smallest_2.isChecked():
            vertical_smallest_unit = self.fixed_smallest_value_2.value()
        self.setConfiguration('vertical_smallest_unit', vertical_smallest_unit, 'GENREP')

        self.setConfiguration('signal_active', self.signal.isChecked(), 'GENREP')
        self.setConfiguration('low_signal', self.signal_low.value(), 'GENREP')
        self.setConfiguration('high_signal', self.signal_high.value(), 'GENREP')
        self.setConfiguration('background_active', self.background.isChecked(), 'GENREP')
        self.setConfiguration('low_background', self.background_low.value(), 'GENREP')
        self.setConfiguration('high_background', self.background_high.value(), 'GENREP')

    def getConfiguration(self, key, file):
        return self.config_handler.configurations[file][key]

    def setConfiguration(self, key, value, file):
        self.config_handler.configurations[file][key] = value
        self.config_handler.save(file)
