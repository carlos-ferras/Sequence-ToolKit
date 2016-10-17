#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from PyQt5 import QtWidgets, QtCore

from controller.gensec.dialogs.processes.information import Information
from view.dialogs.base_dialog import BaseDialog
from view.gensec.dialogs.processes.ui_esl import Ui_process


class ESL(BaseDialog, Ui_process):
    def __init__(self, process_data=False, parent=None):
        BaseDialog.__init__(self, parent)
        self.setupUi(self)

        self.id = 6
        self.date_type = ''
        self.comments = ''
        self.time_per_channel_calculation = 0
        self.information_dialog = None

        self.push_button_accept.clicked.connect(self.accept)
        self.push_button_cancel.clicked.connect(self.close)
        self.push_button_info.clicked.connect(self.showInformationDialog)
        self.channels.valueChanged.connect(self.updateTimePerChannel)
        self.time.valueChanged.connect(self.updateTimePerChannel)
        self.time_measurement.currentIndexChanged.connect(self.updateTimePerChannel)
        self.ligh_co_stimulation.clicked.connect(self.lightCoStimulationChange)
        self.record_during_ee.clicked.connect(self.recordDuringEEChange)

        width = self.sizeHint().width()
        height = self.sizeHint().height()
        widget = QtWidgets.QDesktopWidget()
        main_screen_size = widget.availableGeometry(widget.primaryScreen())
        pos_x = (main_screen_size.width() / 2) - (width / 2)
        pos_y = (main_screen_size.height() / 2) - (height / 2)
        self.setGeometry(QtCore.QRect(pos_x, pos_y, width, height))

        self.fill(process_data)

    def fill(self, process_data):
        if process_data and process_data is not None:
            self.stabilization.setValue(process_data["stabilization"])
            self.heating_rate.setValue(process_data["heating_rate"])
            self.record_during_ee.setChecked(process_data["record_during"])
            self.ligh_co_stimulation.setChecked(process_data["light_co_stimulation"])

            self.ee_frequency.setValue(process_data["excF"])
            self.ee_voltage.setValue(process_data["excV"])

            self.ee_temp.setValue(process_data["final_temp"])
            self.time.setValue(self.convertTime(process_data["time"], process_data["time_unit"]))

            time_measurements = {
                'ms': 0,
                's': 1,
                'us': 2
            }
            self.time_measurement.setCurrentIndex(time_measurements[process_data["time_unit"]])

            if process_data["light_co_stimulation"]:
                self.optical_power.setValue(process_data["start_optical_power"])
                light_source = {
                    'Blue': 0,
                    'IR': 1,
                    'AUX': 2,
                }
                self.ligth_source.setCurrentIndex(light_source[process_data["light_source"]])

            if process_data["record_during"]:
                self.channels.setValue(process_data["datapoints2"])
                self.time_per_channel_calculation = process_data["timePerChannel"]
                self.updateTimePerChannel()

            self.date_type = process_data["date_type"]
            self.comments = process_data["comments"]

            self.lightCoStimulationChange()
            self.recordDuringEEChange()

    def showInformationDialog(self):
        self.information_dialog = Information(self.date_type, self.comments, self)
        self.information_dialog.accepted.connect(self.informationAccepted)
        self.information_dialog.exec_()

    def informationAccepted(self):
        self.date_type, self.comments = self.information_dialog.getData()
        self.information_dialog.close()

    def convertTime(self, time, time_measurement):
        if time_measurement == 'ms':
            return float(time) / 0.001
        elif time_measurement == 's':
            return float(time)
        elif time_measurement == 'us':
            return float(time) / 0.000001

    def getTime(self):
        time = self.time.value()
        if self.time_measurement.currentIndex() == 0:
            time *= 0.001
        elif self.time_measurement.currentIndex() == 1:
            pass
        elif self.time_measurement.currentIndex() == 2:
            time = self.toString(time * 0.000001)
        return time

    def toString(self, f):
        if int(f) < 1:
            s = str(f + 1)
            temp = s.split('.')
            temp[0] = '0'
            s = temp[0] + '.' + temp[1]
        else:
            s = str(f)
        return s

    def updateTimePerChannel(self):
        try:
            self.time_per_channel_calculation = self.time.value() / self.channels.value()
        except:
            pass
        time_measurement = str(self.time_measurement.currentText())
        self.time_per_channel.setText(str(round(self.time_per_channel_calculation, 2)) + ' ' + time_measurement)

    def getData(self):
        data = "ESL, " + \
               str(self.ee_frequency.value()) + "KHz, " + \
               str(self.ee_voltage.value()) + "V"

        all_ = {
            "id": self.id,
            "excV": self.ee_voltage.value(),
            "excF": self.ee_frequency.value(),
            "time": self.getTime(),
            "time_unit": str(self.time_measurement.currentText()),
            "heating_rate": self.heating_rate.value(),
            "stabilization": self.stabilization.value(),
            "final_temp": self.ee_temp.value(),
            "time_final_temp": self.toString(float(self.getTime()) + self.stabilization.value()),
            "record_during": self.record_during_ee.isChecked(),
            "light_co_stimulation": self.ligh_co_stimulation.isChecked(),
            "date_type": self.date_type,
            "comments": self.comments,
            "timePerChannel": self.time_per_channel_calculation
        }

        if self.record_during_ee.isChecked():
            all_['datapoints2'] = self.channels.value()
            all_['timePerChannel'] = self.time_per_channel_calculation
        if self.ligh_co_stimulation.isChecked():
            all_['light_source'] = str(self.ligth_source.currentText())
            all_['start_optical_power'] = self.optical_power.value()

        return data, all_

    def lightCoStimulationChange(self):
        self.ligth_source.setEnabled(self.ligh_co_stimulation.isChecked())
        self.optical_power.setEnabled(self.ligh_co_stimulation.isChecked())

    def recordDuringEEChange(self):
        self.channels.setEnabled(self.record_during_ee.isChecked())
