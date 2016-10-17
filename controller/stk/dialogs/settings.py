#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import os
from functools import partial

from PyQt5 import QtWidgets, QtCore, QtNetwork

from model.handle_config import ConfigHandler
from view.dialogs.base_dialog import BaseDialog
from view.stk.dialogs.ui_settings import Ui_settings


class Settings(BaseDialog, Ui_settings):
    def __init__(self, parent=None):
        BaseDialog.__init__(self, parent)
        self.setupUi(self)

        self.config_handler = ConfigHandler()

        self.push_button_accept.clicked.connect(self.accept)
        self.push_button_cancel.clicked.connect(self.close)
        self.opacity.valueChanged.connect(self.opacityChange)
        self.opacity_spinbox.valueChanged.connect(partial(self.opacityChange, False))
        self.font_family.currentIndexChanged.connect(self.fontChange)
        self.font_style.currentIndexChanged.connect(self.fontChange)
        self.font_size.valueChanged.connect(self.fontChange)
        self.location_explorer.clicked.connect(self.fileSystemExplore)
        self.accepted.connect(self.saveData)

        self.fillLanguages()
        self.fillThemes()
        self.fillSkins()
        self.fillValues()

    def fillLanguages(self):
        self.language.addItem("local")
        self.language.addItem("en")
        for path in os.listdir('resources/i18n/'):
            lang = os.path.splitext(os.path.basename(path))[0]
            if lang.startswith('i18n'):
                lang = os.path.splitext(lang)[-1][1:]
                if self.language.findText(lang) == -1:
                    self.language.addItem(lang)

    def fillThemes(self):
        for path in os.listdir('resources/theme/'):
            self.theme.addItem(os.path.basename(path))

    def fillSkins(self):
        for path in os.listdir('resources/skin/'):
            self.skin.addItem(os.path.basename(path))

    def fillValues(self):
        self.language.setCurrentText(self.getConfiguration('lang', 'GLOBALS'))
        self.theme.setCurrentText(self.getConfiguration('theme', 'GLOBALS'))
        self.skin.setCurrentText(self.getConfiguration('skin', 'GLOBALS'))
        self.location.setText(self.getConfiguration('default_file_location', 'COMMON'))
        self.opacity.setValue(self.getConfiguration('opacity', 'COMMON') * 100)
        self.opacity_spinbox.setValue(self.getConfiguration('opacity', 'COMMON'))

        self.font_family.setCurrentText(self.getConfiguration('font-family', 'COMMON'))
        self.font_size.setValue(self.getConfiguration('font-size', 'COMMON'))
        self.font_style.setCurrentText(self.getConfiguration('font-style', 'COMMON'))

    def fileSystemExplore(self):
        dialog = QtWidgets.QFileDialog(
            self,
            QtCore.QCoreApplication.translate('settings', "Choose a Directory"),
            self.location.text()
        )
        dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        dialog.setViewMode(QtWidgets.QFileDialog.List)
        dialog.setOption(QtWidgets.QFileDialog.ShowDirsOnly, True)

        action = dialog.exec_()
        if action:
            location = dialog.selectedFiles()[0]
            self.location.setText(location)

    def opacityChange(self, slider=True):
        if slider:
            self.opacity_spinbox.setValue(self.opacity.value()/100)
        else:
            self.opacity.setValue(self.opacity_spinbox.value() * 100)

    def fontChange(self):
        font = [
            self.font_family.currentText(),
            str(self.font_size.value()),
            'normal',
            'normal',
        ]

        if self.font_style.currentIndex() == 3:
            font[3] = 'bold'
        elif self.font_style.currentIndex() == 1:
            font[3] = '100'
        elif self.font_style.currentIndex() == 2:
            font[3] = '300'
        if self.font_style.currentIndex() == 4:
            font[2] = 'oblique'

        self.font_testing.setStyleSheet(
            "font-family: " + font[0] + ";font-size: " + font[1] +
            "px;font-style: " + font[2] + ";font-weight: " + font[3] + ";"
        )

        if self.font_size.value() > 12:
            self.font_testing.setMinimumHeight(int(self.font_size.value() * 2.3333))
        else:
            self.font_testing.setMinimumHeight(28)

    def saveData(self):
        self.setConfiguration('lang', self.language.currentText(), 'GLOBALS')
        self.setConfiguration('theme', self.theme.currentText(), 'GLOBALS')
        self.setConfiguration('skin', self.skin.currentText(), 'GLOBALS')
        self.setConfiguration('default_file_location', self.location.text(), 'COMMON')
        self.setConfiguration('opacity', self.opacity_spinbox.value(), 'COMMON')

        self.setConfiguration('font-family', self.font_family.currentText(), 'COMMON')
        self.setConfiguration('font-size', self.font_size.value(), 'COMMON')
        self.setConfiguration('font-style', self.font_style.currentText(), 'COMMON')

        for path,_,files in os.walk(os.path.join(self.config_handler.config_path, 'listening')):
            for file_ in files:
                socket = QtNetwork.QLocalSocket(self)
                socket.connectToServer(os.path.join(path, file_), QtCore.QIODevice.WriteOnly)
                if not socket.waitForConnected(1000):
                    raise Exception(str(socket.errorString()))
                socket.write(b'change')
                if not socket.waitForBytesWritten(1000):
                    raise Exception(str(socket.errorString()))
                socket.disconnectFromServer()

    def getConfiguration(self, key, file):
        return self.config_handler.configurations[file][key]

    def setConfiguration(self, key, value, file):
        self.config_handler.configurations[file][key] = value
        self.config_handler.save(file)
