#!/usr/bin/python3
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from PyQt5 import QtWidgets, QtCore, QtGui

import img_rc
from view.widgets.ui_treewidget_tab import Ui_tree_widget_tab
from model.handle_config import ConfigHandler
from model.handle_rlf import LoadRLF
from controller.decorators import loadingCursor


class GenVisTab(QtWidgets.QWidget, Ui_tree_widget_tab):
    show_success_message = QtCore.pyqtSignal(str)
    show_info_message = QtCore.pyqtSignal(str)
    show_error_message = QtCore.pyqtSignal(str)
    document_changed = QtCore.pyqtSignal(QtWidgets.QWidget)
    document_saved = QtCore.pyqtSignal(QtWidgets.QWidget)

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.config_handler = ConfigHandler()

        self.is_saved = True

        self.sequence_name = ''
        self.sequence_owner = ''
        self.samples_amount = 0
        self.status = ''
        self.nitrogen_use = 0
        self.dose_rate = 0
        self.external_dose_rate = 0
        self.creation_date = ''
        self.modification_date = ''
        self.protocol = ''
        self.reader_id = 'unknown'

        self.undo_stack = QtWidgets.QUndoStack(self)
        self.undo_stack.setUndoLimit(5)
        self.undo_stack_macro = 1

        self.undo_stack.canUndoChanged.connect(self.undoRedoChange)
        self.undo_stack.canRedoChanged.connect(self.undoRedoChange)

    def undo(self):
        if self.undo_stack.canUndo():
            self.undo_stack.undo()

    def redo(self):
        if self.undo_stack.canRedo():
            self.undo_stack.redo()

    def undoRedoChange(self):
        try:
            parent_windows = self.parent().parent().parent().parent()
            parent_windows.findChild(QtWidgets.QAction, "action_undo").setEnabled(self.undo_stack.canUndo())
            parent_windows.findChild(QtWidgets.QAction, "action_redo").setEnabled(self.undo_stack.canRedo())
        except:
            pass

    def itemSelectionChanged(self):
        pass

    def save(self, path):
        pass

    def print(self):
        pass

    def buildHtml(self):
        pass

    @loadingCursor()
    def open(self, path):
        loader = LoadRLF(path)
        general, table = loader.open()

        self.sequence_name = general['name']
        self.sequence_owner = general['owner']
        self.nitrogen_use = general['nitrogen_use']
        self.dose_rate = general['dose_rate']
        self.external_dose_rate = general['external_dose_rate']
        self.creation_date = general['creation_date']
        self.modification_date = general['modification_date']
        self.protocol = general['protocol']
        self.reader_id = general['reader_id']
        self.samples_amount = general['samples_amount']
        self.status = general['status']

        for row in table:
            sample_id = row[0]
            for command in row[1]:
                process_name = command['process_name']
                data_type = command['data_type']
                process_order_id = command['process_order_id']

                curves = command['curves']
                for curve in curves:
                    curve_data = curves[curve]
                    if 'count_signal' in curve_data:
                        pass
                    if 'count_background' in curve_data:
                        pass

                parameters = command['parameters']
                for parameter in parameters:
                    parameter_value = parameters[parameter]

    def isEmpty(self):
        return True

    def runCommand(self, command, *args):
        pass

    def getConfiguration(self, key, file):
        return self.config_handler.configurations[file][key]

    def setConfiguration(self, key, value, file):
        self.config_handler.configurations[file][key] = value
        self.config_handler.save(file)
