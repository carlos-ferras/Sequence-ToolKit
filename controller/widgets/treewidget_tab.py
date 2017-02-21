#!/usr/bin/python3
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from PyQt5 import QtWidgets, QtCore, QtGui

import img_rc
from view.widgets.ui_treewidget_tab import Ui_tree_widget_tab
from model.handle_config import ConfigHandler
from model.handle_slf import LoadSLF
from controller.decorators import loadingCursor


class TreeWidgetTab(QtWidgets.QWidget, Ui_tree_widget_tab):
    show_success_message = QtCore.pyqtSignal(str)
    show_info_message = QtCore.pyqtSignal(str)
    show_error_message = QtCore.pyqtSignal(str)
    document_changed = QtCore.pyqtSignal(QtWidgets.QWidget)
    document_saved = QtCore.pyqtSignal(QtWidgets.QWidget)

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.config_handler = ConfigHandler()

        self.column_count = 2
        self.row_count = 0
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

        self.in_merge = []
        self.process_data = {}
        self.external_irradiation = []
        self.external_irradiation_defined = []

        self.undo_stack = QtWidgets.QUndoStack(self)
        self.undo_stack.setUndoLimit(5)
        self.undo_stack_macro = 1

        if int(self.getConfiguration('font-size', 'COMMON')) > 12:
            height = int(int(self.getConfiguration('font-size', 'COMMON')) * 2.3333)
        else:
            height = 28
        self.tree_widget.setStyleSheet('QTreeWidget::item{{height:{0}}}'.format(height))

        widget = QtWidgets.QDesktopWidget()
        main_screen_size = widget.availableGeometry(widget.primaryScreen())
        screen_width = main_screen_size.width()
        column_width = screen_width % 125
        num = screen_width - column_width
        if column_width < 55:
            num -= 55
            column_width += 55
        columns_cant = int(num / 125) - 1
        for i in range(columns_cant):
            self.addColumn()

        self.tree_widget.header().setSectionsMovable(False)
        self.tree_widget.header().setDefaultSectionSize(125)
        self.tree_widget.header().setHighlightSections(True)
        self.tree_widget.header().setMinimumSectionSize(column_width)
        self.tree_widget.header().setSectionsClickable(True)
        self.tree_widget.setColumnWidth(0, column_width)
        self.tree_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree_widget.header().resizeSection(0, 80)

        screen_height = main_screen_size.height() - 78
        if int(self.getConfiguration('font-size', 'COMMON')) > 11:
            rows_cant = int(screen_height / (int(self.getConfiguration('font-size', 'COMMON')) * 2)) + 1
            if int(self.getConfiguration('font-size', 'COMMON')) < 16:
                rows_cant -= 4
            elif int(self.getConfiguration('font-size', 'COMMON')) > 47:
                pass
            else:
                rows_cant -= 1
        else:
            rows_cant = 27
        for i in range(rows_cant):
            self.addRow()

        self.undo_stack.canUndoChanged.connect(self.undoRedoChange)
        self.undo_stack.canRedoChanged.connect(self.undoRedoChange)

        self.tree_widget.itemSelectionChanged.connect(self.itemSelectionChanged)
        self.tree_widget.customContextMenuRequested.connect(self.popup)

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

    @loadingCursor()
    def merge(self, processes_to_merge=None):
        try:
            if not processes_to_merge or processes_to_merge is None:
                processes_to_merge = self.tree_widget.selectedIndexes()
            for index in processes_to_merge:
                try:
                    temp = self.process_data[str(index.row()) + ',' + str(index.column())]
                    id_ = temp["id"]
                except:
                    raise RuntimeError(
                        QtCore.QCoreApplication.translate(
                            'tree_widget_tab',
                            'Command {0} is empty'
                        ).format(str(index.column() - 1))
                    )
                if id_ in [0, 1, 9]:
                    if id_ in [0, 1]:
                        process = 'Irradiation'
                    else:
                        process = 'Pause'
                    raise RuntimeError(
                        QtCore.QCoreApplication.translate(
                            'tree_widget_tab',
                            'Unable to perform the operation, the process ' + process + ' does not support merging.'
                        )
                    )
                else:
                    pass

            self.runCommand('Merge', self, processes_to_merge)
            self.document_changed.emit(self)
        except Exception as err:
            self.show_error_message.emit(str(err))

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
        loader = LoadSLF(path)
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

        current_row = 0
        last_row = self.tree_widget.topLevelItemCount() - 1
        before = self.getConfiguration('widget_color', 'COMMON')
        after = self.getConfiguration('widget_color', 'COMMON')


        for row in table:
            if current_row > last_row:
                self.addRow()
            self.setValue(current_row, 1, row[0])
            current_column = 2
            for command_set in row[1]:
                if not command_set:
                    current_column += 1
                    continue
                if len(command_set) > 1:
                    process_order_id = 0
                    in_merge = []
                    color = self.getColor(before, after)
                    before = after
                    after = color
                for command in command_set:
                    if current_column >= self.column_count:
                        self.addColumn()
                    id_ = command['id']
                    status = command['status']
                    if id_ == 0 and current_row == 0:
                        self.setValue(current_row, current_column, 'External Irradiation, ' +
                                      str(command['time'] * self.external_dose_rate) + 'Gy')
                        self.external_irradiation.append(current_column)
                        self.external_irradiation_defined.append(current_row)
                    elif id_ == 1:
                        self.setValue(current_row, current_column, 'Beta Irradiation, ' + str(command['time']) + 's')
                    elif id_ == 2:
                        self.setValue(current_row, current_column, 'TL, ' + str(command['final_temp']) + '°C, ' + str(
                            command['heating_rate']) + '°C/s')
                    elif id_ == 3:
                        self.setValue(current_row, current_column, 'OSL, ' + str(command['light_source']) + ', ' + str(
                            command['start_optical_power']) + '%')
                    elif id_ == 4:
                        self.setValue(current_row, current_column, 'POSL, ' + str(command['light_source']) + ', ' + str(
                            command['start_optical_power']) + '%')
                    elif id_ == 5:
                        self.setValue(current_row, current_column, 'LMOSL, ' + str(command['light_source']) + ', ' + str(
                            command['end_optical_power']) + '%')
                    elif id_ == 6:
                        self.setValue(current_row, current_column, 'ESL, ' + str(command['excF']) + 'KHz, ' + str(command['excV']) + 'V')
                    elif id_ == 7:
                        self.setValue(current_row, current_column,
                                      'Pre-Heat, ' + str(command['final_temp']) + '°C, ' + str(
                                          command['heating_rate']) + '°C/s')
                    elif id_ == 8:
                        self.setValue(current_row, current_column, 'Illumination, ' + str(command['light_source']) + ', ' + str(
                            command['start_optical_power']) + '%')
                    elif id_ == 9:
                        self.setValue(current_row, current_column, 'Pause, ' + str(command['time']) + 's')

                    if (id_ != 0 or (id_ == 0 and current_row == 0)) and id_!=-1:
                        self.process_data[str(current_row) + ',' + str(current_column)] = command
                        self.setIcon(current_row, current_column, status)

                    if len(command_set) > 1:
                        in_merge.append(str(current_row) + ',' + str(current_column))
                        parent_item = self.tree_widget.topLevelItem(current_row)
                        parent_item.setForeground(current_column, QtGui.QColor(color))
                        if not process_order_id:
                            process_order_id = self.process_data[str(current_row) + ',' + str(current_column)]['process_order_id']
                        else:
                            self.process_data[str(current_row) + ',' + str(current_column)]['process_order_id'] = process_order_id
                    current_column += 1
                if len(command_set) > 1:
                    self.in_merge.append(in_merge)
            current_row += 1
        self.undo_stack.clear()

        return True

    def getSamplesList(self, sample):
        all_samples = []
        parts = str(sample).split(',')
        for part in parts:
            numbers = part.split('-')
            if len(numbers) > 1:
                range_ = range(int(numbers[0]), int(numbers[-1]) + 1)
                for n in range_:
                    all_samples.append(n)
            else:
                all_samples.append(int(numbers[0]))
        return all_samples

    def sampleExist(self, n):
        for i in range(self.tree_widget.topLevelItemCount()):
            item = self.tree_widget.topLevelItem(i)
            if item.text(1):
                if n in self.getSamplesList(item.text(1)):
                    return i + 1
        return False

    def samplesRepeated(self):
        all_samples = []
        for i in range(self.tree_widget.topLevelItemCount()):
            item = self.tree_widget.topLevelItem(i)
            if item.text(1):
                if len(list(set(all_samples) and set(self.getSamplesList(item.text(1))))) > 0:
                    return True
                all_samples += self.getSamplesList(item.text(1))
        return False

    def areConsecutive(self):
        selected_index = []
        selected_index[:] = self.tree_widget.selectedIndexes()[:]
        for i in range(len(selected_index)):
            for j in range(len(selected_index))[i:]:
                if selected_index[i] > selected_index[j]:
                    temp = selected_index[i]
                    selected_index[i] = selected_index[j]
                    selected_index[j] = temp

        if len(selected_index) == 1:
            return False
        try:
            column = selected_index[0].column()
            if column < 2:
                return False
        except:
            return False

        row = selected_index[0].row()
        for item in selected_index[1:]:
            if (item.column() != (column + 1)) or (item.row() != row):
                return False
            column = item.column()
        return True

    def setData(self, process_data, cell_position):
        data = process_data[0]
        all_ = process_data[1]
        row = cell_position[0]
        column = cell_position[1]
        self.runCommand('SetData', self, row, column, data, all_)
        self.document_changed.emit(self)

    def setValue(self, row, column, value):
        if column < 1:
            raise ValueError(
                QtCore.QCoreApplication.translate(
                    'tree_widget_tab',
                    'The column parameter must be a number greater than 0.'
                )
            )
        self.runCommand('SetValue', self, row, column, value)

        self.document_changed.emit(self)
        return value

    def addRow(self):
        pass

    def addColumn(self):
        pass

    def isEmpty(self):
        if (self.sequence_name or self.sequence_owner or
                self.nitrogen_use or self.dose_rate or
                self.external_dose_rate or self.creation_date or
                self.protocol):
            return False
        for i in range(self.tree_widget.topLevelItemCount()):
            item = self.tree_widget.topLevelItem(i)
            for column in range(item.columnCount())[1:]:
                if item.text(column):
                    return False
        return True

    def setIcon(self, row, column, status):
        return self.tree_widget.topLevelItem(row).setIcon(column, QtGui.QIcon(':/resources/img/icons/status_' + str(status) + '.svg'))

    def quitIcon(self, row, column):
        return self.tree_widget.topLevelItem(row).setIcon(column, QtGui.QIcon(QtGui.QIcon()))

    def getColor(self, before, after):
        merge_colors = [
            self.getConfiguration('merge_color_1', 'GENSEC'),
            self.getConfiguration('merge_color_2', 'GENSEC'),
            self.getConfiguration('merge_color_3', 'GENSEC')
        ]
        return list(set(merge_colors) - {before, after})[0]

    def popup(self, pos):
        pass

    def runCommand(self, command, *args):
        pass

    def getConfiguration(self, key, file):
        return self.config_handler.configurations[file][key]

    def setConfiguration(self, key, value, file):
        self.config_handler.configurations[file][key] = value
        self.config_handler.save(file)
