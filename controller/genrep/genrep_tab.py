#!/usr/bin/python3
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import os
from datetime import datetime
import tempfile
from functools import partial

from PyQt5 import QtWidgets, QtCore, QtGui, QtPrintSupport

import img_rc
from controller.widgets.treewidget_tab import TreeWidgetTab
from controller.widgets.undo_framework_commands import SetValue, SetData
from controller.genrep.undo_framework_commands import Save, Group, Ungroup, UngroupAll
from model.handle_rlf import CreateRLF
from controller.genrep.plot import PlotWidget
from controller.decorators import loadingCursor


class GenRepTab(TreeWidgetTab):
    show_success_message = QtCore.pyqtSignal(str)
    show_info_message = QtCore.pyqtSignal(str)
    show_error_message = QtCore.pyqtSignal(str)
    document_changed = QtCore.pyqtSignal(QtWidgets.QWidget)
    document_saved = QtCore.pyqtSignal(QtWidgets.QWidget)

    def __init__(self, profile_parameters, parent=None):
        TreeWidgetTab.__init__(self, parent)

        self.working_slf = None
        self.in_group = []
        self.selected_row = None
        self.ploting_pos = None
        self.signal_values = {}
        self.background_values = {}
        self.samples_amount = 0
        self.status = None

        self.profile_parameters = profile_parameters

        self.action_group.triggered.connect(self.group)
        self.action_ungroup.triggered.connect(self.ungroup)
        self.action_select_row.triggered.connect(self.selectRow)
        self.undo_stack.canUndoChanged.connect(self.undoRedoChange)
        self.undo_stack.canRedoChanged.connect(self.undoRedoChange)

    def itemSelectionChanged(self):
        try:
            can_group = self.areConsecutive() or not self.getConfiguration('consecutive', 'GENREP')
            can_ungroup = False

            for item in self.tree_widget.selectedIndexes():
                for group in range(len(self.in_group)):
                    for poss in self.in_group[group]:
                        if str(item.row()) + ',' + str(item.column()) == poss:
                            can_ungroup = True

            parent_windows = self.parent().parent().parent().parent()
            parent_windows.findChild(QtWidgets.QAction, "action_group").setEnabled(can_group)
            parent_windows.findChild(QtWidgets.QAction, "action_ungroup").setEnabled(can_ungroup)
        except:
            pass

    @loadingCursor()
    def save(self, path):
        if path.endswith('.rlf') or path.endswith('.xml'):
            report = self.createRLF()
            report.save(path, True)
        elif path.endswith('.txt'):
            self.createTXT(path)
        self.runCommand('Save', self)

    def print(self):
        printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
        printer.setOutputFormat(QtPrintSupport.QPrinter.PdfFormat)
        printer.setOutputFileName(
            os.path.join(
                self.getConfiguration('default_file_location', 'COMMON'),
                'report_' + str(datetime.now()) + '.pdf'
            )
        )

        dialog = QtPrintSupport.QPrintDialog(printer, self)
        dialog.setWindowTitle(QtCore.QCoreApplication.translate('tree_widget_tab', 'Print Table View'))

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            text_document = QtGui.QTextDocument()
            text_document.setHtml(self.buildHtml())
            text_document.print_(printer)

    def getPlotImg(self, data, name):
        x_values = data[4]
        y_values = data[5]
        low_signal = x_values.index(data[0][0])
        high_signal = x_values.index(data[0][1])
        low_background = x_values.index(data[1][0])
        high_background = x_values.index(data[1][1])
        default = True

        plot = PlotWidget()
        plot.main_layout.layout.setColumnFixedWidth(2, 600)
        plot.main_layout.layout.setColumnMaximumWidth(2, 600)
        plot.main_layout.layout.setColumnMinimumWidth(2, 600)
        plot.resize(1170,480)

        plot.updatePlot(
            x_values,
            y_values,
            ls=low_signal,
            hs=high_signal,
            lb=low_background,
            hb=high_background,
            default=default
        )
        plot.drawTheme()

        tmp_path = tempfile.gettempdir()
        path = os.path.join(tmp_path, str(name) + '.png')
        img = plot.export(path)

        return path

    @loadingCursor(empty=True)
    def buildHtml(self):
        sequence_datetime = '<table><tr><td><b>GenRep: </b>' + \
                            str(datetime.now()) +\
                            '</td></tr></table><hr>'

        sequence_global = '<table style="margin-top:15px; margin-bottom: 25px;"><tr><td>' + \
                          QtCore.QCoreApplication.translate('tree_widget_tab', 'Name') + \
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
                          ': </td><td>' + self.reader_id + '</td></tr></table>'

        html = ''
        img_name = 1
        table = self.getSampleCommands()
        parameters = self.getConfiguration('parameters', 'GENREP')
        for row in table:
            samples = row[0]
            sample_list = samples.split(',')
            for sample in sample_list:
                if len(sample) == 1:
                    samples_ids = sample
                elif len(sample) > 1:
                    sample_range = sample.split('-')
                    samples_ids = range(int(sample_range[0]), int(sample_range[-1]) + 1)
                for id_ in samples_ids:
                    sample_table = '<p style="background:#d1d1d1"><b>' + \
                                   QtCore.QCoreApplication.translate('tree_widget_tab', 'Sample') + ' ' +\
                                   str(id_) + '</b></p>'

                    for command in row[1]:
                        curves_amount = tuple(command[1].keys())
                        if curves_amount:
                            position = curves_amount[0][:-2]
                            data = self.process_data[position]
                            if data['id'] == 2:
                                process = 'TL'
                            if data['id'] == 3:
                                process = 'OSL'
                            if data['id'] == 4:
                                process = 'POSL'
                            if data['id'] == 5:
                                process = 'LMOSL'
                            if data['id'] == 6:
                                process = 'ESL'
                            command_table = '<table style="margin-bottom: 10px;">' \
                                            '<tr style="font-weight: bold;" colspan="3"><td>' + \
                                            QtCore.QCoreApplication.translate('tree_widget_tab', 'Process') + ' ' +\
                                            process + '</td></tr>' \
                                            '<tr><td>' +\
                                            QtCore.QCoreApplication.translate('tree_widget_tab', 'Parameter') +\
                                            '</td><td style="padding-left:30px;">' +\
                                            QtCore.QCoreApplication.translate('tree_widget_tab', 'Data') +\
                                            '</td><td style="padding-left: 30px;">Plot</td></tr>' \
                                            '<tr><td>' +\
                                            QtCore.QCoreApplication.translate('tree_widget_tab', 'Date Type') +\
                                            '</td><td style="padding-left:30px;">' + str(data['date_type']) + \
                                            '</td><td></td></tr>'

                            curves = {1: False, 2: False, 3: False}
                            for curve in command[1]:
                                curv = int(curve.split(',')[2])
                                path = self.getPlotImg(command[1][curve], img_name)
                                curve_data = '<tr><td>Curve ' + \
                                             '</td><td> </td><td style="padding-left: 20px;" rowspan="7"><img src="' + \
                                             path + \
                                             '" width="320"></td></tr>'
                                if self.getConfiguration('signal_active', 'GENREP'):
                                    curve_data += \
                                        '<tr><td style="padding-left:15px;">' +\
                                        QtCore.QCoreApplication.translate('tree_widget_tab', 'Signal Count') +\
                                        '</td><td style="padding-left:30px;">' + \
                                        str(command[1][curve][2]) + \
                                        '</td></tr>' \
                                        '<tr><td style="padding-left:15px;">' +\
                                        QtCore.QCoreApplication.translate('tree_widget_tab', 'Signal Min Channel') +\
                                        '</td><td style="padding-left:30px;">' + \
                                        str(command[1][curve][0][0]) + \
                                        '</td></tr>' \
                                        '<tr><td style="padding-left:15px;">' +\
                                        QtCore.QCoreApplication.translate('tree_widget_tab', 'Signal Max Channel') +\
                                        '</td><td style="padding-left:30px;">' + \
                                        str(command[1][curve][0][1]) + \
                                        '</td></tr>'
                                if self.getConfiguration('background_active', 'GENREP'):
                                    curve_data += \
                                        '<tr><td style="padding-left:15px;">' +\
                                        QtCore.QCoreApplication.translate('tree_widget_tab', 'Background Count') +\
                                        '</td><td style="padding-left:30px;">' + \
                                        str(command[1][curve][3]) + \
                                        '</td></tr>' \
                                        '<tr><td style="padding-left:15px;">' +\
                                        QtCore.QCoreApplication.translate('tree_widget_tab', 'Background Min Channel') +\
                                        '</td><td style="padding-left:30px;">' + \
                                        str(command[1][curve][1][0]) + \
                                        '</td></tr>' \
                                        '<tr><td style="padding-left:15px;">' +\
                                        QtCore.QCoreApplication.translate('tree_widget_tab', 'Background Max Channel') +\
                                        '</td><td style="padding-left:30px;">' + \
                                        str(command[1][curve][1][1]) + \
                                        '</td></tr>'
                                img_name += 1
                                curves[int(curv)] = curve_data

                            for curve_data in curves:
                                if curves[curve_data]:
                                    command_table += curves[curve_data]

                            cleaned_data = {}
                            position = curves_amount[0][:-2]
                            for group in self.in_group:
                                if position in group:
                                    for position_2 in (y for y in group if y != position):
                                        data = self.process_data[position_2]

                                        if data['id'] == 0:
                                            if 2 in parameters:
                                                cleaned_data[self.profile_parameters[2]] = self.getData(5, data, None)
                                            if 3 in parameters:
                                                cleaned_data[self.profile_parameters[3]] = self.getData(6, data, None)
                                            if 11 in parameters:
                                                cleaned_data[self.profile_parameters[11]] = self.getData(14, data, None)
                                        if data['id'] == 1:
                                            if 0 in parameters:
                                                cleaned_data[self.profile_parameters[0]] = self.getData(3, data, None)
                                            if 1 in parameters:
                                                cleaned_data[self.profile_parameters[1]] = self.getData(4, data, None)
                                            if 10 in parameters:
                                                cleaned_data[self.profile_parameters[10]] = self.getData(13, data, None)
                                        if data['id'] == 7:
                                            if 4 in parameters:
                                                cleaned_data[self.profile_parameters[4]] = self.getData(7, data, None)
                                            if 6 in parameters:
                                                cleaned_data[self.profile_parameters[6]] = self.getData(9, data, None)
                                        if data['id'] == 8:
                                            if 13 in parameters:
                                                cleaned_data[self.profile_parameters[13]] = self.getData(16, data, None)
                                            if 14 in parameters:
                                                cleaned_data[self.profile_parameters[14]] = self.getData(17, data, None)
                                            if 15 in parameters:
                                                cleaned_data[self.profile_parameters[15]] = self.getData(18, data, None)
                                    break

                            data = self.process_data[position]
                            if data['id'] == 3 or data['id'] == 4 or data['id'] == 5:
                                if 8 in parameters:
                                    cleaned_data[self.profile_parameters[8]] = self.getData(11, data, None)
                                if 9 in parameters:
                                    cleaned_data[self.profile_parameters[9]] = self.getData(12, data, None)
                            if data['id'] == 6:
                                if 16 in parameters:
                                    cleaned_data[self.profile_parameters[16]] = self.getData(19, data, None)
                                if 17 in parameters:
                                    cleaned_data[self.profile_parameters[17]] = self.getData(20, data, None)
                            if 5 in parameters:
                                cleaned_data[self.profile_parameters[5]] = self.getData(8, data, None)
                            if 7 in parameters:
                                cleaned_data[self.profile_parameters[7]] = self.getData(10, data, None)
                            if 11 in parameters:
                                cleaned_data[self.profile_parameters[11]] = self.getData(14, data, None)

                            for entry in cleaned_data:
                                if cleaned_data[entry] is None:
                                    cleaned_data[entry] = '-'
                                command_table += '<tr><td>' + \
                                                 entry + \
                                                 '</td><td style="padding-left:30px;">' + \
                                                 str(cleaned_data[entry]) + \
                                                 '</td><td></td></tr>'
                            command_table += '</table>'
                            sample_table += command_table
                    html += sample_table
        html = sequence_datetime + sequence_global + html
        return html

    def createTXT(self, path):
        header = (
            QtCore.QCoreApplication.translate('tree_widget_tab', 'Sequence Name') + '\t' + self.sequence_name +
            '\n' + QtCore.QCoreApplication.translate('tree_widget_tab', 'Owner') + '\t' + self.sequence_owner +
            '\n' + QtCore.QCoreApplication.translate('tree_widget_tab', 'Created') + '\t' + str(self.creation_date) +
            '\n' + QtCore.QCoreApplication.translate('tree_widget_tab', 'Modified') + '\t' + str(self.modification_date) +
            '\n' + QtCore.QCoreApplication.translate('tree_widget_tab', 'Status') + '\t' + str(self.status) +
            '\n' + QtCore.QCoreApplication.translate('tree_widget_tab', 'Amount of Samples') + '\t' + str(self.samples_amount) +
            '\n' + QtCore.QCoreApplication.translate('tree_widget_tab', 'Nitrogen Use') + '\t' + str(self.nitrogen_use) +
            '\n' + QtCore.QCoreApplication.translate('tree_widget_tab', 'Dose Rate') + '\t' + str(self.dose_rate) +
            '\n' + QtCore.QCoreApplication.translate('tree_widget_tab', 'External Dose Rate') + '\t' + str(self.external_dose_rate) +
            '\n' + QtCore.QCoreApplication.translate('tree_widget_tab', 'Protocol') + '\t' + str(self.protocol) +
            '\n' + QtCore.QCoreApplication.translate('tree_widget_tab', 'Reader ID') + '\t' + str(self.reader_id) + '\n'
        )

        body = ''
        table = self.getSampleCommands()
        parameters = self.getConfiguration('parameters', 'GENREP')
        for row in table:
            samples = row[0]
            sample_list = samples.split(',')
            for sample in sample_list:
                if len(sample) == 1:
                    samples_ids = sample
                elif len(sample) > 1:
                    sample_range = sample.split('-')
                    samples_ids = range(int(sample_range[0]), int(sample_range[-1]) + 1)
                for id_ in samples_ids:
                    sample_table = '\n\n' + QtCore.QCoreApplication.translate('tree_widget_tab', 'Sample') + '\t' + str(id_)

                    for command in row[1]:
                        curves_amount = tuple(command[1].keys())
                        if curves_amount:
                            position = curves_amount[0][:-2]
                            data = self.process_data[position]
                            if data['id'] == 2:
                                process = 'TL'
                            if data['id'] == 3:
                                process = 'OSL'
                            if data['id'] == 4:
                                process = 'POSL'
                            if data['id'] == 5:
                                process = 'LMOSL'
                            if data['id'] == 6:
                                process = 'ESL'

                            command_table = (
                                '\n\n' + QtCore.QCoreApplication.translate('tree_widget_tab', 'Process') + '\t' + process +
                                '\n' + QtCore.QCoreApplication.translate('tree_widget_tab', 'Data Type') + '\t' + str(data['date_type']) +
                                '\n' + QtCore.QCoreApplication.translate('tree_widget_tab', 'Time Per Channel') + '\t' + str(data['timePerChannel'])
                            )

                            cleaned_data = {}
                            for group in self.in_group:
                                if position in group:
                                    for position_2 in (y for y in group if y != position):
                                        data = self.process_data[position_2]

                                        if data['id'] == 0:
                                            if 2 in parameters:
                                                cleaned_data[self.profile_parameters[2]] = self.getData(5, data, None)
                                            if 3 in parameters:
                                                cleaned_data[self.profile_parameters[3]] = self.getData(6, data, None)
                                            if 11 in parameters:
                                                cleaned_data[self.profile_parameters[11]] = self.getData(14, data, None)
                                        if data['id'] == 1:
                                            if 0 in parameters:
                                                cleaned_data[self.profile_parameters[0]] = self.getData(3, data, None)
                                            if 1 in parameters:
                                                cleaned_data[self.profile_parameters[1]] = self.getData(4, data, None)
                                            if 10 in parameters:
                                                cleaned_data[self.profile_parameters[10]] = self.getData(13, data, None)
                                        if data['id'] == 7:
                                            if 4 in parameters:
                                                cleaned_data[self.profile_parameters[4]] = self.getData(7, data, None)
                                            if 6 in parameters:
                                                cleaned_data[self.profile_parameters[6]] = self.getData(9, data, None)
                                        if data['id'] == 8:
                                            if 13 in parameters:
                                                cleaned_data[self.profile_parameters[13]] = self.getData(16, data, None)
                                            if 14 in parameters:
                                                cleaned_data[self.profile_parameters[14]] = self.getData(17, data, None)
                                            if 15 in parameters:
                                                cleaned_data[self.profile_parameters[15]] = self.getData(18, data, None)
                                    break

                            data = self.process_data[position]
                            if data['id'] == 3 or data['id'] == 4 or data['id'] == 5:
                                if 8 in parameters:
                                    cleaned_data[self.profile_parameters[8]] = self.getData(11, data, None)
                                if 9 in parameters:
                                    cleaned_data[self.profile_parameters[9]] = self.getData(12, data, None)
                            if data['id'] == 6:
                                if 16 in parameters:
                                    cleaned_data[self.profile_parameters[16]] = self.getData(19, data, None)
                                if 17 in parameters:
                                    cleaned_data[self.profile_parameters[17]] = self.getData(20, data, None)
                            if 5 in parameters:
                                cleaned_data[self.profile_parameters[5]] = self.getData(8, data, None)
                            if 7 in parameters:
                                cleaned_data[self.profile_parameters[7]] = self.getData(10, data, None)
                            if 11 in parameters:
                                cleaned_data[self.profile_parameters[11]] = self.getData(14, data, None)

                            for entry in cleaned_data:
                                if cleaned_data[entry] is None:
                                    cleaned_data[entry] = '-'
                                command_table += '\n' + entry + '\t' + str(cleaned_data[entry])

                            curves = {1: False, 2: False, 3: False}
                            for curve in command[1]:
                                curv = int(curve.split(',')[2])
                                curve_data = []
                                if self.getConfiguration('signal_active', 'GENREP'):
                                    curve_data += [
                                        str(command[1][curve][2]),
                                        str(command[1][curve][0][0]),
                                        str(command[1][curve][0][1])
                                    ]
                                if self.getConfiguration('background_active', 'GENREP'):
                                    curve_data += [
                                        str(command[1][curve][3]),
                                        str(command[1][curve][1][0]),
                                        str(command[1][curve][1][1])
                                    ]
                                curve_data += [str(command[1][curve][5])[1:-1]]
                                curves[int(curv)] = curve_data

                            command_table += '\n' + QtCore.QCoreApplication.translate('tree_widget_tab', 'Curve')
                            if self.getConfiguration('signal_active', 'GENREP'):
                                command_table += '\t' + QtCore.QCoreApplication.translate('tree_widget_tab', 'Signal Count') +\
                                                '\t' + QtCore.QCoreApplication.translate('tree_widget_tab', 'Signal Min Channel') +\
                                                '\t' + QtCore.QCoreApplication.translate('tree_widget_tab', 'Signal Max Channel')
                            if self.getConfiguration('background_active', 'GENREP'):
                                command_table += '\t' + QtCore.QCoreApplication.translate('tree_widget_tab', 'Background Count') +\
                                                '\t' + QtCore.QCoreApplication.translate('tree_widget_tab', 'Background Min Channel') +\
                                                '\t' + QtCore.QCoreApplication.translate('tree_widget_tab', 'Background Max Channel')
                            command_table += '\t' + QtCore.QCoreApplication.translate('tree_widget_tab', 'Data')
                            for curve_data in curves:
                                if curves[curve_data]:
                                    command_table += '\n' + str(curve_data)
                                    for value in curves[curve_data]:
                                        command_table += '\t' + value

                            sample_table += command_table + '\n'
                    body += sample_table
        txt_file = open(path, 'w+')
        txt_file.write(header + body)
        txt_file.close()

    def createRLF(self):
        table = self.getSampleCommands()
        report = CreateRLF(
            samples_amount=self.samples_amount,
            name=self.sequence_name,
            owner=self.sequence_owner,
            nitrogen_use=self.nitrogen_use,
            dose_rate=self.dose_rate,
            external_dose_rate=self.external_dose_rate,
            protocol=self.protocol,
            status=self.status,
            reader_id=self.reader_id,
            datecrea=None
        )
        parameters = self.getConfiguration('parameters', 'GENREP')
        for row in table:
            samples = row[0]
            sample_list = samples.split(',')
            for sample in sample_list:
                if len(sample) == 1:
                    samples_ids = sample
                elif len(sample) > 1:
                    sample_range = sample.split('-')
                    samples_ids = range(int(sample_range[0]), int(sample_range[-1]) + 1)
                for id_ in samples_ids:
                    sample_id = report.createSample(id_)
                    process_order_id = 1
                    for command in row[1]:
                        curves_amount = tuple(command[1].keys())
                        if curves_amount:
                            curves = []
                            for curve in command[1]:
                                curve_num = int(curve.split(',')[2])
                                curves.append(
                                    report.createCurve(
                                        curve_num,
                                        self.getConfiguration('signal_active', 'GENREP'),
                                        self.getConfiguration('background_active', 'GENREP'),
                                        command[1][curve][2],
                                        command[1][curve][0][0],
                                        command[1][curve][0][1],
                                        command[1][curve][3],
                                        command[1][curve][1][0],
                                        command[1][curve][1][1]
                                    )
                                )
                            cleaned_data = {}
                            position = curves_amount[0][:-2]
                            for group in self.in_group:
                                if position in group:
                                    for position_2 in (y for y in group if y != position):
                                        data = self.process_data[position_2]

                                        if data['id'] == 0:
                                            if 2 in parameters:
                                                cleaned_data['External_irradiation'] = self.getData(5, data, None)
                                            if 3 in parameters:
                                                cleaned_data['External_dose'] = self.getData(6, data, None)
                                            if 11 in parameters:
                                                cleaned_data['Time_external_irradiation'] = self.getData(14, data, None)
                                        if data['id'] == 1:
                                            if 0 in parameters:
                                                cleaned_data['Beta_irradiation_time'] = self.getData(3, data, None)
                                            if 1 in parameters:
                                                cleaned_data['Beta_dose'] = self.getData(4, data, None)
                                            if 10 in parameters:
                                                cleaned_data['Time_beta_irradiation'] = self.getData(13, data, None)
                                        if data['id'] == 7:
                                            if 4 in parameters:
                                                cleaned_data['Preheating_temperature'] = self.getData(7, data, None)
                                            if 6 in parameters:
                                                cleaned_data['Preheating_rate'] = self.getData(9, data, None)
                                        if data['id'] == 8:
                                            if 13 in parameters:
                                                cleaned_data['Illumination_source'] = self.getData(16, data, None)
                                            if 14 in parameters:
                                                cleaned_data['Illumination_power'] = self.getData(17, data, None)
                                            if 15 in parameters:
                                                cleaned_data['Illumination_temperature'] = self.getData(18, data, None)
                                    break

                            data = self.process_data[position]
                            if data['id'] == 3 or data['id'] == 4 or data['id'] == 5:
                                if 8 in parameters:
                                    cleaned_data['Light_source'] = self.getData(11, data, None)
                                if 9 in parameters:
                                    cleaned_data['Optical_power'] = self.getData(12, data, None)
                            if data['id'] == 6:
                                if 16 in parameters:
                                    cleaned_data['Electric_stimulation'] = self.getData(19, data, None)
                                if 17 in parameters:
                                    cleaned_data['Electric_frequency'] = self.getData(20, data, None)
                            if 5 in parameters:
                                cleaned_data['Measuring_temperature'] = self.getData(8, data, None)
                            if 7 in parameters:
                                cleaned_data['Heating_rate'] = self.getData(10, data, None)
                            if 11 in parameters:
                                cleaned_data['Time_external_irradiation'] = self.getData(14, data, None)

                            if data['id'] in (2, 3, 4, 5, 6):
                                cleaned_data['Time_per_channel'] = data['timePerChannel']

                            if data['id'] == 2:
                                process = 'TL'
                            if data['id'] == 3:
                                process = 'OSL'
                            if data['id'] == 4:
                                process = 'POSL'
                            if data['id'] == 5:
                                process = 'LMOSL'
                            if data['id'] == 6:
                                process = 'ESL'

                            report.createProcessOrder(
                                sample_id,
                                process_order_id,
                                process,
                                data['date_type'],
                                curves,
                                cleaned_data
                            )
                            process_order_id += 1
        return report

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
                        if 1 < process_data['id'] < 7:
                            curves = {}
                            for curve in self.getConfiguration('curve_to_show', 'GENREP'):
                                if process_data['curve' + str(curve)] != '':
                                    signal_range = [None, None]
                                    background_range = [None, None]

                                    x_values, y_values = self.valuesOf(row, column, str(curve))

                                    if str(row) + ',' + str(column) + ',' + str(curve) in self.signal_values.keys():
                                        signal_values = self.signal_values[str(row) + ',' + str(column) + ',' + str(curve)]
                                        background_values = self.background_values[str(row) + ',' + str(column) + ',' + str(curve)]
                                    else:
                                        signal_values = [
                                            x_values[int(self.getConfiguration('low_signal', 'GENREP') - 1)],
                                            x_values[int(self.getConfiguration('high_signal', 'GENREP'))]
                                        ]
                                        if self.getConfiguration('high_background', 'GENREP') == 0:
                                            high_background = len(x_values) - 1
                                        else:
                                            high_background = int(self.getConfiguration('high_background', 'GENREP'))
                                        background_values = [
                                            x_values[int(self.getConfiguration('low_background', 'GENREP'))],
                                            x_values[high_background]
                                        ]

                                    signal_range[0] = int(x_values.index(signal_values[0]))
                                    signal_range[1] = int(x_values.index(signal_values[1]) + 1)
                                    background_range[0] = int(x_values.index(background_values[0]))
                                    background_range[1] = int(x_values.index(background_values[1]) + 1)

                                    signal = y_values[signal_range[0]:signal_range[1]]
                                    background = y_values[background_range[0]:background_range[1]]

                                    signal_count = 0
                                    background_count = 0

                                    for k in signal:
                                        signal_count += k
                                    for k in background:
                                        background_count += k

                                    curves[str(row) + ',' + str(column) + ',' + str(curve)] = [
                                        signal_values,
                                        background_values,
                                        signal_count,
                                        background_count,
                                        x_values,
                                        y_values
                                    ]
                            sample[1].append((process_data, curves))
                samples.append(sample)
        return samples

    def getData(self, filter_, data, sample):
        try:
            if filter_ == 0:
                return sample
            elif filter_ == 1:
                return float(data['process_order_id'])
            elif filter_ == 2:
                return data['date_type']
            elif filter_ == 3 and data['id'] == 1:
                return float(data['time'])
            elif filter_ == 4 and data['id'] == 1:
                return float(data['time']) * float(self.dose_rate)
            elif filter_ == 5 and data['id'] == 0:
                return float(data['time'])
            elif filter_ == 6 and data['id'] == 0:
                return float(data['time']) * float(self.external_dose_rate)
            elif filter_ == 7 and data['id'] == 7:
                return float(data['final_temp'])
            elif filter_ == 8 and (data['id'] == 2 or data['id'] == 3 or data['id'] == 4 or data['id'] == 5 or
                                   data['id'] == 6):
                return float(data['final_temp'])
            elif filter_ == 9 and data['id'] == 7:
                return float(data['heating_rate'])
            elif filter_ == 10 and (data['id'] == 2 or data['id'] == 3 or data['id'] == 4 or data['id'] == 5 or
                                    data['id'] == 6):
                return float(data['heating_rate'])
            elif filter_ == 11:
                return str(data['light_source'])
            elif filter_ == 12:
                return float(data['start_optical_power'])
            elif filter_ == 13 and data['id'] == 1:
                return str(data['time2'])
            elif filter_ == 14 and data['id'] == 0:
                return str(data['time2'])
            elif filter_ == 15 and data['id'] in (2, 3, 4, 5, 6):
                return str(data['time1'])
            elif filter_ == 16 and data['id'] == 8:
                return str(data['light_source'])
            elif filter_ == 17 and data['id'] == 8:
                return str(data['start_optical_power'])
            elif filter_ == 18 and data['id'] == 8:
                return str(data['final_temp'])
            elif filter_ == 19:
                return float(data['excV'])
            elif filter_ == 20:
                return float(data['excF'])
            else:
                return None
        except:
            return None

    def ungroup(self, process_to_ungroup):
        if not process_to_ungroup or process_to_ungroup is None:
            process_to_ungroup = self.tree_widget.selectedIndexes()

        self.runCommand('Ungroup', self, process_to_ungroup)
        self.document_changed.emit(self)

    @loadingCursor(empty=True)
    def ungroupAll(self):
        if self.process_data:
            self.runCommand('UngroupAll', self)
            self.document_changed.emit(self)

    def group(self, processes_to_group=None):
        try:
            if not processes_to_group or processes_to_group is None:
                processes_to_group = self.tree_widget.selectedIndexes()
            for index in processes_to_group:
                try:
                    temp = self.process_data[str(index.row()) + ',' + str(index.column())]
                except:
                    raise RuntimeError(
                        QtCore.QCoreApplication.translate(
                            'tree_widget_tab',
                            'Command {0} is empty'
                        ).format(str(index.column() - 1))
                    )
            self.runCommand('Group', self, processes_to_group)
            self.document_changed.emit(self)
        except Exception as err:
            self.show_error_message.emit(str(err))

    def clearGroupAssociation(self, group):
        for poss in self.in_group[group]:
            row = int(poss.split(',')[0])
            column = int(poss.split(',')[1])
            parent_item = self.tree_widget.topLevelItem(row)
            if row % 2 == 0:
                color = self.getConfiguration('tree_widget_item_background', 'COMMON')
            else:
                color = self.getConfiguration('tree_widget_item_alternate_background', 'COMMON')
            parent_item.setBackground(column, QtGui.QColor(color))

    def deleteInGroup(self, group_to_delete):
        for group in group_to_delete:
            try:
                del self.in_group[group]
            except:
                pass

    def getGroupColor(self, before, after):
        association_colors = [
            self.getConfiguration('association_color_1', 'GENREP'),
            self.getConfiguration('association_color_2', 'GENREP'),
            self.getConfiguration('association_color_3', 'GENREP')
        ]
        return list(set(association_colors) - {before, after})[0]

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
        tool_button_header.setToolTip(QtCore.QCoreApplication.translate('tree_widget_tab', 'Select Row'))
        self.tree_widget.setItemWidget(item, 0, tool_button_header)
        tool_button_header.clicked.connect(partial(self.selectRow, self.row_count))
        vs = self.tree_widget.verticalScrollBar()
        vs.setValue(vs.maximum())
        self.row_count += 1
        return self.row_count

    def addColumn(self):
        self.tree_widget.headerItem().setText(
            self.column_count,
            QtCore.QCoreApplication.translate('tree_widget_tab', "Command {0}").format(self.column_count - 1)
        )
        hs = self.tree_widget.horizontalScrollBar()
        hs.setValue(hs.maximum())
        self.column_count += 1
        return self.column_count

    def selectRow(self, index):
        if index is False and len(self.tree_widget.selectedIndexes()) > 0:
            index = self.tree_widget.selectedIndexes()[0].row()
        for i in self.tree_widget.selectedIndexes():
            item = self.tree_widget.topLevelItem(i.row())
            item.setSelected(False)
        item = self.tree_widget.topLevelItem(index)
        item.setSelected(True)
        self.selected_row = index

        parent_windows = self.parent().parent().parent().parent()
        parent_windows.findChild(QtWidgets.QSpinBox, "current_row").setValue(index + 1)
        self.clearColumnList()
        self.fillColumnsList()

        columns_list = parent_windows.findChild(QtWidgets.QTreeWidget, "columns_list")
        find = False
        for i in range(columns_list.topLevelItemCount()):
            item = columns_list.topLevelItem(i)
            if not item.isHidden():
                item.child(0).setSelected(True)
                find = True
                break
        if not find and columns_list.selectedItems():
            columns_list.selectedItems()[0].setSelected(False)

    def goNextRow(self):
        if self.process_data:
            if self.selected_row + 1 < self.tree_widget.topLevelItemCount():
                self.selectRow(self.selected_row + 1)
            else:
                self.show_info_message.emit(
                    QtCore.QCoreApplication.translate('main_window', 'Current selected row is the last one.')
                )

    def goPreviousRow(self):
        if self.process_data:
            if self.selected_row - 1 >= 0:
                self.selectRow(self.selected_row - 1)
            else:
                self.show_info_message.emit(
                    QtCore.QCoreApplication.translate('main_window', 'Current selected row is the first one.')
                )

    def goCustomRow(self):
        if self.process_data:
            parent_windows = self.parent().parent().parent().parent()
            row = parent_windows.findChild(QtWidgets.QSpinBox, "current_row").value() - 1
            if 0 <= row < self.tree_widget.topLevelItemCount():
                self.selectRow(row)
            else:
                self.show_info_message.emit(
                    QtCore.QCoreApplication.translate('main_window', 'Selected row is out of rang.')
                )
                parent_windows.findChild(QtWidgets.QSpinBox, "current_row").setValue(self.selected_row + 1)

    def clearColumnList(self):
        parent_windows = self.parent().parent().parent().parent()
        columns_list = parent_windows.findChild(QtWidgets.QTreeWidget, "columns_list")
        columns_list.clear()

    def fillColumnsList(self):
        parent_windows = self.parent().parent().parent().parent()
        item = self.tree_widget.topLevelItem(self.selected_row)
        for column in range(self.column_count)[2:]:
            data = item.text(column)
            if data:
                process_data = self.process_data[str(self.selected_row)+','+str(column)]
                header = self.tree_widget.header().model().headerData(column, QtCore.Qt.Horizontal)
                columns_list = parent_windows.findChild(QtWidgets.QTreeWidget, "columns_list")

                new_column = QtWidgets.QTreeWidgetItem(columns_list)
                new_column.setFlags(QtCore.Qt.ItemIsEnabled)
                new_column.setText(0, header)
                for curve in self.getConfiguration('curve_to_show', 'GENREP'):
                    if process_data['curve' + str(curve)] != '':
                        new_column.addChild(QtWidgets.QTreeWidgetItem([str(curve)]))
                new_column.setExpanded(True)
                if not new_column.childCount() > 0:
                    new_column.setHidden(True)

    def valuesOf(self, row, column, curve):
        data = self.process_data[str(row)+','+str(column)]
        sum_ = 0
        if 'datapoints1' in data.keys():
            sum_ += data['datapoints1']
        if 'datapoints2' in data.keys():
            sum_ += data['datapoints2']
        if 'datapoints3' in data.keys():
            sum_ += data['datapoints3']
        y_values = [float(i) for i in data['curve' + curve].split(';')[:sum_]]

        if data['id'] == 2 and self.getConfiguration('show_tl', 'GENREP'):
            x_values = [float("{0:.4f}".format(i)) for i in data['curve3'].split(';')[:sum_]]
        else:
            x_values = range(1, sum_ + 1)
        if self.getConfiguration('unit', 'GENREP'):
            x_values = [(i * data['timePerChannel']) for i in x_values]
        if len(x_values) > 0 and x_values[0] == 0 and \
                (self.getConfiguration('horizontal_scale', 'GENREP') == 'log' or
                 self.getConfiguration('horizontal_scale', 'GENREP') == 'ln'):
            del x_values[0]
            new = x_values[-1] + 1
            x_values.append(new)
        x_values = [float('%.4f' % i) for i in x_values]

        return x_values, y_values

    def getLowHigh(self):
        if (self.ploting_pos is None) or (self.ploting_pos not in self.signal_values.keys()):
            low_signal = self.getConfiguration('low_signal', 'GENREP') - 1
            high_signal = self.getConfiguration('high_signal', 'GENREP')
            low_background = self.getConfiguration('low_background', 'GENREP')
            high_background = self.getConfiguration('high_background', 'GENREP')
            default = True
        else:
            low_signal = self.signal_values[self.ploting_pos][0]
            high_signal = self.signal_values[self.ploting_pos][1]
            low_background = self.background_values[self.ploting_pos][0]
            high_background = self.background_values[self.ploting_pos][1]
            default = False
        return low_signal, high_signal, low_background, high_background, default

    def popup(self, pos):
        x = pos.x() + 3
        y = pos.y()
        pos = QtCore.QPoint(x, y)
        menu = QtWidgets.QMenu()

        is_valid = len(self.tree_widget.selectedIndexes()) == 1 or self.areConsecutive()
        is_editable = True
        if is_valid:
            for index in self.tree_widget.selectedIndexes():
                if index.column() < 2:
                    is_editable = False
                    if index.column() < 1:
                        is_valid = False
                    break
        if is_valid:
            menu.addAction(self.action_select_row)
            menu.addSeparator()
        if is_editable:
            parent_windows = self.parent().parent().parent().parent()
            if parent_windows.findChild(QtWidgets.QAction, "action_group").isEnabled():
                menu.addAction(self.action_group)
            if parent_windows.findChild(QtWidgets.QAction, "action_ungroup").isEnabled():
                menu.addAction(self.action_ungroup)
        if is_valid:
            menu.exec_(self.tree_widget.mapToGlobal(pos))

    def runCommand(self, command, *args):
        commands = {
            'SetValue': SetValue,
            'SetData': SetData,
            'Group': Group,
            'Ungroup': Ungroup,
            'UngroupAll': UngroupAll,
            'Save': Save,
        }
        self.undo_stack.beginMacro(str(self.undo_stack_macro))
        self.undo_stack.push(commands[command](*args))
        self.undo_stack.endMacro()
        self.undo_stack_macro += 1
