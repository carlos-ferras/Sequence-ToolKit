#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from PyQt5 import QtWidgets, QtCore

from controller.gensec.dialogs.processes.information import Information
from view.dialogs.base_dialog import BaseDialog
from view.gensec.dialogs.processes.ui_irradiation import Ui_process


class Irradiation(BaseDialog, Ui_process):
    def __init__(self, process_data=False, parent=None):
        BaseDialog.__init__(self, parent)
        self.setupUi(self)

        self.id = 1
        self.date_type = ''
        self.comments = ''
        self.dose_rate = self.parent().parent().dose_rate
        self.external_dose_rate = self.parent().parent().external_dose_rate
        self.dose_rate_to_use = self.parent().parent().dose_rate
        self.information_dialog = None

        self.push_button_accept.clicked.connect(self.accept)
        self.push_button_cancel.clicked.connect(self.close)
        self.push_button_information.clicked.connect(self.showInformationDialog)
        self.irradiation_source.currentIndexChanged.connect(self.sourceChange)
        self.time.valueChanged.connect(self.setDose)

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
            if process_data["source"] == 'Beta':
                source = 0
            else:
                source = 1
            self.irradiation_source.setCurrentIndex(source)
            self.time.setValue(process_data["time"])
            self.final_temperature.setValue(process_data["final_temp"])
            self.stabilization.setValue(process_data["stabilization"])
            self.heating_rate.setValue(process_data["heating_rate"])
            self.date_type = process_data["date_type"]
            self.comments = process_data["comments"]
            self.setDose()
            self.sourceChange()

    def showInformationDialog(self):
        self.information_dialog = Information(self.date_type, self.comments, self)
        self.information_dialog.accepted.connect(self.informationAccepted)
        self.information_dialog.exec_()

    def informationAccepted(self):
        self.date_type, self.comments = self.information_dialog.getData()
        self.information_dialog.close()

    def setDose(self, dose=''):
        if dose:
            self.dose.setText(str(dose))
        else:
            self.dose.setText(str(self.time.value() * self.dose_rate_to_use))

    def sourceChange(self):
        if self.irradiation_source.currentIndex():
            self.id = 0

            self.heating_rate.setHidden(True)
            self.final_temperature.setHidden(True)
            self.stabilization.setHidden(True)
            self.heating_rate_label.setHidden(True)
            self.final_temperature_label.setHidden(True)
            self.stabilization_label.setHidden(True)
            self.line_2.setHidden(True)

            self.form_area.adjustSize()
            self.adjustSize()

            self.dose_rate_to_use = self.external_dose_rate
        else:
            self.id = 1

            self.heating_rate.setHidden(False)
            self.final_temperature.setHidden(False)
            self.stabilization.setHidden(False)
            self.heating_rate_label.setHidden(False)
            self.final_temperature_label.setHidden(False)
            self.stabilization_label.setHidden(False)
            self.line_2.setHidden(False)

            self.dose_rate_to_use = self.dose_rate
        self.setDose()

    def getData(self):
        all_ = {
            "id": self.id,
            "source": str(self.irradiation_source.currentText()),
            "time": self.time.value(),
            "final_temp": self.final_temperature.value(),
            "time_final_temp": self.time.value() + self.stabilization.value(),
            "stabilization": self.stabilization.value(),
            "heating_rate": self.heating_rate.value(),
            "doserate": self.dose.text(),
            "date_type": self.date_type,
            "comments": self.comments
        }

        if self.id == 1:
            data = 'Beta Irradiation, ' + \
                   str(self.time.value()) + "s"
        else:
            data = 'External Irradiation, ' + \
                   str(self.time.value() * float(self.dose.text())) + "Gy"

            all_['heating_rate'] = 0
            all_['stabilization'] = 0
            all_['final_temp'] = 0

        return data, all_
