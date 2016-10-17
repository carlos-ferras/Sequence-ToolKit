#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from PyQt5 import QtWidgets, QtGui


class SetValue(QtWidgets.QUndoCommand):
    def __init__(self, current_tab, row, column, value):
        super(SetValue, self).__init__()
        self.current_tab = current_tab
        self.row = row
        self.column = column
        self.value = value

        self.old_value = None
        self.old_foreground = QtGui.QColor(current_tab.getConfiguration('widget_color', 'COMMON'))
        self.old_icon = None

    def redo(self):
        item = self.current_tab.tree_widget.topLevelItem(self.row)

        self.old_value = item.text(self.column)
        self.old_icon = item.icon(self.column)
        foreground = item.foreground(self.column)
        if foreground.color().name() != '#000000':
            self.old_foreground = foreground

        item.setText(self.column, self.value)
        if not self.value:
            item.setForeground(
                self.column, QtGui.QColor(
                    self.current_tab.getConfiguration('widget_color', 'COMMON')
                )
            )
            self.current_tab.quitIcon(self.row, self.column)

    def undo(self):
        item = self.current_tab.tree_widget.topLevelItem(self.row)

        item.setText(self.column, self.old_value)
        item.setForeground(self.column, self.old_foreground)
        item.setIcon(self.column, self.old_icon)


class SetData(QtWidgets.QUndoCommand):
    def __init__(self, current_tab, row, column, value, process_data):
        super(SetData, self).__init__()
        self.current_tab = current_tab
        self.row = row
        self.column = column
        self.process_data = process_data
        self.value = value

        self.old_process_data = False
        self.old_value = ''
        self.old_icon = None
        self.old_foreground = QtGui.QColor(current_tab.getConfiguration('widget_color', 'COMMON'))
        self.is_valid = True

    def redo(self):
        try:
            item = self.current_tab.tree_widget.topLevelItem(self.row)

            if str(self.row) + ',' + str(self.column) in self.current_tab.process_data:
                self.old_process_data = self.current_tab.process_data[str(self.row) + ',' + str(self.column)]
                self.old_value = item.text(self.column)
            self.old_icon = item.icon(self.column)
            foreground = item.foreground(self.column)
            if foreground.color().name() != '#000000':
                self.old_foreground = foreground

            if self.column in self.current_tab.external_irradiation:
                if self.process_data['id'] == 1 or self.process_data['id'] == 0:
                    index = self.current_tab.external_irradiation.index(self.column)
                    if self.current_tab.external_irradiation_defined[index] == self.row:
                        self.current_tab.delete()
                else:
                    self.is_valid = False
                    raise RuntimeError(
                        'This column is locked, because is used for external '
                        'irradiation process.'
                    )
            if self.process_data['id'] == 0:
                for i in range(self.current_tab.tree_widget.topLevelItemCount()):
                    if i == self.row:
                        continue
                    current_item = self.current_tab.tree_widget.topLevelItem(i)
                    if current_item.text(self.column):
                        self.is_valid = False
                        raise RuntimeError(
                            'The irradiation process with external '
                            'source must be set to an empty column.'
                        )
                    if self.current_tab.samplesRepeated():
                        self.is_valid = False
                        raise RuntimeError(
                            'The irradiation process with external source can '
                            'not be defined when a sample appears in more '
                            'than one row.'
                        )
                self.current_tab.external_irradiation.append(self.column)
                self.current_tab.external_irradiation_defined.append(self.row)

            item.setText(self.column, self.value)
            self.current_tab.setIcon(self.row, self.column, 'pend')
            self.current_tab.process_data[str(self.row) + ',' + str(self.column)] = self.process_data
        except Exception as err:
            self.current_tab.show_error_message.emit(str(err))

    def undo(self):
        if self.is_valid:
            item = self.current_tab.tree_widget.topLevelItem(self.row)

            if self.process_data['id'] == 0:
                del self.current_tab.external_irradiation[self.current_tab.external_irradiation.index(self.column)]
                del self.current_tab.external_irradiation_defined[
                    self.current_tab.external_irradiation_defined.index(self.row)
                ]
            if self.old_process_data:
                self.current_tab.process_data[str(self.row) + ',' + str(self.column)] = self.old_process_data
                self.current_tab.tree_widget.topLevelItem(self.row).setIcon(self.column, self.old_icon)
                if self.old_process_data['id'] == 0:
                    self.current_tab.external_irradiation.append(self.column)
                    self.current_tab.external_irradiation_defined.append(self.row)
            else:
                self.current_tab.quitIcon(self.row, self.column)
                del self.current_tab.process_data[str(self.row) + ',' + str(self.column)]

            item.setText(self.column, self.old_value)
            item.setForeground(self.column, self.old_foreground)
