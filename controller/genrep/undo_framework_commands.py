#!/usr/bin/python3
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from PyQt5 import QtWidgets, QtGui
import numpy as np

from model.custom_data_type import CustomIndex


class ApplyTo(QtWidgets.QUndoCommand):
    def __init__(self, controller, filters):
        super(ApplyTo, self).__init__()
        self.controller = controller
        self.filters = filters

        self.old_values = {}

    def redo(self):
        if self.filters:
            to_apply = []
            current_data = self.controller.tab_widget.currentWidget().process_data[
                self.controller.tab_widget.currentWidget().ploting_pos.split(',')[0] +
                ',' +
                self.controller.tab_widget.currentWidget().ploting_pos.split(',')[1]
            ]
            for row in range(self.controller.tab_widget.currentWidget().tree_widget.topLevelItemCount()):
                item = self.controller.tab_widget.currentWidget().tree_widget.topLevelItem(row)
                sample = item.text(1)
                if sample:
                    for column in range(self.controller.tab_widget.currentWidget().column_count)[2:]:
                        if item.text(column):
                            data = self.controller.tab_widget.currentWidget().process_data[str(row) + ',' + str(column)]
                            match = True
                            for filter_ in self.filters:
                                if match:
                                    match = False
                                    data_in_criterion = self.controller.tab_widget.currentWidget().getData(
                                        filter_[0],
                                        data,
                                        sample
                                    )
                                    current_data_in_criterion = self.controller.tab_widget.currentWidget().getData(
                                        filter_[0],
                                        current_data,
                                        self.controller.tab_widget.currentWidget().tree_widget.topLevelItem(
                                            int(self.controller.tab_widget.currentWidget().ploting_pos.split(',')[0])
                                        ).text(1)
                                    )
                                    if data_in_criterion is not None:
                                        if filter_[1] == 1:
                                            if data_in_criterion == current_data_in_criterion:
                                                match = True
                                        elif filter_[1] == 2:
                                            if data_in_criterion != current_data_in_criterion:
                                                match = True
                                        else:
                                            value = filter_[2]
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
                                to_apply.append(str(row) + ',' + str(column))
            for index in to_apply:
                for curve in self.controller.getConfiguration('curve_to_show'):
                    position = index + ',' + str(curve)

                    signal_value = None
                    background_value = None
                    if position in self.controller.tab_widget.currentWidget().signal_values:
                        signal_value = self.controller.tab_widget.currentWidget().signal_values[position]
                    if position in self.controller.tab_widget.currentWidget().background_values:
                        background_value = self.controller.tab_widget.currentWidget().background_values[position]
                    self.old_values[position] = [
                        signal_value,
                        background_value,
                    ]

                    self.controller.saveSignalBackgroundInPos(position)

            if self.controller.tab_widget.currentWidget().process_data:
                self.controller.tabChanged()

    def undo(self):
        for position in self.old_values:
            values = self.old_values[position]
            if values[0] is not None:
                self.controller.tab_widget.currentWidget().signal_values[position] = values[0]
            else:
                del self.controller.tab_widget.currentWidget().signal_values[position]
            if values[1] is not None:
                self.controller.tab_widget.currentWidget().background_values[position] = values[1]
            else:
                del self.controller.tab_widget.currentWidget().background_values[position]

        if self.controller.tab_widget.currentWidget().process_data:
            self.controller.tabChanged()


class ApplyToAll(QtWidgets.QUndoCommand):
    def __init__(self, controller):
        super(ApplyToAll, self).__init__()
        self.controller = controller

        self.old_values = {}

    def redo(self):
        current_widget = self.controller.tab_widget.currentWidget()
        for i in range(current_widget.tree_widget.topLevelItemCount()):
            item = current_widget.tree_widget.topLevelItem(i)
            for column in range(current_widget.column_count)[2:]:
                if item.text(column):
                    data = current_widget.process_data[str(i) + ',' + str(column)]
                    if 1 < data['id'] < 7:
                        for j in self.controller.getConfiguration('curve_to_show'):
                            if data['curve' + str(j)] != '':
                                position = str(i) + ',' + str(column) + ',' + str(j)

                                signal_value = None
                                background_value = None
                                if position in self.controller.tab_widget.currentWidget().signal_values:
                                    signal_value = self.controller.tab_widget.currentWidget().signal_values[position]
                                if position in self.controller.tab_widget.currentWidget().background_values:
                                    background_value = self.controller.tab_widget.currentWidget().background_values[
                                        position]
                                self.old_values[position] = [
                                    signal_value,
                                    background_value,
                                ]

                                self.controller.saveSignalBackgroundInPos(position)
        if current_widget.process_data:
            self.controller.tabChanged()

    def undo(self):
        for position in self.old_values:
            values = self.old_values[position]
            if values[0] is not None:
                self.controller.tab_widget.currentWidget().signal_values[position] = values[0]
            else:
                del self.controller.tab_widget.currentWidget().signal_values[position]
            if values[1] is not None:
                self.controller.tab_widget.currentWidget().background_values[position] = values[1]
            else:
                del self.controller.tab_widget.currentWidget().background_values[position]

        if self.controller.tab_widget.currentWidget().process_data:
            self.controller.tabChanged()


class UpdateSignalLimits(QtWidgets.QUndoCommand):
    def __init__(self, controller, low, high):
        super(UpdateSignalLimits, self).__init__()
        self.controller = controller
        self.low = low
        self.high = high

        self.position = self.controller.tab_widget.currentWidget().ploting_pos
        self.old_values = None
        self.first = True

    def redo(self):
        if (self.old_values is None) and self.position in self.controller.tab_widget.currentWidget().signal_values:
            self.old_values = self.controller.tab_widget.currentWidget().signal_values[self.position]

        low = self.controller.signal_low._strings.index('%.4f' % self.low)
        high = self.controller.signal_high._strings.index('%.4f' % self.high)

        self.controller.signal_low.setValue(low)
        self.controller.signal_high.setValue(high)

        if not self.first:
            self.controller.plot_area.signal_area.setRegion((
                self.low, self.high
            ))
            self.controller.plot_area.updateSignalPlot()
        else:
            self.first = False

        self.controller.updateSignalCount()
        self.controller.saveSignalBackgroundInPos()
        self.controller.tabChanged()

    def undo(self):
        if self.old_values is not None:
            self.controller.tab_widget.currentWidget().signal_values[self.position] = self.old_values

            if self.controller.tab_widget.currentWidget().ploting_pos == self.position:
                self.controller.signal_low.setValue(self.old_values[0] - 1)
                self.controller.signal_high.setValue(self.old_values[1] - 1)

                values = list(self.old_values)

                if self.controller.getConfiguration('horizontal_scale') == 'log':
                    values[0], values[1] = round(10 ** values[0]), round(10 ** values[1])
                elif self.controller.getConfiguration('horizontal_scale') == 'ln':
                    values[0], values[1] = round(np.e ** values[0]), np.e ** round(values[1])

                self.controller.plot_area.signal_area.setRegion((
                    values[0], values[1]
                ))
                self.controller.plot_area.updateSignalPlot()

                self.controller.updateSignalCount()
                self.controller.tabChanged()


class UpdateSignalArea(QtWidgets.QUndoCommand):
    def __init__(self, controller):
        super(UpdateSignalArea, self).__init__()
        self.controller = controller

        self.position = self.controller.tab_widget.currentWidget().ploting_pos
        self.new_values = None
        self.old_values = None

    def redo(self):
        if self.new_values is None:
            self.new_values = (
                self.controller.signal_low.value(),
                self.controller.signal_high.value(),
            )
        else:
            self.controller.signal_low.setValue(self.new_values[0])
            self.controller.signal_high.setValue(self.new_values[1])

        if self.new_values[1] >= self.new_values[0]:
            values = (
                float(self.controller.signal_low._strings[self.new_values[0]]),
                float(self.controller.signal_high._strings[self.new_values[1]])
            )

            if self.controller.getConfiguration('horizontal_scale') == 'log':
                values = tuple(np.log10([values[0], values[1]]))
            elif self.controller.getConfiguration('horizontal_scale') == 'ln':
                values = tuple(np.log([values[0], values[1]]))

            self.controller.plot_area.signal_area.setRegion((
                values[0],
                values[1],
            ))
            self.controller.plot_area.updateSignalPlot()
            if (self.old_values is None) and self.position in self.controller.tab_widget.currentWidget().signal_values:
                self.old_values = self.controller.tab_widget.currentWidget().signal_values[self.position]

            self.controller.updateSignalCount()
            self.controller.saveSignalBackgroundInPos()
            self.controller.tabChanged()

    def undo(self):
        if self.old_values is not None:
            self.controller.tab_widget.currentWidget().signal_values[self.position] = self.old_values

            if self.controller.tab_widget.currentWidget().ploting_pos == self.position:
                values = self.old_values

                if self.controller.getConfiguration('horizontal_scale') == 'log':
                    values = tuple(np.log10([values[0], values[1]]))
                elif self.controller.getConfiguration('horizontal_scale') == 'ln':
                    values = tuple(np.log([values[0], values[1]]))

                self.controller.plot_area.signal_area.setRegion((
                    values[0],
                    values[1],
                ))
                self.controller.plot_area.updateSignalPlot()

                self.controller.signal_low.setValue(self.old_values[0] - 1)
                self.controller.signal_high.setValue(self.old_values[1] - 1)

                self.controller.updateSignalCount()
                self.controller.tabChanged()


class UpdateBackgroundLimits(QtWidgets.QUndoCommand):
    def __init__(self, controller, low, high):
        super(UpdateBackgroundLimits, self).__init__()
        self.controller = controller
        self.low = low
        self.high = high

        self.position = self.controller.tab_widget.currentWidget().ploting_pos
        self.old_values = None
        self.first = True

    def redo(self):
        if (self.old_values is None) and self.position in self.controller.tab_widget.currentWidget().background_values:
            self.old_values = self.controller.tab_widget.currentWidget().background_values[self.position]

        low = self.controller.background_low._strings.index('%.4f' % self.low)
        high = self.controller.background_high._strings.index('%.4f' % self.high)

        self.controller.background_low.setValue(low)
        self.controller.background_high.setValue(high)

        if not self.first:
            self.controller.plot_area.background_area.setRegion((
                self.low, self.high
            ))
            self.controller.plot_area.updateBackgroundPlot()
        else:
            self.first = False

        self.controller.updateBackgroundCount()
        self.controller.saveSignalBackgroundInPos()
        self.controller.tabChanged()

    def undo(self):
        if self.old_values is not None:
            self.controller.tab_widget.currentWidget().background_values[self.position] = self.old_values

            if self.controller.tab_widget.currentWidget().ploting_pos == self.position:
                self.controller.background_low.setValue(self.old_values[0] - 1)
                self.controller.background_high.setValue(self.old_values[1] - 1)

                values = self.old_values

                if self.controller.getConfiguration('horizontal_scale') == 'log':
                    values[0], values[1] = round(10 ** values[0]), round(10 ** values[1])
                elif self.controller.getConfiguration('horizontal_scale') == 'ln':
                    values[0], values[1] = round(np.e ** values[0]), round(np.e ** values[1])

                self.controller.plot_area.background_area.setRegion((
                    values[0], values[1]
                ))
                self.controller.plot_area.updateBackgroundPlot()

                self.controller.updateBackgroundCount()
                self.controller.tabChanged()


class UpdateBackgroundArea(QtWidgets.QUndoCommand):
    def __init__(self, controller):
        super(UpdateBackgroundArea, self).__init__()
        self.controller = controller

        self.position = self.controller.tab_widget.currentWidget().ploting_pos
        self.new_values = None
        self.old_values = None

    def redo(self):
        if self.new_values is None:
            self.new_values = (
                self.controller.background_low.value(),
                self.controller.background_high.value(),
            )
        else:
            self.controller.background_low.setValue(self.new_values[0])
            self.controller.background_high.setValue(self.new_values[1])

        if self.new_values[1] >= self.new_values[0]:
            values = (
                float(self.controller.background_low._strings[self.new_values[0]]),
                float(self.controller.background_high._strings[self.new_values[1]])
            )

            if self.controller.getConfiguration('horizontal_scale') == 'log':
                values = tuple(np.log10([values[0], values[1]]))
            elif self.controller.getConfiguration('horizontal_scale') == 'ln':
                values = tuple(np.log([values[0], values[1]]))

            self.controller.plot_area.background_area.setRegion((
                values[0],
                values[1],
            ))
            self.controller.plot_area.updateBackgroundPlot()
            if (self.old_values is None) and self.position in self.controller.tab_widget.currentWidget().background_values:
                self.old_values = self.controller.tab_widget.currentWidget().background_values[self.position]

            self.controller.updateBackgroundCount()
            self.controller.saveSignalBackgroundInPos()
            self.controller.tabChanged()

    def undo(self):
        if self.old_values is not None:
            self.controller.tab_widget.currentWidget().background_values[self.position] = self.old_values

            if self.controller.tab_widget.currentWidget().ploting_pos == self.position:
                values = self.old_values

                if self.controller.getConfiguration('horizontal_scale') == 'log':
                    values = tuple(np.log10([values[0], values[1]]))
                elif self.controller.getConfiguration('horizontal_scale') == 'ln':
                    values = tuple(np.log([values[0], values[1]]))

                self.controller.plot_area.background_area.setRegion((
                    values[0],
                    values[1],
                ))
                self.controller.plot_area.updateBackgroundPlot()

                self.controller.background_low.setValue(self.old_values[0] - 1)
                self.controller.background_high.setValue(self.old_values[1] - 1)

                self.controller.updateBackgroundCount()
                self.controller.tabChanged()


class Save(QtWidgets.QUndoCommand):
    def __init__(self, current_tab):
        super(Save, self).__init__()
        self.current_tab = current_tab

    def redo(self):
        self.current_tab.document_saved.emit(self.current_tab)

    def undo(self):
        self.current_tab.document_changed.emit(self.current_tab)


class UngroupAll(QtWidgets.QUndoCommand):
    def __init__(self, current_tab):
        super(UngroupAll, self).__init__()
        self.current_tab = current_tab

    def redo(self):
        to_ungroup = []
        for group in self.current_tab.in_group:
            to_ungroup.append(
                CustomIndex(
                    group[0].split(',')[0],
                    group[0].split(',')[1]
                )
            )
        self.current_tab.ungroup(to_ungroup)

    def undo(self):
        pass


class Ungroup(QtWidgets.QUndoCommand):
    def __init__(self, current_tab, processes_to_ungroup):
        super(Ungroup, self).__init__()
        self.current_tab = current_tab
        self.processes_to_ungroup = processes_to_ungroup

        self.processes_to_group = []

    def redo(self):
        delete = []
        for index in self.processes_to_ungroup:
            for group in range(len(self.current_tab.in_group)):
                for pos in self.current_tab.in_group[group]:
                    if str(index.row()) + ',' + str(index.column()) == pos:
                        self.current_tab.clearGroupAssociation(group)
                        if group not in delete:
                            self.processes_to_group.append(self.current_tab.in_group[group])
                            delete.insert(0, group)
        self.current_tab.deleteInGroup(delete)

    def undo(self):
        for group in self.processes_to_group:
            index_group = []
            for pos in group:
                row = int(pos.split(',')[0])
                column = int(pos.split(',')[1])
                index_group.append(CustomIndex(row, column))
            self.current_tab.group(index_group)


class Group(QtWidgets.QUndoCommand):
    def __init__(self, current_tab, processes_to_group):
        super(Group, self).__init__()
        self.current_tab = current_tab
        self.processes_to_group = processes_to_group

    def redo(self):
        in_group = []
        delete = []
        first = True
        color = self.current_tab.getConfiguration('association_color_1', 'GENREP')

        for index in self.processes_to_group:
            for group in range(len(self.current_tab.in_group)):
                for poss in self.current_tab.in_group[group]:
                    if str(index.row()) + ',' + str(index.column()) == poss:
                        self.current_tab.clearGroupAssociation(group)
                        if group not in delete:
                            delete.insert(0, group)
        self.current_tab.deleteInGroup(delete)
        for index in self.processes_to_group:
            in_group.append(str(index.row()) + ',' + str(index.column()))
            parent_item = self.current_tab.tree_widget.topLevelItem(index.row())
            if first:
                before = str(parent_item.background(index.column() - 1).color().name())
                after = str(parent_item.background(index.column() + len(self.current_tab.tree_widget.selectedIndexes())).color().name())

                color = self.current_tab.getGroupColor(before, after)
                first = False
            parent_item.setBackground(index.column(), QtGui.QColor(color))
        self.current_tab.in_group.append(in_group)

    def undo(self):
        self.current_tab.ungroup(self.processes_to_group)
