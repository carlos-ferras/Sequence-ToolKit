#!/usr/bin/python3
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import os
import re
import subprocess
from functools import partial

from PyQt5 import QtWidgets, QtCore, QtGui, QtNetwork

from controller.dialogs.xml_preview import XMLPreview
from controller.gensec.dialogs.about import AboutGenSec
from controller.gensec.dialogs.merge_colors import MergeColors
from controller.gensec.dialogs.criterias import Criterias
from controller.gensec.gensec_tab import GenSecTab
from controller.stk.dialogs.about import AboutSTK
from controller.stk.dialogs.settings import Settings
from model.handle_config import ConfigHandler
from model.handle_recent_files import RecentFilesHandler
from model.handle_theme import ThemeHandler
from model.custom_data_type import CustomIndex
from view.gensec.ui_gensec import Ui_main_window
from controller.decorators import loadingCursor


class GenSec(Ui_main_window):
    def __init__(self, appname, dirs=None):
        self.appname = appname
        self.main_window = QtWidgets.QMainWindow()
        self.setupUi(self.main_window)

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

        self.action_undo.setEnabled(False)
        self.action_redo.setEnabled(False)
        self.action_merge.setEnabled(False)
        self.action_split.setEnabled(False)

        # file
        self.action_new.triggered.connect(self.new)
        self.action_open.triggered.connect(self.openSLF)
        self.action_save.triggered.connect(self.save)
        self.action_save_as.triggered.connect(self.saveAs)
        self.action_save_all.triggered.connect(self.saveAll)
        self.action_print.triggered.connect(self.print)
        self.main_window.setAcceptDrops(True)
        self.main_window.dropEvent = self.onDrop
        self.main_window.dragEnterEvent = self.onDrag
        self.main_window.dragMoveEvent = self.onDrag

        # sequence global
        self.action_name.triggered.connect(self.name)
        self.action_owner.triggered.connect(self.owner)
        self.action_nitrogen_use.triggered.connect(self.nitrogenUse)
        self.action_dose_rate.triggered.connect(self.doseRate)
        self.action_external_dose_rate.triggered.connect(self.externalDoseRate)
        self.action_protocol.triggered.connect(self.protocol)
        self.action_reader_id.triggered.connect(self.readerId)

        # open dialog
        self.action_merge_colors.triggered.connect(self.mergeColors)
        self.action_preview.triggered.connect(self.xmlPreview)
        self.action_settings.triggered.connect(self.settings)
        self.action_help.triggered.connect(self.help)
        self.action_about_gensec.triggered.connect(self.aboutGenSec)
        self.action_about.triggered.connect(self.aboutSTK)

        # edit
        self.action_undo.triggered.connect(partial(self.execInCurrentTab, 'undo'))
        self.action_redo.triggered.connect(partial(self.execInCurrentTab, 'redo'))
        self.action_cut.triggered.connect(partial(self.execInCurrentTab, 'cut'))
        self.action_copy.triggered.connect(partial(self.execInCurrentTab, 'copy'))
        self.action_paste.triggered.connect(partial(self.execInCurrentTab, 'paste'))
        self.action_delete.triggered.connect(partial(self.execInCurrentTab, 'delete'))
        self.action_clear_all.triggered.connect(self.clearAll)
        self.action_merge.triggered.connect(partial(self.execInCurrentTab, 'merge'))
        self.action_split.triggered.connect(partial(self.execInCurrentTab, 'split'))
        self.action_merge_by_criteria.triggered.connect(self.mergeByCriteria)
        self.action_split_by_criteria.triggered.connect(self.splitByCriteria)
        self.action_reset.triggered.connect(self.reset)
        self.action_add_row.triggered.connect(partial(self.execInCurrentTab, 'addRow'))
        self.action_add_column.triggered.connect(partial(self.execInCurrentTab, 'addColumn'))
        self.action_sort.triggered.connect(self.sort)

        # close events
        self.action_close.triggered.connect(self.closeTab)
        self.tab_widget.tabCloseRequested.connect(self.closeTab)
        self.action_quit.triggered.connect(self.main_window.close)
        self.main_window.closeEvent = self.quit

        self.tab_widget.currentChanged.connect(self.tabContentChanged)
        self.recent_files_handler.signals.recent_file_added.connect(self.fillRecentFiles)

        self.action_exec_genrep.triggered.connect(self.execGenRep)
        self.action_exec_genvis.triggered.connect(self.execGenVis)

        self.setting_watsh = QtNetwork.QLocalServer(self.main_window)
        self.setting_watsh.newConnection.connect(self.settingTrigger)
        self.setting_watsh.listen(os.path.join(self.config_handler.config_path, 'listening', self.appname))

        self.settingsChange()

        if dirs and dirs is not None:
            self.openSLF(dirs)
        else:
            self.new()

        self.fillRecentFiles(True)

    # --------------------------------------------------------------------------------

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

    def execGenVis(self):
        command = None
        # if os.sys.platform in ('linux', 'linux2'):
        if os.path.exists('genvis.pyw'):
            command = 'python3 genvis.pyw '
        # elif os.path.exists('GenVis.exe'):
        #     command = 'GenVis.exe '
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
                    'Unable to launch {0}').format('GenVis')
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
        self.openSLF(paths)

    @loadingCursor()
    def new(self, path=False):
        current_tab = GenSecTab(self.main_window)
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

    def openSLF(self, paths=False):
        if not paths:
            dialog = QtWidgets.QFileDialog(
                self.main_window,
                QtCore.QCoreApplication.translate('main_window', "Choose one or more files to open"),
                self.getConfiguration('default_file_location', 'COMMON'),
                QtCore.QCoreApplication.translate('main_window', 'File {0}').format(' SLF (*.slf)')
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
                if os.path.splitext(path)[-1] == '.slf':
                    is_open = False
                    for i in range(self.tab_widget.count()):
                        if self.tab_widget.tabToolTip(i) == str(path):
                            self.tab_widget.setCurrentIndex(i)
                            is_open = True
                    if not is_open:
                        self.recent_files_handler.appendPath(path, 'GENSEC')
                        if (self.tab_widget.currentWidget() is not None) and self.tab_widget.currentWidget().isEmpty():
                            self.openInCurrent(path)
                        else:
                            self.new(path)
                else:
                    self.showErrorMessage(
                        QtCore.QCoreApplication.translate('main_window', 'The file "{0}" is not valid, must be an slf.').format(path))
            else:
                self.showErrorMessage(QtCore.QCoreApplication.translate('main_window', 'The file "{0}" does not exist.').format(path))
        if self.tab_widget.count() == 0:
            self.new()

    def save(self, index=None):
        if (index is None) or (index is False):
            index = self.tab_widget.currentIndex()
        path = self.tab_widget.tabToolTip(index)
        if os.path.exists(path) and os.path.isfile(path) and (path.endswith('.slf') or path.endswith('.xml')):
            self.tab_widget.widget(index).save(path)
            if path.endswith('.slf'):
                self.recent_files_handler.appendPath(path, 'GENSEC')
            self.statusbar.showMessage(
                QtCore.QCoreApplication.translate('main_window',
                                                  '"{0}" has been saved.').format(path),
                3000
            )
        else:
            self.saveAs()

    def saveAs(self):
        path, selected_filter = QtWidgets.QFileDialog.getSaveFileName(
            self.main_window,
            QtCore.QCoreApplication.translate('main_window', "Save sequence as..."),
            self.getConfiguration('default_file_location', 'COMMON'),
            QtCore.QCoreApplication.translate(
                'main_window', 'File {0}').format(' SLF (*.slf);; ') +
            QtCore.QCoreApplication.translate(
                'main_window', 'File {0}').format(' XML (*.xml)')
        )

        if path:
            if ('xml' in selected_filter) and (not path.endswith('.xml')):
                path += '.xml'
            elif ('slf' in selected_filter) and (not path.endswith('.slf')):
                path += '.slf'

            title = str(self.tab_widget.currentIndex() + 1) + '. '

            if len(path) > 10:
                title += os.path.basename(path)
            else:
                title += path
            self.tab_widget.setTabText(self.tab_widget.currentIndex(), title)
            self.tab_widget.setTabToolTip(self.tab_widget.currentIndex(), path)
            self.tab_widget.currentWidget().save(path)
            if path.endswith('.slf'):
                self.recent_files_handler.appendPath(path, 'GENSEC')
            self.statusbar.showMessage(
                QtCore.QCoreApplication.translate('main_window',
                                                  '"{0}" has been saved.').format(path),
                3000
            )

    def saveAll(self):
        for index in range(self.tab_widget.count()):
            self.save(index)
        self.statusbar.showMessage(
            QtCore.QCoreApplication.translate('main_window',
                                              'All sequences has been saved.'),
            3000
        )

    def sort(self):
        self.statusbar.showMessage(
            QtCore.QCoreApplication.translate('main_window', 'Wait while sorting.'),
        )
        self.tab_widget.widget(self.tab_widget.currentIndex()).sort()
        self.statusbar.showMessage(
            QtCore.QCoreApplication.translate('main_window',
                                              'Samples has been sorted.'),
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

    def reset(self):
        action = self.showWarningMessage(
            QtCore.QCoreApplication.translate(
                'main_window',
                'This action may cause loss of data, do you want to continue?'
            )
        )
        if action:
            self.execInCurrentTab('reset')
        self.statusbar.showMessage(
            QtCore.QCoreApplication.translate('main_window',
                                              'The sequences has been restored.'),
            3000
        )

    def clearAll(self):
        action = self.showWarningMessage(
            QtCore.QCoreApplication.translate(
                'main_window',
                'This action may cause loss of data, do you want to continue?'
            )
        )
        if action:
            self.execInCurrentTab('clearAll')

    # --------------------------------------------------------------------------------

    def name(self):
        output, accepted = QtWidgets.QInputDialog.getText(
            self.main_window,
            QtWidgets.QApplication.translate('main_window', 'Name'),
            QtWidgets.QApplication.translate('main_window', 'Name') + ':',
            QtWidgets.QLineEdit.Normal,
            self.tab_widget.currentWidget().sequence_name
        )

        if accepted:
            pattern = re.compile('^([a-zA-Z][a-zA-Z0-9 ]*)$')
            if pattern.match(output) or not output:
                self.tab_widget.currentWidget().sequence_name = output
                self.tabChanged()
            else:
                self.showErrorMessage(
                    QtCore.QCoreApplication.translate(
                        'main_window',
                        'The Name entry should contain only letters and numbers and has to start with a letter.'
                    )
                )

    def owner(self):
        output, accepted = QtWidgets.QInputDialog.getText(
            self.main_window,
            QtWidgets.QApplication.translate('main_window', 'Owner'),
            QtWidgets.QApplication.translate('main_window', 'Owner') + ':',
            QtWidgets.QLineEdit.Normal,
            self.tab_widget.currentWidget().sequence_owner
        )

        if accepted:
            pattern = re.compile('^([a-zA-Z][a-zA-Z ]*)$')
            if pattern.match(output) or not output:
                self.tab_widget.currentWidget().sequence_owner = output
                self.tabChanged()
            else:
                self.showErrorMessage(
                    QtCore.QCoreApplication.translate(
                        'main_window',
                        'The Owner entry should contain only letters.'
                    )
                )

    def nitrogenUse(self):
        output, accepted = QtWidgets.QInputDialog.getInt(
            self.main_window,
            QtWidgets.QApplication.translate('main_window', 'Nitrogen Use'),
            QtWidgets.QApplication.translate('main_window', 'Nitrogen use') + ':',
            self.tab_widget.currentWidget().nitrogen_use,
            0, 1
        )

        if accepted:
            self.tab_widget.currentWidget().nitrogen_use = output
            self.tabChanged()


    def doseRate(self):
        output, accepted = QtWidgets.QInputDialog.getDouble(
            self.main_window,
            QtWidgets.QApplication.translate('main_window', 'Dose Rate'),
            QtWidgets.QApplication.translate('main_window', 'Dose rate') + ':',
            self.tab_widget.currentWidget().dose_rate,
            0, 9999999, 2
        )

        if accepted:
            self.tab_widget.currentWidget().dose_rate = output
            self.tabChanged()

    def externalDoseRate(self):
        output, accepted = QtWidgets.QInputDialog.getDouble(
            self.main_window,
            QtWidgets.QApplication.translate('main_window', 'External Dose Rate'),
            QtWidgets.QApplication.translate('main_window', 'External dose rate') + ':',
            self.tab_widget.currentWidget().external_dose_rate,
            0, 9999999, 2
        )

        if accepted:
            self.tab_widget.currentWidget().external_dose_rate = output
            self.tabChanged()

    def protocol(self):
        output, accepted = QtWidgets.QInputDialog.getText(
            self.main_window,
            QtWidgets.QApplication.translate('main_window', 'Protocol'),
            QtWidgets.QApplication.translate('main_window', 'Protocol') + ':',
            QtWidgets.QLineEdit.Normal,
            self.tab_widget.currentWidget().protocol
        )

        if accepted:
            pattern = re.compile('^([a-zA-Z]{16})$')
            if pattern.match(output) or not output:
                self.tab_widget.currentWidget().protocol = output
                self.tabChanged()
            else:
                self.showErrorMessage(
                    QtCore.QCoreApplication.translate(
                        'main_window',
                        'The Protocol entry should contain only letters, and has to be 16 characters long.'
                    )
                )

    def readerId(self):
        message = QtWidgets.QMessageBox(self.main_window)
        message.setWindowTitle(QtCore.QCoreApplication.translate('main_window', 'Reader ID'))
        message.setText(
            QtCore.QCoreApplication.translate('main_window', 'Reader id') +
            ': ' + self.tab_widget.currentWidget().reader_id
        )
        message.addButton(QtCore.QCoreApplication.translate('main_window', 'Ok'), QtWidgets.QMessageBox.AcceptRole)

        return message.exec_()

    # --------------------------------------------------------------------------------

    def mergeByCriteria(self):
        self.criteria_dialog = Criterias(QtCore.QCoreApplication.translate('main_window', 'Merge by Criterion'), self.main_window)
        self.criteria_dialog.accepted.connect(partial(self.criteriasAccepted, True))
        self.criteria_dialog.exec_()

    def splitByCriteria(self):
        self.criteria_dialog = Criterias(QtCore.QCoreApplication.translate('main_window', 'Split by Criterion'), self.main_window)
        self.criteria_dialog.accepted.connect(partial(self.criteriasAccepted, False))
        self.criteria_dialog.exec_()

    def criteriasAccepted(self, action=True):
        self.tab_widget.currentWidget().undo_stack.beginMacro(
            str(self.tab_widget.currentWidget().undo_stack_macro)
        )
        filters = self.criteria_dialog.getData()
        for row in range(self.tab_widget.currentWidget().tree_widget.topLevelItemCount()):
            item = self.tab_widget.currentWidget().tree_widget.topLevelItem(row)
            sample = item.text(1)
            if sample:
                to_change = []
                for column in range(self.tab_widget.currentWidget().column_count)[2:]:
                    if item.text(column):
                        current_data = None
                        if to_change:
                            if to_change[-1].column() + 1 == column:
                                current_data = self.tab_widget.currentWidget().process_data[
                                    str(to_change[-1].row()) +
                                    ',' +
                                    str(to_change[-1].column())
                                    ]
                            else:
                                if len(to_change) > 1:
                                    if action:
                                        self.tab_widget.currentWidget().merge(to_change)
                                    else:
                                        self.tab_widget.currentWidget().split(to_change)
                                to_change = []
                        data = self.tab_widget.currentWidget().process_data[str(row) + ',' + str(column)]
                        if data['id'] in range(2, 9):
                            match = True
                            for filter_ in filters:
                                if match:
                                    match = False
                                    data_in_criterion = self.tab_widget.currentWidget().getData(
                                        filter_[0],
                                        data,
                                        sample
                                    )
                                    current_data_in_criterion = data_in_criterion
                                    if current_data is not None:
                                        current_data_in_criterion = self.tab_widget.currentWidget().getData(
                                            filter_[0],
                                            current_data,
                                            sample
                                        )
                                    if data_in_criterion is not None:
                                        if filter_[1] is None:
                                            match = True
                                            if data_in_criterion != current_data_in_criterion:
                                                if len(to_change) > 1:
                                                    if action:
                                                        self.tab_widget.currentWidget().merge(to_change)
                                                    else:
                                                        self.tab_widget.currentWidget().split(to_change)
                                                to_change = []
                                        else:
                                            value = filter_[1]
                                            if '*' in value:
                                                while '*' in value:
                                                    position = value.find('*')
                                                    if str(data_in_criterion)[:position] != value[:position]:
                                                        break
                                                    value = value[position + 1:]
                                                    data_in_criterion = data_in_criterion[position + 1:]
                                                    if data == data_in_criterion:
                                                        match = True
                                            else:
                                                if str(value) == str(data_in_criterion):
                                                    match = True
                                break
                            if match:
                                to_change.append(CustomIndex(row, column))
                if len(to_change) > 1:
                    if action:
                        self.tab_widget.currentWidget().merge(to_change)
                    else:
                        self.tab_widget.currentWidget().split(to_change)
        self.tab_widget.currentWidget().undo_stack.endMacro()
        self.tab_widget.currentWidget().undo_stack_macro += 1

    def mergeColors(self):
        dialog = MergeColors(self.main_window)
        dialog.accepted.connect(partial(self.mergeColorsChange, dialog))
        dialog.show_error_message.connect(self.showErrorMessage)
        dialog.exec_()

    def xmlPreview(self):
        dialog = XMLPreview(self.main_window)
        sequence = self.tab_widget.currentWidget().createSLF()
        dialog.xml_content.setText(sequence.preview())
        if self.action_save.isEnabled():
            dialog.action_save.triggered.connect(self.save)
        else:
            dialog.action_save.setEnabled(False)
        dialog.action_save_as.triggered.connect(self.saveAs)
        dialog.show()

    def settings(self):
        dialog = Settings(self.main_window)
        dialog.exec_()

    def help(self):
        subprocess.Popen('python3 assistant.pyw gensec', shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, stdin=subprocess.PIPE)

    def aboutGenSec(self):
        dialog = AboutGenSec(self.main_window)
        dialog.exec_()

    def aboutSTK(self):
        dialog = AboutSTK(self.main_window)
        dialog.exec_()

    # --------------------------------------------------------------------------------

    def showSuccessMessage(self, message_text, title=QtCore.QCoreApplication.translate('main_window', 'Successfully!')):
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
        message.addButton(QtWidgets.QApplication.translate('main_window', 'Discard'), QtWidgets.QMessageBox.RejectRole)
        message.addButton(QtWidgets.QApplication.translate('main_window', 'Continue'), QtWidgets.QMessageBox.AcceptRole)
        return message.exec_()

    def showQuestionMessage(self, message_text, title=QtCore.QCoreApplication.translate('main_window', 'Attention!')):
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

        if not self.recent_files_handler.recent_files['GENSEC']:
            self.menu_recent_files.setEnabled(False)
        else:
            self.menu_recent_files.setEnabled(True)
        for date_path in self.recent_files_handler.recent_files['GENSEC']:
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
        action_file.triggered.connect(partial(self.openSLF, [date_path[1]]))
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

    def mergeColorsChange(self, dialog):
        old_color1_palette = self.getConfiguration('merge_color_1', 'GENSEC')
        old_color2_palette = self.getConfiguration('merge_color_2', 'GENSEC')
        old_color3_palette = self.getConfiguration('merge_color_3', 'GENSEC')

        color1_palette = dialog.color1_palette
        color2_palette = dialog.color2_palette
        color3_palette = dialog.color3_palette

        self.setConfiguration('merge_color_1', color1_palette)
        self.setConfiguration('merge_color_2', color2_palette)
        self.setConfiguration('merge_color_3', color3_palette)

        for tab in range(self.tab_widget.count()):
            for row in range(self.tab_widget.widget(tab).tree_widget.topLevelItemCount()):
                item = self.tab_widget.widget(tab).tree_widget.topLevelItem(row)
                for column in range(item.columnCount()):
                    current_foreground = item.foreground(column).color().name()
                    if current_foreground == old_color1_palette:
                        item.setForeground(column, QtGui.QColor(color1_palette))
                    elif current_foreground == old_color2_palette:
                        item.setForeground(column, QtGui.QColor(color2_palette))
                    elif current_foreground == old_color3_palette:
                        item.setForeground(column, QtGui.QColor(color3_palette))

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
        self.setConfiguration('widget_color', self.theme_handler.skin_keys['widget_color'], 'COMMON')
        self.setConfiguration('tree_widget_item_background', self.theme_handler.skin_keys['tree_widget_item_background'], 'COMMON')
        self.setConfiguration('tree_widget_item_alternate_background', self.theme_handler.skin_keys['tree_widget_item_alternate_background'], 'COMMON')
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

        if int(self.getConfiguration('font-size', 'COMMON')) > 12:
            height = int(int(self.getConfiguration('font-size', 'COMMON')) * 2.3333)
        else:
            height = 28
        for tab_index in range(self.tab_widget.count()):
            tab = self.tab_widget.widget(tab_index)
            tab.tree_widget.setStyleSheet('QTreeWidget::item{{height:{0}}}'.format(height))
            tab.tree_widget.headerItem().setText(
                0,
                QtCore.QCoreApplication.translate('tree_widget_tab', "Group")
            )
            tab.tree_widget.headerItem().setText(
                1,
                QtCore.QCoreApplication.translate('tree_widget_tab', "Sample")
            )
            for i in range(tab.column_count)[2:]:
                tab.tree_widget.headerItem().setText(
                    i,
                    QtCore.QCoreApplication.translate('tree_widget_tab', "Command {0}").format(i - 1)
                )
                tab.tree_widget.headerItem().setToolTip(
                    i,
                    QtCore.QCoreApplication.translate('tree_widget_tab', 'Add Column')
                )
                for j in range(tab.tree_widget.topLevelItemCount()):
                    item = tab.tree_widget.topLevelItem(j)
                    tool_button_header = tab.tree_widget.itemWidget(item, 0)
                    tool_button_header.setToolTip(QtCore.QCoreApplication.translate('tree_widget_tab', 'Add Row'))
            for i in range(tab.tree_widget.topLevelItemCount()):
                if i % 2 == 0:
                    color = self.getConfiguration('tree_widget_item_background', 'COMMON')
                else:
                    color = self.getConfiguration('tree_widget_item_alternate_background', 'COMMON')
                for j in range(tab.column_count):
                    tab.tree_widget.topLevelItem(i).setBackground(j, QtGui.QColor(color))

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
                    title = str(i+1) + '.' + '.'.join(title.split('.')[1:])
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

    def getConfiguration(self, key, file='GENSEC'):
        return self.config_handler.configurations[file][key]

    def setConfiguration(self, key, value, file='GENSEC'):
        self.config_handler.configurations[file][key] = value
        self.config_handler.save(file)
