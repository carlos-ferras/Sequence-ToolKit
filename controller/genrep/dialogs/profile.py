#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import os
from PyQt5 import QtWidgets, QtCore
import pickle
from datetime import datetime

from model.handle_config import ConfigHandler
from view.genrep.dialogs.ui_profile import Ui_profile
from view.dialogs.base_dialog import BaseDialog


class Profile(BaseDialog, Ui_profile):
    def __init__(self, profile_parameters, parent=None):
        BaseDialog.__init__(self, parent)
        self.setupUi(self)

        self.config_handler = ConfigHandler()

        self.push_button_accept.clicked.connect(self.accept)
        self.push_button_cancel.clicked.connect(self.close)
        self.push_button_save.clicked.connect(self.save)
        self.push_button_load.clicked.connect(self.load)
        self.all_parameters.clicked.connect(self.selectUnselectAll)

        self.populate(profile_parameters)

        self.parameters_list.itemClicked.connect(self.checkAll)
        self.accepted.connect(self.saveData)

    def populate(self, profile_parameters):
        for parameter in profile_parameters:
            item = QtWidgets.QListWidgetItem()
            item.setText(parameter)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.parameters_list.addItem(item)
        self.fillValues()
        self.checkAll()

    def selectUnselectAll(self):
        for row in range(self.parameters_list.count()):
            item = self.parameters_list.item(row)
            item.setCheckState(self.all_parameters.checkState())

    def checkAll(self):
        checked = True
        for row in range(self.parameters_list.count()):
            item = self.parameters_list.item(row)
            if not item.checkState():
                checked = False
                break
        self.all_parameters.setChecked(checked)

    def fillValues(self, values=None):
        if values is None:
            values = self.getConfiguration('parameters', 'GENREP')
        for row in range(self.parameters_list.count()):
            if row in values:
                item = self.parameters_list.item(row)
                item.setCheckState(2)

    def saveData(self):
        self.setConfiguration('parameters', self.getData(), 'GENREP')

    def getData(self):
        data = []
        for row in range(self.parameters_list.count()):
            item = self.parameters_list.item(row)
            if item.checkState():
                data.append(row)
        return tuple(data)

    def save(self):
        path, selected_filter = QtWidgets.QFileDialog.getSaveFileName(
            self,
            QtCore.QCoreApplication.translate('association', "Save as..."),
            os.path.join(self.getConfiguration('default_file_location', 'COMMON'), str(datetime.now()) + '.pstk'),
            QtCore.QCoreApplication.translate(
                'association', 'File {0}').format(' AP (*.pstk)')
        )
        if path:
            if not path.endswith('.pstk'):
                path += '.pstk'
            file_ = open(path, 'wb')
            file_.write(pickle.dumps(
                self.getData(),
            ))
            file_.close()

    def load(self):
        dialog = QtWidgets.QFileDialog(
            self,
            QtCore.QCoreApplication.translate('association', "Choose a files to open"),
            self.getConfiguration('default_file_location', 'COMMON'),
            QtCore.QCoreApplication.translate('association', 'File {0} ').format('AP (*.pstk)')
        )
        dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        dialog.setViewMode(QtWidgets.QFileDialog.List)
        action = dialog.exec_()

        if action:
            path = dialog.selectedFiles()[0]
            if os.path.exists(path) and path.endswith('.pstk'):
                with open(path, 'rb') as file_:
                    data = pickle.load(file_)
                    self.fillValues(data)

    def getConfiguration(self, key, file):
        return self.config_handler.configurations[file][key]

    def setConfiguration(self, key, value, file):
        self.config_handler.configurations[file][key] = value
        self.config_handler.save(file)
