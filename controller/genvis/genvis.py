#!/usr/bin/python3
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import os
import subprocess
from functools import partial

from PyQt5 import QtWidgets, QtCore, QtGui, QtNetwork

from controller.genvis.dialogs.about import AboutGenVis
from controller.genvis.genvis_tab import GenVisTab
from controller.stk.dialogs.about import AboutSTK
from controller.stk.dialogs.settings import Settings
from model.handle_config import ConfigHandler
from model.handle_recent_files import RecentFilesHandler
from model.handle_theme import ThemeHandler
from view.genvis.ui_genvis import Ui_main_window
from controller.decorators import loadingCursor


class GenVis(Ui_main_window):
    def __init__(self, appname, dirs=None):
        self.appname = appname
        self.main_window = QtWidgets.QMainWindow()
        self.setupUi(self.main_window)


        self.theme_handler = ThemeHandler()
        self.config_handler = ConfigHandler()
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

        self.action_undo.setEnabled(False)
        self.action_redo.setEnabled(False)

        # file
        self.action_new.triggered.connect(self.new)
        self.action_open.triggered.connect(self.openRLF)
        self.action_save.triggered.connect(self.save)
        self.action_save_as.triggered.connect(self.saveAs)
        self.action_save_all.triggered.connect(self.saveAll)
        self.action_print.triggered.connect(self.print)
        self.main_window.setAcceptDrops(True)
        self.main_window.dropEvent = self.onDrop
        self.main_window.dragEnterEvent = self.onDrag
        self.main_window.dragMoveEvent = self.onDrag

        # open dialog
        self.action_settings.triggered.connect(self.settings)
        self.action_help.triggered.connect(self.help)
        self.action_about_genvis.triggered.connect(self.aboutGenVis)
        self.action_about.triggered.connect(self.aboutSTK)

        # edit
        self.action_undo.triggered.connect(partial(self.execInCurrentTab, 'undo'))
        self.action_redo.triggered.connect(partial(self.execInCurrentTab, 'redo'))
        # self.action_cut.triggered.connect(partial(self.execInCurrentTab, 'cut'))
        # self.action_copy.triggered.connect(partial(self.execInCurrentTab, 'copy'))
        # self.action_paste.triggered.connect(partial(self.execInCurrentTab, 'paste'))
        # self.action_delete.triggered.connect(partial(self.execInCurrentTab, 'delete'))
        # self.action_clear_all.triggered.connect(self.clearAll)

        # close events
        self.action_close.triggered.connect(self.closeTab)
        self.tab_widget.tabCloseRequested.connect(self.closeTab)
        self.action_quit.triggered.connect(self.main_window.close)
        self.main_window.closeEvent = self.quit

        self.tab_widget.currentChanged.connect(self.tabContentChanged)
        self.recent_files_handler.signals.recent_file_added.connect(self.fillRecentFiles)

        self.action_exec_gensec.triggered.connect(self.execGenSec)
        self.action_exec_genrep.triggered.connect(self.execGenRep)

        self.setting_watsh = QtNetwork.QLocalServer(self.main_window)
        self.setting_watsh.newConnection.connect(self.settingTrigger)
        self.setting_watsh.listen(os.path.join(self.config_handler.config_path, 'listening', self.appname))

        self.settingsChange()

        if dirs and dirs is not None:
            self.openRLF(dirs)
        else:
            self.new()

        self.fillRecentFiles(True)

    # --------------------------------------------------------------------------------

    def execGenSec(self):
        command = None
        # if os.sys.platform in ('linux', 'linux2'):
        if os.path.exists('gensec.pyw'):
            command = 'python3 gensec.pyw '
        # elif os.path.exists('GenSec.exe'):
        #     command = 'GenSec.exe '
        if command is not None:
            subprocess.Popen(
                command,
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

    def execGenRep(self):
        command = None
        # if os.sys.platform in ('linux', 'linux2'):
        if os.path.exists('genrep.pyw'):
            command = 'python3 genrep.pyw '
        # elif os.path.exists('GenRep.exe'):
        #     command = 'GenRep.exe '
        if command is not None:
            subprocess.Popen(
                command,
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

    def onDrag(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def onDrop(self, event):
        paths = []
        path_list = event.mimeData().text().split('\r\n')
        for path in path_list:
            path = os.path.normpath(path).split(':')[-1]
            if path and path != '.':
                paths.append(path)
        self.openRLF(paths)

    @loadingCursor()
    def new(self, path=False):
        current_tab = GenVisTab(self.main_window)
        current_tab.document_changed.connect(self.tabChanged)
        current_tab.document_saved.connect(self.tabSaved)
        current_tab.show_success_message.connect(self.showSuccessMessage)
        current_tab.show_info_message.connect(self.showInfoMessage)
        current_tab.show_error_message.connect(self.showErrorMessage)

        if path:
            current_tab.open(path)
            title = path
            self.statusbar.showMessage(
                QtCore.QCoreApplication.translate('main_window',
                                                  '"{0}" is ready to use.').format(path),
                3000
            )
        else:
            title = QtCore.QCoreApplication.translate('main_window', 'Untitled')
            path = QtCore.QCoreApplication.translate('main_window', 'Untitled')
            self.statusbar.showMessage(
                QtCore.QCoreApplication.translate('main_window',
                                                  'New document is ready.'),
                3000
            )
        if len(path) > 10:
            title = os.path.basename(path)
        index = self.tab_widget.addTab(current_tab, str(self.tab_widget.count() + 1) + '. ' + title)
        self.tab_widget.setTabToolTip(index, path)
        self.tab_widget.setCurrentIndex(index)
        return index

    def openInCurrent(self, path):
        self.tab_widget.currentWidget().open(path)
        title = str(self.tab_widget.currentIndex() + 1) + '. '

        if len(path) > 10:
            title += os.path.basename(path)
        else:
            title += path
        self.tab_widget.setTabText(self.tab_widget.currentIndex(), title)
        self.tab_widget.setTabToolTip(self.tab_widget.currentIndex(), path)

    def openRLF(self, paths=False):
        if not paths:
            dialog = QtWidgets.QFileDialog(
                self.main_window,
                QtCore.QCoreApplication.translate('main_window', "Choose one or more files to open"),
                self.getConfiguration('default_file_location', 'COMMON'),
                QtCore.QCoreApplication.translate('main_window', 'File {0}').format(' RLF (*.rlf)')
            )
            dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
            dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
            dialog.setViewMode(QtWidgets.QFileDialog.List)

            action = dialog.exec_()
            paths = []
            if action:
                paths = dialog.selectedFiles()

        for path in paths:
            if os.path.exists(path) and os.path.isfile(path):
                if os.path.splitext(path)[-1] == '.rlf':
                    is_open = False
                    for i in range(self.tab_widget.count()):
                        if self.tab_widget.tabToolTip(i) == str(path):
                            self.tab_widget.setCurrentIndex(i)
                            is_open = True
                    if not is_open:
                        self.recent_files_handler.appendPath(path, 'GENVIS')
                        if (self.tab_widget.currentWidget() is not None) and self.tab_widget.currentWidget().isEmpty():
                            self.openInCurrent(path)
                        else:
                            self.new(path)
                else:
                    self.showErrorMessage(
                        QtCore.QCoreApplication.translate('main_window',
                                                          'The file "{0}" is not valid, must be an rlf.').format(path))
            else:
                self.showErrorMessage(
                    QtCore.QCoreApplication.translate('main_window', 'The file "{0}" does not exist.').format(path))
        if self.tab_widget.count() == 0:
            self.new()

    def save(self, index=None):
        pass

    def saveAs(self):
        pass

    def saveAll(self):
        for index in range(self.tab_widget.count()):
            self.save(index)
        self.statusbar.showMessage(
            QtCore.QCoreApplication.translate('main_window',
                                              'All sequences has been saved.'),
            3000
        )

    def print(self):
        self.statusbar.showMessage(
            QtCore.QCoreApplication.translate('main_window', 'Preparing for print.'),
        )
        self.tab_widget.widget(self.tab_widget.currentIndex()).print()
        self.statusbar.showMessage(
            QtCore.QCoreApplication.translate('main_window',
                                              'Table view has been printed.'),
            3000
        )

    # --------------------------------------------------------------------------------

    def settings(self):
        dialog = Settings(self.main_window)
        #dialog.accepted.connect(self.settingsChange)
        dialog.exec_()

    def help(self):
        subprocess.Popen('python3 assistant.pyw genvis', shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, stdin=subprocess.PIPE)

    def aboutGenVis(self):
        dialog = AboutGenVis(self.main_window)
        dialog.exec_()

    def aboutSTK(self):
        dialog = AboutSTK(self.main_window)
        dialog.exec_()

    # --------------------------------------------------------------------------------

    def showSuccessMessage(self, message_text,
                           title=QtCore.QCoreApplication.translate('main_window', 'Successfully!')):
        self.showMessage('success', title, message_text)

    def showInfoMessage(self, message_text, title=QtCore.QCoreApplication.translate('main_window', 'Information')):
        self.showMessage('information', title, message_text)

    def showErrorMessage(self, message_text, title=QtCore.QCoreApplication.translate('main_window', 'Error!')):
        self.showMessage('error', title, message_text)

    def showWarningMessage(self, message_text, title=QtCore.QCoreApplication.translate('main_window', 'Warning!')):
        message = QtWidgets.QMessageBox(self.main_window)
        message.setIconPixmap(QtGui.QPixmap(':/resources/img/icons/warning.svg'))
        message.setWindowTitle(title)
        message.setText(message_text)
        message.addButton(QtWidgets.QApplication.translate('main_window', 'Discard'),
                          QtWidgets.QMessageBox.RejectRole)
        message.addButton(QtWidgets.QApplication.translate('main_window', 'Continue'),
                          QtWidgets.QMessageBox.AcceptRole)
        return message.exec_()

    def showQuestionMessage(self, message_text,
                            title=QtCore.QCoreApplication.translate('main_window', 'Attention!')):
        message = QtWidgets.QMessageBox(self.main_window)
        message.setIconPixmap(QtGui.QPixmap(':/resources/img/icons/question.svg'))
        message.setWindowTitle(title)
        message.setText(message_text)
        message.addButton(QtWidgets.QMessageBox.Cancel)
        message.addButton(QtWidgets.QMessageBox.Yes)
        message.addButton(QtWidgets.QMessageBox.No)
        return message.exec_()

    def showMessage(self, type_, title, message_text):
        message = QtWidgets.QMessageBox(self.main_window)
        message.setIconPixmap(QtGui.QPixmap(':/resources/img/icons/' + type_ + '.svg'))
        message.setWindowTitle(title)
        message.setText(message_text)
        message.setStandardButtons(QtWidgets.QMessageBox.Ok)
        message.exec_()

    def fillRecentFiles(self, initial=False):
        self.menu_recent_files.clear()

        if not self.recent_files_handler.recent_files['GENVIS']:
            self.menu_recent_files.setEnabled(False)
        else:
            self.menu_recent_files.setEnabled(True)
        for date_path in self.recent_files_handler.recent_files['GENVIS']:
            self.setRecentFile(date_path)

        if not initial:
            socket = QtNetwork.QLocalSocket(self.main_window)
            socket.connectToServer(
                os.path.join(self.config_handler.config_path, 'listening', 'STK'),
                QtCore.QIODevice.WriteOnly
            )
            if socket.state() == QtNetwork.QLocalSocket.ConnectedState:
                if not socket.waitForConnected(1000):
                    raise Exception(str(socket.errorString()))
                socket.write(b'refresh_recent_files')
                if not socket.waitForBytesWritten(1000):
                    raise Exception(str(socket.errorString()))
            socket.disconnectFromServer()

    def setRecentFile(self, date_path):
        action_file = QtWidgets.QAction(self.main_window)
        action_file.setStatusTip(date_path[0])
        action_file.setText(date_path[1])
        action_file.triggered.connect(partial(self.openRLF, [date_path[1]]))
        self.menu_recent_files.addAction(action_file)

    def tabChanged(self, widget=None):
        if (widget is None) or (widget is False):
            index = self.tab_widget.currentIndex()
        else:
            index = self.tab_widget.indexOf(widget)
        title = self.tab_widget.tabText(index)
        if not title.endswith('*'):
            title += '*'
        self.tab_widget.setTabText(index, title)
        if self.tab_widget.widget(index) is not None:
            self.tab_widget.widget(index).is_saved = False
            if index == self.tab_widget.currentIndex():
                self.action_save.setEnabled(True)

    def tabSaved(self, widget=None):
        if (widget is None) or (widget is False):
            index = self.tab_widget.currentIndex()
        else:
            index = self.tab_widget.indexOf(widget)
        title = self.tab_widget.tabText(index)
        if title.endswith('*'):
            title = title[:-1]
        self.tab_widget.setTabText(index, title)
        if self.tab_widget.widget(index) is not None:
            self.tab_widget.widget(index).is_saved = True
            if index == self.tab_widget.currentIndex():
                self.action_save.setEnabled(False)

    def tabContentChanged(self, index):
        if self.tab_widget.currentWidget() is not None:
            self.tab_widget.currentWidget().undoRedoChange()
            self.tab_widget.currentWidget().itemSelectionChanged()
            self.action_save.setEnabled(not self.tab_widget.currentWidget().is_saved)

    def settingTrigger(self):
        if self.setting_watsh.hasPendingConnections():
            self.setting_watsh.nextPendingConnection()
        self.settingsChange()

    @loadingCursor(empty=True)
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
        self.main_window.setWindowOpacity(opacity)

        if self.translator:
            for translator in self.translator:
                QtCore.QCoreApplication.instance().removeTranslator(translator)
            self.translator = []
        if (not lang) or (lang is None) or (lang == 'locale') or (lang == 'None'):
            lang = QtCore.QLocale.system().name()

        translator = QtCore.QTranslator()
        if translator.load("resources/i18n/i18n_genvis." + lang):
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
            QtCore.QCoreApplication.translate('main_window',
                                              'New settings has been applied.'),
            3000
        )

    def execInCurrentTab(self, function_name):
        exec('self.tab_widget.currentWidget().' + function_name + '()')

    def closeTab(self, index=None):
        if index is None:
            index = self.tab_widget.currentIndex()

        action = QtWidgets.QMessageBox.NoRole
        if not self.tab_widget.widget(index).is_saved:
            action = self.showQuestionMessage(
                'Save changes to "' +
                self.tab_widget.tabToolTip(index) +
                '" before closing?'
            )

        if action == QtWidgets.QMessageBox.Yes:
            self.save(index)

        if action != QtWidgets.QMessageBox.Cancel:
            self.tab_widget.widget(index).undo_stack.clear()
            self.tab_widget.removeTab(index)
            if self.tab_widget.count() == 0:
                self.main_window.close()
            else:
                self.tab_widget.currentWidget().undoRedoChange()
                self.tab_widget.currentWidget().itemSelectionChanged()

                for i in range(self.tab_widget.count()):
                    title = self.tab_widget.tabText(i)
                    title = str(i + 1) + '.' + '.'.join(title.split('.')[1:])
                    self.tab_widget.setTabText(i, title)

            return True
        return False

    def quit(self, event):
        for i in range(self.tab_widget.count())[::-1]:
            forward = self.closeTab(i)
            if not forward:
                return event.ignore()
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

    def getConfiguration(self, key, file='GENVIS'):
        return self.config_handler.configurations[file][key]

    def setConfiguration(self, key, value, file='GENVIS'):
        self.config_handler.configurations[file][key] = value
        self.config_handler.save(file)
