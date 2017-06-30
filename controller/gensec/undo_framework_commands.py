#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from PyQt5 import QtWidgets, QtGui
import pickle

from model.custom_data_type import CustomIndex


class Split(QtWidgets.QUndoCommand):
    def __init__(self, current_tab, processes_to_split):
        super(Split, self).__init__()
        self.current_tab = current_tab
        self.processes_to_split = processes_to_split

        self.group_to_merge = []

    def redo(self):
        delete = []
        for index in self.processes_to_split:
            for group in range(len(self.current_tab.in_merge)):
                for pos in self.current_tab.in_merge[group]:
                    if str(index.row()) + ',' + str(index.column()) == pos:
                        self.current_tab.clearGroupMerge(group)
                        if group not in delete:
                            self.group_to_merge.append(self.current_tab.in_merge[group])
                            delete.insert(0, group)
        self.current_tab.deleteInMerge(delete)

    def undo(self):
        for group in self.group_to_merge:
            index_group = []
            for pos in group:
                row = int(pos.split(',')[0])
                column = int(pos.split(',')[1])
                index_group.append(CustomIndex(row, column))
            self.current_tab.merge(index_group)


class Merge(QtWidgets.QUndoCommand):
    def __init__(self, current_tab, processes_to_merge):
        super(Merge, self).__init__()
        self.current_tab = current_tab
        self.processes_to_merge = processes_to_merge

    def redo(self):
        process_order_id = 0
        in_merge = []
        delete = []
        first = True
        color = self.current_tab.getConfiguration('merge_color_1', 'GENSEC')

        for index in self.processes_to_merge:
            for group in range(len(self.current_tab.in_merge)):
                for poss in self.current_tab.in_merge[group]:
                    if str(index.row()) + ',' + str(index.column()) == poss:
                        self.current_tab.clearGroupMerge(group)
                        if group not in delete:
                            delete.insert(0, group)
        self.current_tab.deleteInMerge(delete)
        for index in self.processes_to_merge:
            in_merge.append(str(index.row()) + ',' + str(index.column()))
            parent_item = self.current_tab.tree_widget.topLevelItem(index.row())
            if first:
                before = str(parent_item.foreground(index.column() - 1).color().name())
                after = str(parent_item.foreground(
                    index.column() + len(self.current_tab.tree_widget.selectedIndexes())
                ).color().name())

                color = self.current_tab.getColor(before, after)
                first = False
            parent_item.setForeground(index.column(), QtGui.QColor(color))
            if not process_order_id:
                process_order_id = self.current_tab.process_data[
                    str(index.row()) + ',' + str(index.column())
                ]['process_order_id']
            else:
                self.current_tab.process_data[str(index.row()) + ',' +
                                              str(index.column())]['process_order_id'] = process_order_id

            self.current_tab.process_data[str(index.row()) + ',' + str(index.column())]['status'] = 'pend'
            self.current_tab.setIcon(index.row(), index.column(), 'pend')

        self.current_tab.in_merge.append(in_merge)

    def undo(self):
        self.current_tab.split(self.processes_to_merge)


class Save(QtWidgets.QUndoCommand):
    def __init__(self, current_tab):
        super(Save, self).__init__()
        self.current_tab = current_tab

    def redo(self):
        self.current_tab.document_saved.emit(self.current_tab)

    def undo(self):
        self.current_tab.document_changed.emit(self.current_tab)


class Paste(QtWidgets.QUndoCommand):
    def __init__(self, current_tab):
        super(Paste, self).__init__()
        self.current_tab = current_tab

        self.first = True
        self.in_irradiation = []
        self.merge_to_delete = []
        self.merge_groups = []

        self.index = None

    def redo(self):
        clipboard = QtWidgets.QApplication.clipboard()
        mime_data = clipboard.mimeData()

        if mime_data.hasFormat('custom_data_type'):
            data_set = pickle.loads(mime_data.data('custom_data_type').data())
            if len(self.current_tab.tree_widget.selectedIndexes()) > 0:
                if self.index is None:
                    self.index = self.current_tab.tree_widget.selectedIndexes()[0]
                if self.index.column() > 1:
                    for group in data_set.custom_data_set:
                        merge_group = []

                        for mime in group:
                            position = mime.position
                            text = mime.text
                            process_data = mime.process_data
                            process_data['status'] = 'pend'

                            current_row = position.row() + self.index.row()
                            current_column = position.column() + self.index.column()
                            last_row = self.current_tab.tree_widget.topLevelItemCount() - 1

                            process_data['process_order_id'] = current_column - 1

                            if current_row > last_row:
                                for k in range(current_row - last_row):
                                    self.current_tab.addRow()
                            if current_column > self.current_tab.column_count:
                                for k in range(current_column - self.current_tab.column_count):
                                    self.current_tab.addColumn()

                            if process_data['id'] == 0:
                                for i in range(self.current_tab.tree_widget.topLevelItemCount()):
                                    if i == current_row:
                                        continue
                                    item = self.current_tab.tree_widget.topLevelItem(i)
                                    if item.text(current_column):
                                        raise RuntimeError(
                                            'The irradiation process with external source must be set to an '
                                            'empty column'
                                        )
                                    if self.current_tab.samplesRepeated():
                                        raise RuntimeError(
                                            'The irradiation process with external source can not be defined '
                                            'when a sample appears in more than one row'
                                        )
                                self.current_tab.external_irradiation.append(current_column)
                                self.current_tab.external_irradiation_defined(current_row)
                            else:
                                if self.index.column() in self.current_tab.external_irradiation:
                                    irradiation_position = self.current_tab.external_irradiation.index(self.index.column())
                                    if self.index.row() == \
                                            self.current_tab.external_irradiation_defined[irradiation_position]:
                                        self.in_irradiation.append((
                                            self.current_tab.external_irradiation[irradiation_position],
                                            self.current_tab.external_irradiation_defined[irradiation_position]
                                        ))
                                        del self.current_tab.external_irradiation[irradiation_position]
                                        del self.current_tab.external_irradiation_defined[irradiation_position]

                            if self.first:
                                self.current_tab.setValue(current_row, current_column, text)
                            self.current_tab.setIcon(current_row, current_column, 'pend')
                            self.current_tab.process_data[str(current_row) + ',' + str(current_column)] = process_data

                            for current_merge_group in range(len(self.current_tab.in_merge)):
                                for poss in self.current_tab.in_merge[current_merge_group]:
                                    if str(self.index.row()) + ',' + str(self.index.column()) == poss:
                                        self.current_tab.clearGroupMerge(current_merge_group)
                                        if current_merge_group not in self.merge_to_delete:
                                            self.merge_to_delete.insert(
                                                0,
                                                self.current_tab.in_merge[current_merge_group]
                                            )

                            if len(group) > 1:
                                merge_group.append(CustomIndex(current_row, current_column))
                        if len(group) > 1:
                            self.current_tab.merge(merge_group)
                            self.merge_groups.append(merge_group)
                    self.current_tab.deleteInMerge(self.merge_to_delete)
        self.first = False

    def undo(self):
        for process in self.in_irradiation:
            self.current_tab.external_irradiation.append(process[0])
            self.current_tab.external_irradiation_defined.append(process[1])

        for group in self.merge_to_delete:
            for_merge = []
            for pos in group:
                row = int(pos.split(',')[0])
                column = int(pos.split(',')[1])
                for_merge.append(CustomIndex(row, column))
            self.current_tab.merge(for_merge)
        self.current_tab.deleteInMerge(self.merge_to_delete)


class Reset(QtWidgets.QUndoCommand):
    def __init__(self, current_tab):
        super(Reset, self).__init__()
        self.current_tab = current_tab

        self.old_sequence_name = None
        self.old_creation_date = None
        self.old_reader_id = None
        self.old_process_data = None
        self.old_icons = []

    def redo(self):
        self.old_sequence_name = self.current_tab.sequence_name
        self.old_creation_date = self.current_tab.creation_date
        self.old_reader_id = self.current_tab.reader_id
        self.old_process_data = self.current_tab.process_data

        self.current_tab.sequence_name = ''
        self.current_tab.creation_date = ''
        self.current_tab.reader_id = 'unknown'
        for data in self.current_tab.process_data.keys():
            self.current_tab.process_data[str(data)]['status'] = 'pend'
            self.current_tab.process_data[str(data)]['curve1'] = ''
            self.current_tab.process_data[str(data)]['curve2'] = ''
            self.current_tab.process_data[str(data)]['curve3'] = ''
            self.current_tab.process_data[str(data)]['time1'] = ''
            self.current_tab.process_data[str(data)]['time2'] = ''
            pos = data.split(',')

            self.old_icons.append(
                self.current_tab.tree_widget.topLevelItem(int(pos[0])).icon(int(pos[1]))
            )

            self.current_tab.setIcon(int(pos[0]), int(pos[1]), 'pend')

    def undo(self):
        self.current_tab.sequence_name = self.old_sequence_name
        self.current_tab.creation_date = self.old_creation_date
        self.current_tab.reader_id = self.old_reader_id

        self.current_tab.process_data = self.old_process_data

        i = 0
        for data in self.current_tab.process_data.keys():
            pos = data.split(',')
            self.current_tab.tree_widget.topLevelItem(int(pos[0])).setIcon(int(pos[1]), self.old_icons[i])
            i += 1


class ClearAll(QtWidgets.QUndoCommand):
    def __init__(self, current_tab):
        super(ClearAll, self).__init__()
        self.current_tab = current_tab

        self.first = True

    def redo(self):
        if self.first:
            for row in range(self.current_tab.tree_widget.topLevelItemCount()):
                item = self.current_tab.tree_widget.topLevelItem(row)
                item.setSelected(True)
            self.current_tab.delete()
            for row in range(self.current_tab.tree_widget.topLevelItemCount()):
                item = self.current_tab.tree_widget.topLevelItem(row)
                item.setSelected(False)
            self.first = False

    def undo(self):
        pass


class Delete(QtWidgets.QUndoCommand):
    def __init__(self, current_tab):
        super(Delete, self).__init__()
        self.current_tab = current_tab

        self.old_processes_data = []
        self.in_irradiation = []
        self.merge_to_delete = []

    def redo(self):
        if self.old_processes_data:
            selected_index = []
            for process in self.old_processes_data:
                selected_index.append(CustomIndex(process[0], process[1]))
        else:
            selected_index = self.current_tab.tree_widget.selectedIndexes()
        for index in selected_index:
            if index.column():
                item = self.current_tab.tree_widget.topLevelItem(index.row())
                if index.column() > 1:
                    try:
                        if str(index.row()) + ',' + str(index.column()) in self.current_tab.process_data:
                            self.old_processes_data.append((
                                index.row(),
                                index.column(),
                                item.text(index.column()),
                                self.current_tab.process_data[str(index.row()) + ',' + str(index.column())],
                                item.icon(index.column())
                            ))

                        del self.current_tab.process_data[str(index.row()) + ',' + str(index.column())]
                        self.current_tab.tree_widget.topLevelItem(index.row()).setText(index.column(), '')
                        self.current_tab.quitIcon(index.row(), index.column())

                        if index.column() in self.current_tab.external_irradiation:
                            irradiation_position = self.current_tab.external_irradiation.index(index.column())
                            if index.row() == self.current_tab.external_irradiation_defined[irradiation_position]:
                                self.in_irradiation.append((
                                    self.current_tab.external_irradiation[irradiation_position],
                                    self.current_tab.external_irradiation_defined[irradiation_position]
                                ))
                                del self.current_tab.external_irradiation[irradiation_position]
                                del self.current_tab.external_irradiation_defined[irradiation_position]

                        for group in range(len(self.current_tab.in_merge)):
                            for poss in self.current_tab.in_merge[group]:
                                if str(index.row()) + ',' + str(index.column()) == poss:
                                    self.current_tab.clearGroupMerge(group)
                                    if group not in self.merge_to_delete:
                                        self.merge_to_delete.insert(0, self.current_tab.in_merge[group])
                    except:
                        pass
                if index.column() == 1:
                    self.old_processes_data.append((
                        index.row(),
                        1,
                        item.text(1),
                        False,
                        False
                    ))
                    self.current_tab.tree_widget.topLevelItem(index.row()).setText(index.column(), '')
        self.current_tab.deleteInMerge(self.merge_to_delete)

    def undo(self):
        for process in self.old_processes_data:
            self.current_tab.tree_widget.topLevelItem(process[0]).setText(process[1], process[2])
            if process[3]:
                self.current_tab.process_data[str(process[0]) + ',' + str(process[1])] = process[3]
                self.current_tab.tree_widget.topLevelItem(process[0]).setIcon(process[1], process[4])

        for process in self.in_irradiation:
            self.current_tab.external_irradiation.append(process[0])
            self.current_tab.external_irradiation_defined.append(process[1])

        for group in self.merge_to_delete:
            for_merge = []
            for pos in group:
                row = int(pos.split(',')[0])
                column = int(pos.split(',')[1])
                for_merge.append(CustomIndex(row, column))
            self.current_tab.merge(for_merge)
        self.current_tab.deleteInMerge(self.merge_to_delete)
