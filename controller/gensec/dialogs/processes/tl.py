#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from PyQt5 import QtWidgets, QtCore

from controller.gensec.dialogs.processes.information import Information
from view.dialogs.base_dialog import BaseDialog
from view.gensec.dialogs.processes.ui_tl import Ui_process


class TL(BaseDialog, Ui_process):
    def __init__(self, process_data=False, parent=None):
        BaseDialog.__init__(self, parent)
        self.setupUi(self)

        self.id = 2
        self.date_type = ''
        self.comments = ''
        self.information_dialog = None

        self.push_button_accept.clicked.connect(self.accept)
        self.push_button_cancel.clicked.connect(self.close)
        self.push_button_info.clicked.connect(self.showInformationDialog)

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
            self.heating_rate.setValue(float(process_data["heating_rate"]))
            self.time_at_final_temp.setValue(float(process_data["time_final_temp"]))
            self.final_temperature.setValue(int(process_data["final_temp"]))
            self.channels.setValue(float(process_data["datapoints2"]))
            self.date_type = process_data["date_type"]
            self.comments = process_data["comments"]
            self.save_temp.setChecked(process_data["save_temp"])

    def showInformationDialog(self):
        self.information_dialog = Information(self.date_type, self.comments, self)
        self.information_dialog.accepted.connect(self.informationAccepted)
        self.information_dialog.exec_()

    def informationAccepted(self):
        self.date_type, self.comments = self.information_dialog.getData()
        self.information_dialog.close()

    def getData(self):
        data = "TL, " + \
               str(self.final_temperature.value()) + "°C , " + \
               str(self.heating_rate.value()) + "°C/s"

        all_ = {
            "id": self.id,
            "heating_rate": self.heating_rate.value(),
            "time_final_temp": self.time_at_final_temp.value(),
            "final_temp": self.final_temperature.value(),
            "datapoints2": self.channels.value(),
            "date_type": self.date_type,
            "comments": self.comments,
            "save_temp": self.save_temp.isChecked(),
            "timePerChannel": self.final_temperature.value()/self.heating_rate.value() + self.time_at_final_temp.value()
        }

        return data, all_
