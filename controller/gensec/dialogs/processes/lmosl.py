#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from PyQt5 import QtWidgets, QtCore

from controller.gensec.dialogs.processes.information import Information
from view.dialogs.base_dialog import BaseDialog
from view.gensec.dialogs.processes.ui_lmosl import Ui_process


class LMOSL(BaseDialog, Ui_process):
    def __init__(self, process_data=False, parent=None):
        BaseDialog.__init__(self, parent)
        self.setupUi(self)

        self.id = 5
        self.date_type = ''
        self.comments = ''
        self.time_per_channel_calculation = 0
        self.information_dialog = None

        self.push_button_accept.clicked.connect(self.accept)
        self.push_button_cancel.clicked.connect(self.close)
        self.push_button_information.clicked.connect(self.showInformationDialog)
        self.channels.valueChanged.connect(self.updateTimePerChannel)
        self.time.valueChanged.connect(self.updateTimePerChannel)
        self.time_measurement.currentIndexChanged.connect(self.updateTimePerChannel)

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
            self.final_temperature.setValue(process_data["final_temp"])
            self.time.setValue(self.convertTime(process_data["time"], process_data["time_unit"]))
            self.start_optical_power.setValue(process_data["start_optical_power"])
            self.end_optical_power.setValue(process_data["end_optical_power"])
            self.channels.setValue(process_data["datapoints2"])

            time_measurements = {
                'ms': 0,
                's': 1,
                'us': 2
            }
            self.time_measurement.setCurrentIndex(time_measurements[process_data["time_unit"]])

            light_source = {
                'Blue': 0,
                'IR': 1,
                'AUX': 2,
            }
            self.ligth_source.setCurrentIndex(light_source[process_data["light_source"]])

            self.time_per_channel_calculation = process_data["timePerChannel"]
            self.date_type = process_data["date_type"]
            self.comments = process_data["comments"]

            self.updateTimePerChannel()

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
        data = "LMOSL, " + \
               str(self.ligth_source.currentText()) + ", " + \
               str(self.end_optical_power.value()) + "%"

        all_ = {
            "id": self.id,
            "light_source": str(self.ligth_source.currentText()),
            "datapoints2": self.channels.value(),
            "time": self.getTime(),
            "time_unit": str(self.time_measurement.currentText()),
            "start_optical_power": self.start_optical_power.value(),
            "end_optical_power": self.end_optical_power.value(),
            "final_temp": self.final_temperature.value(),
            "time_final_temp": self.toString(float(self.getTime()) + self.stabilization.value()),
            "heating_rate": self.heating_rate.value(),
            "stabilization": self.stabilization.value(),
            "date_type": self.date_type,
            "comments": self.comments,
            "timePerChannel": self.time_per_channel_calculation
        }

        return data, all_
