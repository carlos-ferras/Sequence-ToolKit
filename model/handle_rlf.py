#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import os
from datetime import datetime
from xml.dom.minidom import Document
from xml.etree import cElementTree as cET


class TagBase:
    def __init__(self):
        pass

    def setTextNode(self, tag, data):
        if data != '' and data is not None:
            if data is False or data == 'False':
                data = 0
            if data is True or data == 'True':
                data = 1
            tag.appendChild(self.xml.createTextNode(str(data)))


class Sample(TagBase):
    def __init__(self, id_):
        self.xml = Document()
        self.sample_id = self.xml.createElement("sample_id")
        self.sample_id.setAttribute("sample", str(id_))


class ProcessOrder(TagBase):
    def __init__(self, id_, ptype_, dtype_, curves, parameters):
        self.parameters = parameters
        self.xml = Document()
        self.process_order = self.xml.createElement("process_order")
        self.process_order.setAttribute("number", str(id_))

        self.process = self.xml.createElement("process")
        self.data_type = self.xml.createElement("data_type")
        self.curves = self.xml.createElement("curves")
        self.param = self.xml.createElement("param")

        super(ProcessOrder, self).setTextNode(self.process, ptype_)
        super(ProcessOrder, self).setTextNode(self.data_type, dtype_)

        self.process_order.appendChild(self.process)
        self.process_order.appendChild(self.data_type)
        self.process_order.appendChild(self.curves)
        self.process_order.appendChild(self.param)

        for curve in curves:
            self.curves.appendChild(curve)

        self.time_per_channel = self.xml.createElement("time_per_channel")
        self.beta_irradiation_time = self.xml.createElement("beta_irradiation_time")
        self.beta_dose = self.xml.createElement("beta_dose")
        self.external_irradiation = self.xml.createElement("external_irradiation")
        self.external_dose = self.xml.createElement("external_dose")
        self.preheating_temperature = self.xml.createElement("preheating_temperature")
        self.measuring_temperature = self.xml.createElement("measuring_temperature")
        self.preheating_rate = self.xml.createElement("preheating_rate")
        self.heating_rate = self.xml.createElement("heating_rate")
        self.light_source = self.xml.createElement("light_source")
        self.optical_power = self.xml.createElement("optical_power")
        self.electric_stimulation = self.xml.createElement("electric_stimulation")
        self.electric_frequency = self.xml.createElement("electric_frequency")
        self.time_beta_irradiation = self.xml.createElement("time_beta_irradiation")
        self.time_external_irradiation = self.xml.createElement("time_external_irradiation")
        self.time_measurement = self.xml.createElement("time_measurement")
        self.illumination_source = self.xml.createElement("illumination_source")
        self.illumination_power = self.xml.createElement("illumination_power")
        self.illumination_temperature = self.xml.createElement("illumination_temperature")

        self.setTextNode(self.time_per_channel, 'Time_per_channel')
        self.setTextNode(self.beta_irradiation_time, 'Beta_irradiation_time')
        self.setTextNode(self.beta_dose, 'Beta_dose')
        self.setTextNode(self.external_irradiation, 'External_irradiation')
        self.setTextNode(self.external_dose, 'External_dose')
        self.setTextNode(self.preheating_temperature, 'Preheating_temperature')
        self.setTextNode(self.measuring_temperature, 'Measuring_temperature')
        self.setTextNode(self.preheating_rate, 'Preheating_rate')
        self.setTextNode(self.heating_rate, 'Heating_rate')
        self.setTextNode(self.light_source, 'Light_source')
        self.setTextNode(self.optical_power, 'Optical_power')
        self.setTextNode(self.electric_stimulation, 'Electric_stimulation')
        self.setTextNode(self.electric_frequency, 'Electric_frequency')
        self.setTextNode(self.time_beta_irradiation, 'Time_beta_irradiation')
        self.setTextNode(self.time_external_irradiation, 'Time_external_irradiation')
        self.setTextNode(self.time_measurement, 'Time_measurement')
        self.setTextNode(self.illumination_source, 'Illumination_source')
        self.setTextNode(self.illumination_power, 'Illumination_power')
        self.setTextNode(self.illumination_temperature, 'Illumination_temperature')

    def setTextNode(self, tag, key):
        if key in self.parameters:
            data = self.parameters[key]
            if data is False or data == 'False':
                data = 0
            if data is True or data == 'True':
                data = 1
            if data != '' and data is not None:
                tag.appendChild(self.xml.createTextNode(str(data)))
                self.param.appendChild(tag)


class Curve(TagBase):
    def __init__(self, number, signal_active, background_active, count_signal, low_signal,
                 high_signal, count_background, low_background, high_background):
        self.xml = Document()
        self.curve = self.xml.createElement("curve_" + str(number))

        if signal_active:
            self.count_signal = self.xml.createElement("count_signal")
            self.low_signal = self.xml.createElement("low_signal")
            self.high_signal = self.xml.createElement("high_signal")

            self.setTextNode(self.count_signal, count_signal)
            self.setTextNode(self.low_signal, low_signal)
            self.setTextNode(self.high_signal, high_signal)

            self.curve.appendChild(self.count_signal)
            self.curve.appendChild(self.low_signal)
            self.curve.appendChild(self.high_signal)
        if background_active:
            self.count_background = self.xml.createElement("count_background")
            self.low_background = self.xml.createElement("low_background")
            self.high_background = self.xml.createElement("high_background")

            self.setTextNode(self.count_background, count_background)
            self.setTextNode(self.low_background, low_background)
            self.setTextNode(self.high_background, high_background)

            self.curve.appendChild(self.count_background)
            self.curve.appendChild(self.low_background)
            self.curve.appendChild(self.high_background)


class CreateRLF(TagBase):
    def __init__(self, samples_amount, name, owner, nitrogen_use, dose_rate,
                 external_dose_rate, protocol, status, reader_id, datecrea):
        self.xml = Document()
        self.rlf = self.xml.createElement("rlf")
        self.xml.appendChild(self.rlf)

        self.name = self.xml.createElement("name")
        self.status = self.xml.createElement("status")
        self.datecrea = self.xml.createElement("date_crea")
        self.datemod = self.xml.createElement("date_mod")
        self.owner = self.xml.createElement("owner")
        self.samples_amount = self.xml.createElement("samples_amount")
        self.reader_id = self.xml.createElement("reader_id")
        self.nitrogen_use = self.xml.createElement("N2_flow")
        self.dose_rate = self.xml.createElement("dose_rate")
        self.external_dose_rate = self.xml.createElement("external_dose_rate")
        self.protocol = self.xml.createElement("protocol")
        self.rep = self.xml.createElement("rep")

        datemod = datetime.now()
        if (not datecrea) or datecrea is None:
            datecrea = datemod

        self.setTextNode(self.samples_amount, samples_amount)
        self.setTextNode(self.name, name)
        self.setTextNode(self.owner, owner)
        self.setTextNode(self.nitrogen_use, nitrogen_use)
        self.setTextNode(self.dose_rate, dose_rate)
        self.setTextNode(self.external_dose_rate, external_dose_rate)
        self.setTextNode(self.protocol, protocol)
        self.setTextNode(self.reader_id, reader_id)
        self.setTextNode(self.datecrea, datecrea)
        self.setTextNode(self.status, status)
        self.setTextNode(self.datemod, datemod)

        self.rlf.appendChild(self.name)
        self.rlf.appendChild(self.status)
        self.rlf.appendChild(self.datecrea)
        self.rlf.appendChild(self.datemod)
        self.rlf.appendChild(self.owner)
        self.rlf.appendChild(self.samples_amount)
        self.rlf.appendChild(self.reader_id)
        self.rlf.appendChild(self.nitrogen_use)
        self.rlf.appendChild(self.dose_rate)
        self.rlf.appendChild(self.external_dose_rate)
        self.rlf.appendChild(self.protocol)
        self.rlf.appendChild(self.rep)

    def refreshDateMod(self):
        self.datemod.firstChild.data = str(datetime.now())

    def createSample(self, id_):
        self.refreshDateMod()
        samples_ids = self.xml.getElementsByTagName("rep")[0].getElementsByTagName('sample_id')
        new_sample = Sample(id_).sample_id
        if len(samples_ids) > 0:
            for sample_id in samples_ids:
                value = sample_id.attributes['sample'].value
                if int(value) == int(id_):
                    return sample_id
                if int(value) > int(id_):
                    self.seq.insertBefore(new_sample, sample_id)
                    return new_sample
        self.rep.appendChild(new_sample)
        return new_sample

    def createProcessOrder(self, sample_id, id_, ptype_, dtype_, curves, parameters):
        self.refreshDateMod()
        process_order = ProcessOrder(id_, ptype_, dtype_, curves, parameters).process_order
        sample_id.appendChild(process_order)
        return process_order

    def createCurve(self, number, signal_active, background_active, count_signal, low_signal,
                    high_signal, count_background, low_background, high_background):
        self.refreshDateMod()
        curve = Curve(number, signal_active, background_active, count_signal, low_signal,
                      high_signal, count_background, low_background, high_background).curve
        return curve

    def preview(self):
        return self.xml.toprettyxml(indent="    ")

    def save(self, path, rewrite=False):
        if os.path.exists(path):
            if os.path.isfile(path):
                ext = os.path.splitext(path)[-1]
                if ext not in ('.xml', '.rlf',):
                    raise ValueError('Incorrect format, must be a rlf or xml file.')
                else:
                    if rewrite:
                        try:
                            document = open(path, 'w')
                            self.xml.writexml(document, addindent='    ', newl='\n', encoding='iso-8859-1')
                            return True
                        except:
                            raise ValueError('Error while writing.')
                    return False
            else:
                raise ValueError('Invalid file path.')
        else:
            dirname = os.path.dirname(path)
            if os.path.exists(dirname) or dirname == '':
                ext = os.path.splitext(path)[-1]
                if ext not in ('.xml', '.rlf',):
                    path += '.rlf'
                document = open(path, 'w')
                self.xml.writexml(document, addindent='    ', newl='\n', encoding='iso-8859-1')
                return True
            else:
                raise ValueError('Directory "{0}" does not exist.'.format(dirname))


class LoadRLF:
    def __init__(self, path):
        if os.path.exists(path):
            if os.path.isfile(path):
                ext = os.path.splitext(path)[-1]
                if ext != '.rlf':
                    raise ValueError('Incorrect format, must be a rlf file')
            else:
                raise ValueError('The path is not valid, must be a rlf file')
        else:
            raise ValueError('Directory "{0}" does not exist.'.format(path))
        try:
            self.path = path
            self.tree = cET.parse(path)
            self.root = self.tree.getroot()
        except:
            raise ValueError('Error while reading')

    def build(self, root):
        childs = root.getchildren()
        keys = root.keys()
        data = {}
        for key in keys:
            data[key] = root.get(key)
        tree = [root, childs, data]
        if len(childs) == 0:
            tree[1] = root.text
        else:
            for i in range(len(tree[1])):
                child = self.build(tree[1][i])
                tree[1][i] = child
        return tree

    def getCleanData(self, data):
        if data == 'None' or data is None:
            return ''
        return str(data)

    def open(self):
        general = {}
        try:
            tree = self.build(self.root)
            general['name'] = self.getCleanData(tree[1][0][1])
            general['status'] = self.getCleanData(tree[1][1][1])
            general['creation_date'] = self.getCleanData(tree[1][2][1])
            general['modification_date'] = self.getCleanData(tree[1][3][1])
            general['owner'] = self.getCleanData(tree[1][4][1])
            general['samples_amount'] = self.getCleanData(tree[1][5][1])
            general['reader_id'] = self.getCleanData(tree[1][6][1])
            general['nitrogen_use'] = int(tree[1][7][1])
            general['dose_rate'] = float(tree[1][8][1])
            general['external_dose_rate'] = float(tree[1][9][1])
            general['protocol'] = self.getCleanData(tree[1][10][1])
        except:
            raise RuntimeError("General data of the report can't be read.")

        table = []
        for rep in tree[1][11:]:
            for sample in rep[1]:
                tuple_ = ['', []]
                for process_order in sample[1]:
                    command = {
                        'process_name': self.getCleanData(process_order[1][0][1]),
                        'data_type': self.getCleanData(process_order[1][1][1]),
                        'process_order_id': int(process_order[2]['number'])
                    }

                    curves = {}
                    for curve in process_order[1][2][1]:
                        curve_num = str(curve[0]).split('\'')[1].split('_')[1]
                        curve_data = {}
                        for data in curve[1]:
                            data_key = str(data[0]).split('\'')[1]
                            curve_data[data_key] = data[1]
                        curves[curve_num] = curve_data

                    parameters = {}
                    for param in process_order[1][3][1]:
                        parameter_key = str(param[0]).split('\'')[1]
                        parameter_value = param[1]
                        parameters[parameter_key] = parameter_value

                    command['curves'] = curves
                    command['parameters'] = parameters
                    tuple_[1].append(command)

                sample_id = sample[2]['sample']
                tuple_[0] = sample_id
                table.append(tuple_)
        return general, table
