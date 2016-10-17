#!/usr/bin/python3
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import os
import pickle
from datetime import datetime
import tempfile

from PyQt5 import QtWidgets, QtCore, QtGui, QtPrintSupport

import img_rc
from controller.widgets.treewidget_tab import TreeWidgetTab
from controller.gensec.dialogs.processes_set import ProcessesSet
from model.custom_data_type import CustomDataSet
from model.handle_slf import CreateSLF
from controller.widgets.undo_framework_commands import SetValue, SetData
from controller.gensec.undo_framework_commands import Delete, ClearAll, Reset, Paste, Save, Merge, Split
from controller.decorators import loadingCursor


class GenSecTab(TreeWidgetTab):
    show_success_message = QtCore.pyqtSignal(str)
    show_info_message = QtCore.pyqtSignal(str)
    show_error_message = QtCore.pyqtSignal(str)
    document_changed = QtCore.pyqtSignal(QtWidgets.QWidget)
    document_saved = QtCore.pyqtSignal(QtWidgets.QWidget)

    def __init__(self, parent=None):
        TreeWidgetTab.__init__(self, parent)

        self.process_dialog = None

        self.tree_widget.header().sectionClicked.connect(self.headerAction)
        self.tree_widget.itemDoubleClicked.connect(self.itemAction)

        self.action_cut.triggered.connect(self.cut)
        self.action_copy.triggered.connect(self.copy)
        self.action_paste.triggered.connect(self.paste)
        self.action_delete.triggered.connect(self.delete)
        self.action_merge.triggered.connect(self.merge)
        self.action_split.triggered.connect(self.split)
        self.action_select_row.triggered.connect(self.selectRow)
        self.undo_stack.canUndoChanged.connect(self.undoRedoChange)
        self.undo_stack.canRedoChanged.connect(self.undoRedoChange)

    def open(self, path):
        super(GenSecTab, self).open(path)
        self.document_saved.emit(self)

    def cut(self):
        self.copy()
        self.delete()
        self.document_changed.emit(self)

    def copy(self):
        if len(self.tree_widget.selectedIndexes()) > 0:
            data_set = CustomDataSet()

            first_row = 9999999
            first_column = 9999999
            for item in self.tree_widget.selectedIndexes():
                first_row = min(first_row, item.row())
                first_column = min(first_column, item.column())

            for item in self.tree_widget.selectedIndexes():
                if item.column() > 1:
                    try:
                        row = item.row() - first_row
                        column = item.column() - first_column
                        text = self.tree_widget.topLevelItem(item.row()).text(item.column())
                        data = self.process_data[str(item.row())+','+str(item.column())]

                        added = False
                        for group in range(len(self.in_merge)):
                            if data_set.custom_data_set and \
                                    (str(item.row()) + ',' + str(item.column()) in self.in_merge[group]) and \
                                    (str(data_set.custom_data_set[-1][-1].position.row() + first_row) + ',' +
                                     str(data_set.custom_data_set[-1][-1].position.column() + first_column) in
                                     self.in_merge[group]):
                                data_set.setData(
                                    row,
                                    column,
                                    text,
                                    data,
                                    True
                                )
                                added = True
                                break
                        if not added:
                            data_set.setData(
                                row,
                                column,
                                text,
                                data
                            )
                    except:
                        pass
            clipboard = QtWidgets.QApplication.clipboard()
            mime_data = QtCore.QMimeData()
            mime_data.setData('custom_data_type', QtCore.QByteArray(pickle.dumps(data_set)))
            mime_data.setText(str(data_set))
            clipboard.setMimeData(mime_data)
        return None

    def paste(self):
        self.runCommand('Paste', self)
        self.document_changed.emit(self)

    def delete(self):
        self.runCommand('Delete', self)
        self.document_changed.emit(self)

    @loadingCursor(empty=True)
    def clearAll(self):
        self.runCommand('ClearAll', self)
        self.document_changed.emit(self)

    def split(self, processes_to_split=None):
        if not processes_to_split or processes_to_split is None:
            processes_to_split = self.tree_widget.selectedIndexes()

        self.runCommand('Split', self, processes_to_split)
        self.document_changed.emit(self)

    def itemSelectionChanged(self):
        try:
            can_merge = self.areConsecutive()
            can_split = False
            is_valid = True
            is_editable = True

            for item in self.tree_widget.selectedIndexes():
                if item.column() < 2:
                    is_editable = False
                    if item.column() < 1:
                        is_valid = False
                for group in range(len(self.in_merge)):
                    for poss in self.in_merge[group]:
                        if str(item.row()) + ',' + str(item.column()) == poss:
                            can_split = True

            parent_windows = self.parent().parent().parent().parent()
            parent_windows.findChild(QtWidgets.QAction, "action_merge").setEnabled(can_merge)
            parent_windows.findChild(QtWidgets.QAction, "action_split").setEnabled(can_split)

            parent_windows.findChild(QtWidgets.QAction, "action_cut").setEnabled(is_editable)
            parent_windows.findChild(QtWidgets.QAction, "action_copy").setEnabled(is_editable)
            parent_windows.findChild(QtWidgets.QAction, "action_paste").setEnabled(is_editable)

            parent_windows.findChild(QtWidgets.QAction, "action_delete").setEnabled(is_valid)
        except:
            pass

    @loadingCursor(empty=True)
    def reset(self):
        self.runCommand('Reset', self)
        self.document_changed.emit(self)

    @loadingCursor(empty=True)
    def sort(self):
        tmp_path = tempfile.gettempdir()
        path = os.path.join(tmp_path, str(datetime.now()) + '.slf')
        try:
            self.save(path)
            self.clearAll()
            self.open(path)
            self.document_changed.emit(self)
        except:
            pass

    @loadingCursor()
    def save(self, path):
        sequence = self.createSLF()
        sequence.save(path, True)
        self.runCommand('Save', self)

    def print(self):
        printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
        printer.setOutputFormat(QtPrintSupport.QPrinter.PdfFormat)
        printer.setOutputFileName(
            os.path.join(
                self.getConfiguration('default_file_location', 'COMMON'),
                'sequence_' + str(datetime.now()) + '.pdf'
            )
        )

        dialog = QtPrintSupport.QPrintDialog(printer, self)
        dialog.setWindowTitle(QtCore.QCoreApplication.translate('tree_widget_tab', 'Print Table View'))

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            text_document = QtGui.QTextDocument()
            text_document.setHtml(self.buildHtml())
            text_document.print_(printer)

    @loadingCursor(empty=True)
    def buildHtml(self):
        sequence_datetime = '<table><tr><td><b>GenSec: </b>' + \
                            str(datetime.now()) +\
                            '</td></tr></table><hr>'

        sequence_global = \
            '<table><tr><td>' + \
            QtCore.QCoreApplication.translate('tree_widget_tab', 'Name') +\
            ': </td><td>' + self.sequence_name + '</td></tr><tr><td>' + \
            QtCore.QCoreApplication.translate('tree_widget_tab', 'Owner') + \
            ': </td><td>' + self.sequence_owner + '</td></tr><tr><td>' + \
            QtCore.QCoreApplication.translate('tree_widget_tab', 'Created') + \
            ': </td><td>' + str(self.creation_date) + '</td></tr><tr><td>' + \
            QtCore.QCoreApplication.translate('tree_widget_tab', 'Nitrogen Use') + \
            ': </td><td>' + str(self.nitrogen_use) + '</td></tr><tr><td>' + \
            QtCore.QCoreApplication.translate('tree_widget_tab', 'Dose Rate') + \
            ': </td><td>' + str(self.dose_rate) + '</td></tr><tr><td>' + \
            QtCore.QCoreApplication.translate('tree_widget_tab', 'External Dose Rate') + \
            ': </td><td>' + str(self.external_dose_rate) + '</td></tr><tr><td>' + \
            QtCore.QCoreApplication.translate('tree_widget_tab', 'Protocol') + \
            ': </td><td>' + self.protocol + '</td></tr><tr><td>' + \
            QtCore.QCoreApplication.translate('tree_widget_tab', 'Reader ID') + \
            ': </td><td>' + self.reader_id + '</td></tr><tr><td> </td><td> </td></tr></table>'

        html = ''
        row_count = 0
        column_count = 0
        for i in range(self.tree_widget.topLevelItemCount()):
            item = self.tree_widget.topLevelItem(i)
            if item.text(1):
                row_count += 1
                item_column_count = 0
                html += '<tr style="border: 0; background:#FFFFFF">'
                html += '<td style="background:#eeeeee;color:#3e3e3e;border:0px;">     ' + \
                        str(row_count) + '      </td>'
                html += '<td>     ' + str(item.text(1)) + '     </td>'
                for column in range(self.column_count)[2:]:
                    color = item.foreground(column).color().name()
                    font = self.getConfiguration('font-family', 'COMMON')
                    size = str(self.getConfiguration('font-size', 'COMMON'))
                    data = item.text(column)
                    text = ''
                    for c in data:
                        try:
                            text += str(c)
                        except:
                            text += '°'
                    if text != '':
                        if str(self.process_data[str(i) + ',' + str(column)]['status']) == 'running':
                            icon_source = ':/resources/img/icons/status_exe.svg'
                        elif str(self.process_data[str(i) + ',' + str(column)]['status']) == 'pend':
                            icon_source = ':/resources/img/icons/status_pend.svg'
                        else:
                            icon_source = ':/resources/img/icons/status_done.svg'
                        icon = '<img width="10" height="10" src="' + icon_source + '"></img>'
                    else:
                        icon = ''
                    html += '<td style="font-family:' + font + \
                            ';font-size:' + size + \
                            '; color:' + color + ';">' + \
                            str(icon) + '     ' + text + '     </td>'
                    item_column_count += 1
                html += '</tr>'
                if column_count < item_column_count:
                    column_count = item_column_count
        html += "</table></body></html>"

        header = '<table border="1" style="background:#fafafa"><tr style="background:#eeeeee;color:#3e3e3e;border:0px;"><td style="padding:8px">     ' + \
                 QtCore.QCoreApplication.translate('tree_widget_tab', 'Group') + \
                 '     </td><td style="padding:8px">     ' + \
                 QtCore.QCoreApplication.translate('tree_widget_tab', 'Sample') + '     </td>'
        for i in range(column_count):
            header += '<td style="padding:8px">     ' + str(i + 1) + '     </td>'
        header += '</tr>'
        html = sequence_datetime + sequence_global + header + html
        return html

    def createSLF(self):
        samples_numbers = []
        sample_commands = self.getSampleCommands()
        samples_amount = 0
        for row in sample_commands:
            samples = row[0]
            sample_list = samples.split(',')
            for sample in sample_list:
                if '-' in sample:
                    sample_range = sample.split('-')
                    start = int(sample_range[0])
                    end = int(sample_range[-1])
                    for val in range(start, end + 1):
                        if val not in samples_numbers:
                            samples_amount += 1
                            samples_numbers.append(val)
                elif not int(sample) in samples_numbers:
                    samples_amount += 1
                    samples_numbers.append(int(sample))

        sequence = CreateSLF(
            samples_amount=samples_amount,
            name=self.sequence_name,
            owner=self.sequence_owner,
            nitrogen_use=self.nitrogen_use,
            dose_rate=self.dose_rate,
            external_dose_rate=self.external_dose_rate,
            protocol=self.protocol,
            reader_id=self.reader_id,
            datecrea=self.creation_date
        )
        process_order_by_sample = {}
        for row in sample_commands:
            samples = row[0]
            sample_list = samples.split(',')
            for sample in sample_list:
                if len(sample) == 1:
                    samples_ids = sample
                elif len(sample) > 1:
                    sample_range = sample.split('-')
                    samples_ids = range(int(sample_range[0]), int(sample_range[-1]) + 1)
                for id_ in samples_ids:
                    commands = {}
                    sample_id = sequence.createSample(id_)

                    for command in row[1]:
                        status = command['status']
                        group = []
                        try:
                            group[:] = commands[command['process_order_id']][1][:]
                        except:
                            pass

                        data = {
                            'curve1': str(command['curve1']),
                            'curve2': str(command['curve2']),
                            'curve3': str(command['curve3']),
                            'time1': str(command['time1']),
                            'time2': str(command['time2'])
                        }

                        group.append(sequence.createProcess(command['id'], command, data, command['column']))
                        commands[command['process_order_id']] = [status, group[:]]

                    for group in commands:
                        try:
                            last = process_order_by_sample[str(id_)]
                            process_order_by_sample[str(id_)] += 1
                        except:
                            last = 1
                            process_order_by_sample[str(id_)] = 2
                        if commands[group][1][0].getAttribute('id') == '0' or commands[group][1][0].getAttribute(
                                'id') == '1':
                            command_type = 'irrad'
                        elif commands[group][1][0].getAttribute('id') == '9':
                            command_type = 'pc'
                        else:
                            command_type = 'meas'
                        status = commands[group][0]
                        sequence.createProcessOrder(
                            sample_id,
                            last,
                            type_=command_type,
                            status=status,
                            processes=commands[group][1]
                        )
        return sequence

    def getSampleCommands(self):
        samples = []
        for row in range(self.tree_widget.topLevelItemCount()):
            item = self.tree_widget.topLevelItem(row)
            if item.text(1):
                sample = [str(item.text(1)), []]
                for column in range(self.column_count)[2:]:
                    data = item.text(column)
                    if data != '':
                        process_data = self.process_data[str(row) + ',' + str(column)]
                        if process_data['id'] == 0:
                            process_data['doserate'] = process_data['time'] * self.dose_rate
                        elif process_data['id'] == 1:
                            process_data['doserate'] = process_data['time'] * self.external_dose_rate

                        if len(self.external_irradiation) > 0:
                            process_data['process_order_id'] = int(process_data['process_order_id']) + len(
                                sorted([j for j in self.external_irradiation if j < column]))

                        sample[1].append(process_data)
                        sample[1][-1]['column'] = column
                    elif column in self.external_irradiation:
                        index = self.external_irradiation.index(column)
                        process_data = self.process_data[str(self.external_irradiation_defined[index]) + ',' + str(column)]
                        process_data['doserate'] = process_data['time'] * self.external_dose_rate
                        sample[1].append(process_data)
                        sample[1][-1]['column'] = column
                if sample[1]:
                    samples.append(sample)
        return samples

    def clearGroupMerge(self, group):
        for poss in self.in_merge[group]:
            row = int(poss.split(',')[0])
            column = int(poss.split(',')[1])
            parent_item = self.tree_widget.topLevelItem(row)
            parent_item.setForeground(column, QtGui.QColor(self.getConfiguration('widget_color', 'COMMON')))
            try:
                self.process_data[poss]['process_order_id'] = column - 1
                self.process_data[poss]['status'] = 'pend'
                self.setIcon(row, column, 'pend')
            except:
                pass

    def deleteInMerge(self, merge_to_delete):
        for group in merge_to_delete:
            try:
                del self.in_merge[group]
            except:
                pass

    def addRow(self):
        item = QtWidgets.QTreeWidgetItem(self.tree_widget)
        if self.row_count % 2 == 0:
            color = self.getConfiguration('tree_widget_item_background', 'COMMON')
        else:
            color = self.getConfiguration('tree_widget_item_alternate_background', 'COMMON')
        for i in range(self.column_count):
            item.setBackground(i, QtGui.QColor(color))
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        tool_button_header = QtWidgets.QToolButton()
        tool_button_header.setText(QtCore.QCoreApplication.translate('tree_widget_tab', str(self.row_count + 1)))
        tool_button_header.setToolTip(QtCore.QCoreApplication.translate('tree_widget_tab', 'Add Row'))
        self.tree_widget.setItemWidget(item, 0, tool_button_header)
        tool_button_header.clicked.connect(self.addRow)
        vs = self.tree_widget.verticalScrollBar()
        vs.setValue(vs.maximum())
        self.row_count += 1
        return self.row_count

    def addColumn(self):
        self.tree_widget.headerItem().setText(
            self.column_count,
            QtCore.QCoreApplication.translate('tree_widget_tab', "Command {0}").format(self.column_count - 1)
        )
        self.tree_widget.headerItem().setToolTip(
            self.column_count,
            QtCore.QCoreApplication.translate('tree_widget_tab', 'Add Column')
        )
        hs = self.tree_widget.horizontalScrollBar()
        hs.setValue(hs.maximum())
        self.column_count += 1
        return self.column_count

    def headerAction(self, logical_index):
        if logical_index > 1:
            self.addColumn()

    def isValidSample(self, sample):
        if len(sample) > 1:
            if sample[0].isdigit():
                num = ''
                num += sample[0]
                for i in range(len(sample))[1:]:
                    if sample[i].isdigit():
                        num += sample[i]
                        if i == len(sample) - 1:
                            if 0 < int(num) < 25:
                                return True
                    else:
                        if sample[i] == '-' or sample[i] == ',':
                            return self.isValidSample(sample[i + 1:])
                        else:
                            return False
        elif sample == '':
            return True
        elif sample.isdigit() and 0 < int(sample) < 24:
            return True
        return False

    def itemAction(self, item, column):
        row = self.tree_widget.indexFromItem(item).row()
        data = item.text(column)
        if column == 1:
            sample, accepted = QtWidgets.QInputDialog.getText(
                self,
                QtWidgets.QApplication.translate('tree_widget_tab', 'Sample'),
                QtWidgets.QApplication.translate('tree_widget_tab', 'Sample') + ':',
                QtWidgets.QLineEdit.Normal,
                data
            )

            if accepted:
                try:
                    if self.isValidSample(str(sample)):
                        all_samples = []
                        sections = str(sample).split(',')
                        for section in sections:
                            samples_numbers = section.split('-')
                            if len(samples_numbers) > 1:
                                current = 0
                                for num in samples_numbers:
                                    try:
                                        n = int(num)
                                    except:
                                        raise ValueError(
                                            QtCore.QCoreApplication.translate(
                                                'tree_widget_tab',
                                                'Samples must have the structure [1-3,4,5]\nonly contains ranges '
                                                'and numbers between 1-24 separated by commas.'
                                            )
                                        )
                                    if n <= current:
                                        raise ValueError(
                                            QtCore.QCoreApplication.translate(
                                                'tree_widget_tab',
                                                'samples ranges must be low to high, and should not have repeated elements.'
                                            )
                                        )
                                    else:
                                        current = int(num)
                                range_ = range(int(samples_numbers[0]), int(samples_numbers[-1]) + 1)
                                for n in range_:
                                    if n not in all_samples:
                                        if self.external_irradiation:
                                            if not self.sampleExist(n):
                                                all_samples.append(n)
                                            else:
                                                raise ValueError(
                                                    QtCore.QCoreApplication.translate(
                                                        'tree_widget_tab',
                                                        'Incompatible sample declaration.'
                                                    )
                                                )
                                        else:
                                            all_samples.append(n)
                                    else:
                                        raise ValueError(
                                            QtCore.QCoreApplication.translate(
                                                'tree_widget_tab',
                                                'There are repeated number in sample sequence.'
                                            )
                                        )
                            elif str(samples_numbers[0]) != '':
                                if not int(samples_numbers[0]) in all_samples:
                                    if self.external_irradiation:
                                        if not self.sampleExist(int(samples_numbers[0])):
                                            all_samples.append(int(samples_numbers[0]))
                                        else:
                                            raise ValueError(
                                                QtCore.QCoreApplication.translate(
                                                    'tree_widget_tab',
                                                    'Incompatible sample declaration.'
                                                )
                                            )
                                    else:
                                        all_samples.append(int(samples_numbers[0]))
                                else:
                                    raise ValueError(
                                        QtCore.QCoreApplication.translate(
                                            'tree_widget_tab',
                                            'There are repeated number in sample sequence.'
                                        )
                                    )
                        self.setValue(row, column, str(sample))
                    else:
                        raise ValueError(
                            QtCore.QCoreApplication.translate(
                                'tree_widget_tab',
                                'Samples must have the structure [1-3,4,5]\nonly contains ranges '
                                'and numbers between 1-24 separated by commas.'
                            )
                        )
                except Exception as err:
                    self.show_error_message.emit(str(err))

        elif column > 1:
            command = data.split(',')[0]
            position_process_data = False
            if str(row) + ',' + str(column) in self.process_data:
                position_process_data = self.process_data[str(row) + ',' + str(column)]

            self.processes_dialog = ProcessesSet((row, column), self)
            self.processes_dialog.process_accepted.connect(self.setData)

            if command and command is not None:
                command = command.split()[-1]
                self.processes_dialog.getProcessDialog(command, position_process_data)
            else:
                self.processes_dialog.exec_()
        else:
            pass

    def selectRow(self):
        for index in self.tree_widget.selectedIndexes():
            item = self.tree_widget.topLevelItem(index.row())
            item.setSelected(True)

    def getData(self, filter_, data, sample):
        if filter_ == 0:
            return sample
        elif filter_ == 1:
            return data['id']
        elif filter_ == 2:
            return data['date_type']

    def popup(self, pos):
        x = pos.x() + 3
        y = pos.y()
        pos = QtCore.QPoint(x, y)
        menu = QtWidgets.QMenu()

        is_valid = True
        is_editable = True
        for index in self.tree_widget.selectedIndexes():
            if index.column() < 2:
                is_editable = False
                if index.column() < 1:
                    is_valid = False
                break
        if is_editable:
            menu.addAction(self.action_cut)
            menu.addAction(self.action_copy)
            menu.addAction(self.action_paste)
        if is_valid:
            menu.addAction(self.action_delete)
            menu.addSeparator()
        if is_editable:
            parent_windows = self.parent().parent().parent().parent()
            if parent_windows.findChild(QtWidgets.QAction, "action_merge").isEnabled():
                menu.addAction(self.action_merge)
            if parent_windows.findChild(QtWidgets.QAction, "action_split").isEnabled():
                menu.addAction(self.action_split)
        if is_valid:
            menu.addSeparator()
            menu.addAction(self.action_select_row)
            menu.exec_(self.tree_widget.mapToGlobal(pos))

    def runCommand(self, command, *args):
        commands = {
            'SetValue': SetValue,
            'SetData': SetData,
            'Delete': Delete,
            'ClearAll': ClearAll,
            'Merge': Merge,
            'Split': Split,
            'Reset': Reset,
            'Paste': Paste,
            'Save': Save,
        }
        self.undo_stack.beginMacro(str(self.undo_stack_macro))

        self.undo_stack.push(commands[command](*args))

        self.undo_stack.endMacro()
        self.undo_stack_macro += 1
