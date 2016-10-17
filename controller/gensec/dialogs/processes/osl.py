#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from functools import partial

from PyQt5 import QtWidgets, QtCore

from controller.gensec.dialogs.processes.information import Information
from view.dialogs.base_dialog import BaseDialog
from view.gensec.dialogs.processes.ui_osl import Ui_process


class OSL(BaseDialog, Ui_process):
    def __init__(self, process_data=False, parent=None):
        BaseDialog.__init__(self, parent)
        self.setupUi(self)

        self.id = 3
        self.date_type = ''
        self.comments = ''
        self.channels_calculation = 0
        self.time_per_channel_calculation = 0
        self.information_dialog = None

        self.push_button_accept.clicked.connect(self.accept)
        self.push_button_cancel.clicked.connect(self.close)
        self.push_button_information.clicked.connect(self.showInformationDialog)
        self.before_stimulation.valueChanged.connect(partial(self.dataPointsValidator, 1))
        self.during_stimulation.valueChanged.connect(partial(self.dataPointsValidator, 2))
        self.after_stimulation.valueChanged.connect(partial(self.dataPointsValidator, 3))
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
            self.before_stimulation.setValue(process_data["datapoints1"])
            self.during_stimulation.setValue(process_data["datapoints2"])
            self.after_stimulation.setValue(process_data["datapoints3"])

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
            self.channels_calculation = process_data["channels"]
            self.date_type = process_data["date_type"]
            self.comments = process_data["comments"]

            self.updateTimePerChannel()
            self.dataPointsValidator(None)

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
            self.time_per_channel_calculation = self.time.value() / self.channels_calculation
        except:
            pass
        time_measurement = str(self.time_measurement.currentText())
        self.time_per_channel.setText(str(round(self.time_per_channel_calculation, 2)) + ' ' + time_measurement)

    def dataPointsValidator(self, button):
        before = self.before_stimulation.value()
        during = self.during_stimulation.value()
        after = self.after_stimulation.value()

        if (before + during + after) > 512:
            if button == 1:
                self.before_stimulation.setValue(before - 1)
            elif button == 2:
                self.during_stimulation.setValue(during - 1)
            else:
                self.after_stimulation.setValue(after - 1)
        else:
            self.channels_calculation = before + during + after
            self.channels.setText(str(self.channels_calculation))
            self.updateTimePerChannel()

    def getData(self):
        data = "OSL, " + \
               str(self.ligth_source.currentText()) + ", " + \
               str(self.start_optical_power.value()) + "%"

        all_ = {
            "id": self.id,
            "light_source": str(self.ligth_source.currentText()),
            "start_optical_power": self.start_optical_power.value(),
            "time": self.getTime(),
            "time_unit": str(self.time_measurement.currentText()),
            "datapoints1": self.before_stimulation.value(),
            "datapoints2": self.during_stimulation.value(),
            "datapoints3": self.after_stimulation.value(),
            "final_temp": self.final_temperature.value(),
            "time_final_temp": self.toString(float(self.getTime()) + self.stabilization.value()),
            "heating_rate": self.heating_rate.value(),
            "stabilization": self.stabilization.value(),
            "date_type": self.date_type,
            "comments": self.comments,
            "channels": self.channels_calculation,
            "timePerChannel": self.time_per_channel_calculation
        }

        return data, all_

