#!/usr/bin/python3
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import os
import subprocess
import pickle
from datetime import datetime
from functools import partial

from PyQt5 import QtWidgets, QtCore, QtGui, QtNetwork

from controller.stk.dialogs.about import AboutSTK
from controller.stk.dialogs.open_with import OpenWith
from controller.widgets.custom_row_widget import CustomRowWidget
from controller.stk.dialogs.settings import Settings
from model.handle_config import ConfigHandler
from model.handle_recent_files import RecentFilesHandler
from model.handle_theme import ThemeHandler
from view.stk.ui_stk import Ui_stk
from controller.decorators import loadingCursor


class STK(Ui_stk):
    def __init__(self, appname, dirs=None):
        self.appname = appname
        self.main_window = QtWidgets.QMainWindow()
        self.setupUi(self.main_window)
        self.visit_row_widget = None
        self.row_widgets = []

        self.config_handler = ConfigHandler()
        self.theme_handler = ThemeHandler()
        self.recent_files_handler = RecentFilesHandler()
        self.translator = []

        if self.getConfiguration('pos_x') is None or 'None':
            widget = QtWidgets.QDesktopWidget()
            main_screen_size = widget.availableGeometry(widget.primaryScreen())
            pos_x = (main_screen_size.width() / 2) - (int(self.getConfiguration('width')) / 2)
            pos_y = (main_screen_size.height() / 2) - (int(self.getConfiguration('height')) / 2)

            self.geometryUpdate(
                pos_x,
                pos_y
            )

        self.main_window.setGeometry(QtCore.QRect(
            int(self.getConfiguration('pos_x')),
            int(self.getConfiguration('pos_y')),
            int(self.getConfiguration('width')),
            int(self.getConfiguration('height'))
        ))
        self.main_window.closeEvent = self.quit

        self.push_button_settings.clicked.connect(self.settings)
        self.push_button_about.clicked.connect(self.about)
        self.push_button_help.clicked.connect(self.help)
        self.push_button_open_file.clicked.connect(self.openFile)
        self.push_button_gensec.clicked.connect(self.openWithGenSec)
        self.push_button_genrep.clicked.connect(self.openWithGenRep)
        self.push_button_genvis.clicked.connect(self.openWithGenVis)

        self.setting_watsh = QtNetwork.QLocalServer(self.main_window)
        self.setting_watsh.newConnection.connect(self.settingTrigger)
        self.setting_watsh.listen(os.path.join(self.config_handler.config_path, 'listening', self.appname))

        self.settingsChange()
        self.fillRecentFiles()

    # --------------------------------------------------------------------------------

    def openFile(self):
        dialog = QtWidgets.QFileDialog(
            self.main_window,
            QtCore.QCoreApplication.translate('stk', "Choose a file to open"),
            self.getConfiguration('default_file_location', 'COMMON'),
            QtCore.QCoreApplication.translate('stk', 'File {0}').format(' SLF (*.slf);; ') +
            QtCore.QCoreApplication.translate('stk', 'File {0}').format(' RLF (*.rlf)')
        )
        dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        dialog.setViewMode(QtWidgets.QFileDialog.List)

        action = dialog.exec_()
        if action:
            path = dialog.selectedFiles()[0]
            if path.endswith('.rlf'):
                self.openWithGenVis(path)
            elif path.endswith('.slf'):
                dialog = OpenWith(self.main_window)
                dialog.push_button_gensec.clicked.connect(partial(self.openWithGenSec, path))
                dialog.push_button_genrep.clicked.connect(partial(self.openWithGenRep, path))
                dialog.exec_()

    def openWithGenSec(self, path=None):
        if (path is None) or (path is False):
            path = ''
        command = None
        # if os.sys.platform in ('linux', 'linux2'):
        if os.path.exists('gensec.pyw'):
            command = 'python3 gensec.pyw '
        # elif os.path.exists('GenSec.exe'):
        #     command = 'GenSec.exe '
        if command is not None:
            subprocess.Popen(
                command + path,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE
            )
        else:
            self.showErrorMessage(
                QtCore.QCoreApplication.translate(
                    'main_window',
                    'Unable to launch {0}').format('GenSec')
            )

    def openWithGenRep(self, path=None):
        if (path is None) or (path is False):
            path = ''
        command = None
        # if os.sys.platform in ('linux', 'linux2'):
        if os.path.exists('genrep.pyw'):
            command = 'python3 genrep.pyw '
        # elif os.path.exists('GenRep.exe'):
        #     command = 'GenRep.exe '
        if command is not None:
            subprocess.Popen(
                command + path,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE
            )
        else:
            self.showErrorMessage(
                QtCore.QCoreApplication.translate(
                    'main_window',
                    'Unable to launch {0}').format('GenRep')
            )

    def openWithGenVis(self, path=None):
        if (path is None) or (path is False):
            path = ''
        command = None
        # if os.sys.platform in ('linux', 'linux2'):
        if os.path.exists('genvis.pyw'):
            command = 'python3 genvis.pyw '
        # elif os.path.exists('GenVis.exe'):
        #     command = 'GenVis.exe '
        if command is not None:
            subprocess.Popen(
                command + path,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE
            )
        else:
            self.showErrorMessage(
                QtCore.QCoreApplication.translate(
                    'main_window',
                    'Unable to launch {0}').format('GenVis')
            )

    def showErrorMessage(self, message_text, title=QtCore.QCoreApplication.translate('main_window', 'Error!')):
        self.showMessage('error', title, message_text)

    def showMessage(self, type_, title, message_text):
        message = QtWidgets.QMessageBox(self.main_window)
        message.setIconPixmap(QtGui.QPixmap(':/resources/img/icons/' + type_ + '.svg'))
        message.setWindowTitle(title)
        message.setText(message_text)
        message.setStandardButtons(QtWidgets.QMessageBox.Ok)
        message.exec_()

    def fillRecentFiles(self):
        self.clear()

        today = []
        yesterday = []
        others = []
        description_today = QtCore.QCoreApplication.translate('stk', 'Recent Files') + \
                            QtCore.QCoreApplication.translate('stk', ' (today)')
        description_yesterday = QtCore.QCoreApplication.translate('stk', 'Recent Files') + \
                                QtCore.QCoreApplication.translate('stk', ' (yesterday)')
        description_others = QtCore.QCoreApplication.translate('stk', 'Recent Files') + \
                                QtCore.QCoreApplication.translate('stk', ' (a few days ago)')

        for date_path in self.recent_files_handler.getGlobal():
            if date_path[0].split()[0] == str(datetime.now()).split()[0]:
                today.append(date_path)
            else:
                current_date = date_path[0].split()[0].split('-')
                if int(current_date[0]) == datetime.today().year and \
                        int(current_date[1]) == datetime.today().month and \
                        int(current_date[2]) == datetime.today().day - 1:
                    yesterday.append(date_path)
                else:
                    others.append(date_path)

        components = []
        if today:
            components.append((today, description_today))
        if yesterday:
            components.append((yesterday, description_yesterday))
        if others:
            components.append((others, description_others))

        for i in range(len(components)):
            if components[i][0]:
                description_widget = QtWidgets.QWidget()
                description_layout = QtWidgets.QHBoxLayout(description_widget)
                description_layout.setContentsMargins(6, 20, 6, -1)
                description_layout.setSpacing(8)
                line = QtWidgets.QFrame(self.stk_right_area)
                line.setMinimumSize(QtCore.QSize(20, 0))
                line.setFrameShadow(QtWidgets.QFrame.Plain)
                line.setFrameShape(QtWidgets.QFrame.HLine)
                line.setObjectName("line")
                description_layout.addWidget(line)
                description = QtWidgets.QLabel(self.stk_right_area)
                description.setMinimumSize(QtCore.QSize(0, 30))
                description.setText(components[i][1])
                description_layout.addWidget(description)
                line_2 = QtWidgets.QFrame(self.stk_right_area)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(line_2.sizePolicy().hasHeightForWidth())
                line_2.setSizePolicy(sizePolicy)
                line_2.setFrameShadow(QtWidgets.QFrame.Plain)
                line_2.setFrameShape(QtWidgets.QFrame.HLine)
                line_2.setObjectName("line")
                description_layout.addWidget(line_2)

                self.scroll_area_layout.addWidget(description_widget)

                count = 0
                custom_row_widget = CustomRowWidget(self)
                for date_path in components[i][0]:
                    if count < 4:
                        custom_row_widget.addWidget(date_path)
                        count += 1
                    else:
                        self.scroll_area_layout.addWidget(custom_row_widget)
                        self.row_widgets.append(custom_row_widget)
                        count = 0
                        custom_row_widget = CustomRowWidget(self)
                if count > 0:
                    self.scroll_area_layout.addWidget(custom_row_widget)
                    if count < 4:
                        custom_row_widget.addSpacer()
                self.row_widgets.append(custom_row_widget)

        vertical_spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.scroll_area_layout.addItem(vertical_spacer)

    def clear(self):
        self.scroll_area.takeWidget()

        self.scroll_area_contents = QtWidgets.QWidget()
        self.scroll_area_contents.setGeometry(QtCore.QRect(0, 0, 687, 1322))
        self.scroll_area_contents.setObjectName("scroll_area_contents")
        self.scroll_area_layout = QtWidgets.QVBoxLayout(self.scroll_area_contents)
        self.scroll_area_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area_layout.setSpacing(0)
        self.scroll_area_layout.setObjectName("scroll_area_layout")
        self.scroll_area.setWidget(self.scroll_area_contents)


    def settings(self):
        dialog = Settings(self.main_window)
        dialog.exec_()

    def about(self):
        dialog = AboutSTK(self.main_window)
        dialog.exec_()

    def help(self):
        subprocess.Popen('python3 assistant.pyw stk', shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, stdin=subprocess.PIPE)

    def settingTrigger(self):
        if self.setting_watsh.hasPendingConnections():
            self.setting_watsh.nextPendingConnection()
        self.recent_files_handler.load()
        self.settingsChange()
        self.fillRecentFiles()

    @loadingCursor()
    def settingsChange(self):
        self.config_handler.load()

        lang = self.getConfiguration('lang', 'GLOBALS')
        theme = self.getConfiguration('theme', 'GLOBALS')
        skin = self.getConfiguration('skin', 'GLOBALS')

        opacity = self.getConfiguration('opacity', 'COMMON')
        font_style = self.getConfiguration('font-style', 'COMMON')

        font = [
            self.getConfiguration('font-family', 'COMMON'),
            self.getConfiguration('font-size', 'COMMON'),
            'normal',
            'normal',
        ]

        if font_style == 'Bold':
            font[3] = 'bold'
        elif font_style == 'Light':
            font[3] = '100'
        elif font_style == 'Book':
            font[3] = '300'
        elif font_style == 'Oblique':
            font[2] = 'oblique'

        qapp = QtCore.QCoreApplication.instance()

        self.theme_handler.load(theme, skin, font)
        qapp.setStyleSheet(self.theme_handler.theme)
        self.setConfiguration('widget_color', self.theme_handler.skin_keys['widget_color'], 'COMMON')
        self.setConfiguration('tree_widget_item_background',
                              self.theme_handler.skin_keys['tree_widget_item_background'], 'COMMON')
        self.setConfiguration('tree_widget_item_alternate_background',
                              self.theme_handler.skin_keys['tree_widget_item_alternate_background'], 'COMMON')
        self.main_window.setWindowOpacity(opacity)

        if self.translator:
            for translator in self.translator:
                QtCore.QCoreApplication.instance().removeTranslator(translator)
            self.translator = []
        if (not lang) or (lang is None) or (lang == 'locale') or (lang == 'None'):
            lang = QtCore.QLocale.system().name()

        translator = QtCore.QTranslator()
        if translator.load("resources/i18n/i18n_gensec." + lang):
            qapp.installTranslator(translator)
            self.translator.append(translator)

        stk_translator = QtCore.QTranslator()
        if stk_translator.load("resources/i18n/i18n_stk." + lang):
            qapp.installTranslator(stk_translator)
            self.translator.append(stk_translator)

        qt_translator = QtCore.QTranslator()
        if qt_translator.load("resources/i18n/i18n_qt." + lang):
            qapp.installTranslator(qt_translator)
            self.translator.append(qt_translator)

        qtbase_translator = QtCore.QTranslator()
        if qtbase_translator.load("resources/i18n/i18n_qtbase." + lang):
            qapp.installTranslator(qtbase_translator)
            self.translator.append(qtbase_translator)

        self.retranslateUi(self.main_window)

        self.statusbar.showMessage(
            QtCore.QCoreApplication.translate('stk',
                                              'New settings has been applied.'),
            3000
        )

    def quit(self, event):
        self.geometryUpdate(
            self.main_window.pos().x(),
            self.main_window.pos().y(),
            self.main_window.width(),
            self.main_window.height()
        )
        self.setConfiguration('running_state', 0)
        os.remove(os.path.join(self.config_handler.config_path, 'listening', self.appname))
        os.remove(os.path.join(self.config_handler.config_path, 'share_memory', self.appname))
        return event.accept()

    def geometryUpdate(self, pos_x, pos_y, width=None, height=None):
        self.setConfiguration('pos_x', pos_x)
        self.setConfiguration('pos_y', pos_y)
        if (width is not None) and (height is not None):
            self.setConfiguration('width', width)
            self.setConfiguration('height', height)

    def getConfiguration(self, key, file='STK'):
        return self.config_handler.configurations[file][key]

    def setConfiguration(self, key, value, file='STK'):
        self.config_handler.configurations[file][key] = value
        self.config_handler.save(file)
