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
        self.sample_id = self.xml.createElement("Sample_ID")
        self.sample_id.setAttribute("sample", str(id_))


class ProcessOrder(TagBase):
    def __init__(self, id_, type_, status, processes):
        self.xml = Document()
        self.process_order = self.xml.createElement("Process_order")
        self.process_order.setAttribute("number", str(id_))

        self.status = self.xml.createElement("Status")
        self.type_ = self.xml.createElement("Type")

        self.setTextNode(self.status, status)
        self.setTextNode(self.type_, type_)

        self.process_order.appendChild(self.status)
        self.process_order.appendChild(self.type_)

        for process in processes:
            self.process_order.appendChild(process)


class Process(TagBase):
    def __init__(self, id_, parameters, data):
        self.parameters = parameters

        self.xml = Document()
        self.process = self.xml.createElement("Process_ID")
        self.process.setAttribute("id", str(id_))

        if self.parameters is not None:
            self.param = self.xml.createElement("Param")
            self.info = self.xml.createElement("info")
            self.data = self.xml.createElement("data")

            self.process.appendChild(self.param)
            self.process.appendChild(self.info)
            self.process.appendChild(self.data)

            if id_ in [3, 4, 5, 6, 8]:
                self.light_source = self.xml.createElement("light_source")
                self.setTextNode(self.light_source, 'light_source')

                self.start_optical_power = self.xml.createElement("start_optical_power")
                self.setTextNode(self.start_optical_power, 'start_optical_power')
            if id_ == 5:
                self.end_optical_power = self.xml.createElement("end_optical_power")
                self.setTextNode(self.end_optical_power, 'end_optical_power')
            if id_ in [0, 1, 3, 4, 5, 6, 8, 9]:
                self.time = self.xml.createElement("time")
                self.setTextNode(self.time, 'time')
            if id_ in [3, 4]:
                self.datapoints1 = self.xml.createElement("datapoints1")
                self.setTextNode(self.datapoints1, 'datapoints1')
            if id_ in [2, 3, 4, 5, 6]:
                self.datapoints2 = self.xml.createElement("datapoints2")
                self.setTextNode(self.datapoints2, 'datapoints2')
            if id_ in [3, 4]:
                self.datapoints3 = self.xml.createElement("datapoints3")
                self.setTextNode(self.datapoints3, 'datapoints3')
            if id_ == 4:
                self.number_of_scans = self.xml.createElement("number_of_scans")
                self.setTextNode(self.number_of_scans, 'number_scan')
            if id_ == 2:
                self.save_temp = self.xml.createElement("save_temp")
                self.setTextNode(self.save_temp, 'save_temp')
            if id_ in [1, 2, 3, 4, 5, 6, 7, 8]:
                self.heating_rate = self.xml.createElement("heating_rate")
                self.setTextNode(self.heating_rate, 'heating_rate')

                self.final_temp = self.xml.createElement("T1")
                self.setTextNode(self.final_temp, 'final_temp')
            if id_ in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
                self.time_final_temp = self.xml.createElement("tT1")
                self.setTextNode(self.time_final_temp, 'time_final_temp')
            if id_ in [1, 3, 4, 5, 6, 8]:
                self.stabilization = self.xml.createElement("dT1")
                self.setTextNode(self.stabilization, 'stabilization')
            if id_ == 6:
                self.exc_v = self.xml.createElement("ExcV")
                self.setTextNode(self.exc_v, 'excV')

                self.exc_f = self.xml.createElement("ExcF")
                self.setTextNode(self.exc_f, 'excF')

            self.data_type = self.xml.createElement("Datatype")
            super(Process, self).setTextNode(self.data_type, self.parameters['date_type'])
            self.info.appendChild(self.data_type)

            self.comment = self.xml.createElement("comment")
            super(Process, self).setTextNode(self.comment, self.parameters['comments'])
            self.info.appendChild(self.comment)

            self.curve_1 = self.xml.createElement("Curva1")
            self.data.appendChild(self.curve_1)

            self.curve_2 = self.xml.createElement("Curva2")
            self.data.appendChild(self.curve_2)

            self.curve_3 = self.xml.createElement("Curva3")
            self.data.appendChild(self.curve_3)

            self.time_1 = self.xml.createElement("Tiempo1")
            self.data.appendChild(self.time_1)

            self.time_2 = self.xml.createElement("Tiempo2")
            self.data.appendChild(self.time_2)

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


class CreateSLF(TagBase):
    def __init__(self, samples_amount, name, owner, nitrogen_use, dose_rate,
                 external_dose_rate, protocol, reader_id, datecrea):
        self.xml = Document()
        self.slf = self.xml.createElement("SEQ")
        self.xml.appendChild(self.slf)

        self.name = self.xml.createElement("Name")
        self.status = self.xml.createElement("STATUS")
        self.datecrea = self.xml.createElement("Datecrea")
        self.datemod = self.xml.createElement("Datemod")
        self.owner = self.xml.createElement("Owner")
        self.samples_amount = self.xml.createElement("NMuestras")
        self.reader_id = self.xml.createElement("Reader_ID")
        self.nitrogen_use = self.xml.createElement("N2Flow")
        self.dose_rate = self.xml.createElement("Doserate")
        self.external_dose_rate = self.xml.createElement("ExtDoserate")
        self.protocol = self.xml.createElement("Protocol")
        self.seq = self.xml.createElement("seq")

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
        self.setTextNode(self.status, 'pend')
        self.setTextNode(self.datemod, datemod)

        self.slf.appendChild(self.name)
        self.slf.appendChild(self.status)
        self.slf.appendChild(self.datecrea)
        self.slf.appendChild(self.datemod)
        self.slf.appendChild(self.owner)
        self.slf.appendChild(self.samples_amount)
        self.slf.appendChild(self.reader_id)
        self.slf.appendChild(self.nitrogen_use)
        self.slf.appendChild(self.dose_rate)
        self.slf.appendChild(self.external_dose_rate)
        self.slf.appendChild(self.protocol)
        self.slf.appendChild(self.seq)

    def refreshDateMod(self):
        self.datemod.firstChild.data = str(datetime.now())

    def createSample(self, id_):
        self.refreshDateMod()
        samples_ids = self.xml.getElementsByTagName("seq")[0].getElementsByTagName('Sample_ID')
        new_sample = Sample(id_).sample_id
        if len(samples_ids) > 0:
            for sample_id in samples_ids:
                value = sample_id.attributes['sample'].value
                if int(value) == int(id_):
                    return sample_id
                if int(value) > int(id_):
                    self.seq.insertBefore(new_sample, sample_id)
                    return new_sample
        self.seq.appendChild(new_sample)
        return new_sample

    def createProcess(self, id_, parameters, data):
        self.refreshDateMod()
        process = Process(id_, parameters, data).process
        return process

    def createProcessOrder(self, sample_id, id_, type_, status, processes):
        self.refreshDateMod()
        process_order = ProcessOrder(id_, type_, status, processes).process_order
        sample_id.appendChild(process_order)
        return process_order

    def preview(self):
        return self.xml.toprettyxml(indent="    ")

    def save(self, path, rewrite=False):
        if os.path.exists(path):
            if os.path.isfile(path):
                ext = os.path.splitext(path)[-1]
                if ext not in ('.xml', '.slf',):
                    raise ValueError('Incorrect format, must be a slf or xml file.')
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
                if ext not in ('.xml', '.slf',):
                    path += '.slf'
                document = open(path, 'w')
                self.xml.writexml(document, addindent='    ', newl='\n', encoding='iso-8859-1')
                return True
            else:
                raise ValueError('Directory "{0}" does not exist.'.format(dirname))


class LoadSLF:
    def __init__(self, path):
        if os.path.exists(path):
            if os.path.isfile(path):
                ext = os.path.splitext(path)[-1]
                if ext != '.slf':
                    raise ValueError('Incorrect format, must be a slf file')
            else:
                raise ValueError('The path is not valid, must be a slf file')
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
            raise RuntimeError("General data of the sequence can't be read.")

        table = []
        for seq in tree[1][11:]:
            for sample in seq[1]:
                tuple_ = ['', []]
                process_order_id = 1
                for process_order in sample[1]:
                    status = self.getCleanData(process_order[1][0][1])
                    type_ = self.getCleanData(process_order[1][1][1])
                    # process_order_id = int(process_order[2]['number'])

                    merge = []
                    for process_id in process_order[1][2:]:
                        command = {'status': status}
                        command['id'] = int(process_id[2]['id'])
                        if command['id'] != -1:
                            for param in process_id[1][0][1]:
                                parameter_key = str(param[0]).split('\'')[1]
                                parameter_value = param[1]
                                if parameter_value is not None:
                                    if parameter_key == 'T1':
                                        parameter_key = 'final_temp'
                                    elif parameter_key == 'dT1':
                                        parameter_key = 'stabilization'
                                    elif parameter_key == 'tT1':
                                        parameter_key = 'time_final_temp'
                                    elif parameter_key == 'ExcV':
                                        parameter_key = 'excV'
                                    elif parameter_key == 'ExcF':
                                        parameter_key = 'excF'

                                    if parameter_key == 'stabilization' or \
                                                        parameter_key == 'excV' or \
                                                        parameter_key == 'excF' or \
                                                        parameter_key == 'final_temp' or \
                                                        parameter_key == 'time_final_temp' or \
                                                        parameter_key == 'heating_rate' or \
                                                        parameter_key == 'time':
                                        parameter_value = float(parameter_value)
                                    elif parameter_key == 'datapoints1' or \
                                                            parameter_key == 'datapoints2' or \
                                                            parameter_key == 'datapoints3' or \
                                                            parameter_key == 'start_optical_power' or \
                                                            parameter_key == 'end_optical_power' or \
                                                            parameter_key == 'number_of_scans' or \
                                                            parameter_key == 'save_temp':
                                        parameter_value = int(parameter_value)

                                    command[parameter_key] = parameter_value
                                    command['time_unit'] = 's'

                            command['date_type'] = self.getCleanData(process_id[1][1][1][0][1])
                            command['comments'] = self.getCleanData(process_id[1][1][1][1][1])

                            command['curve1'] = self.getCleanData(process_id[1][2][1][0][1])
                            command['curve2'] = self.getCleanData(process_id[1][2][1][1][1])
                            command['curve3'] = self.getCleanData(process_id[1][2][1][2][1])
                            command['time1'] = self.getCleanData(process_id[1][2][1][3][1])
                            command['time2'] = self.getCleanData(process_id[1][2][1][4][1])

                            command['process_order_id'] = process_order_id

                            if command['id'] == 1:
                                command['source'] = 'Beta'
                            if command['id'] == 0:
                                command['source'] = 'External'
                            if command['id'] == 3 or command['id'] == 4:
                                command['channels'] = command['datapoints1'] + \
                                                      command['datapoints2'] + \
                                                      command['datapoints3']
                                try:
                                    command['timePerChannel'] = float(command['time']) / float(command['channels'])
                                except:
                                    command['timePerChannel'] = 0
                            if command['id'] == 4:
                                try:
                                    command['number_scan'] = command['number_of_scans']
                                except:
                                    command['number_scan'] = 0
                            if command['id'] == 5:
                                try:
                                    command['timePerChannel'] = float(command['time']) / float(command['datapoints2'])
                                except:
                                    command['timePerChannel'] = 0
                            if command['id'] == 6:
                                command['record_during'] = 0
                                command['light_co_stimulation'] = 0
                                if 'datapoints2' in command:
                                    command['record_during'] = 1
                                if 'light_source' in command:
                                    command['light_co_stimulation'] = 1
                                try:
                                    command['timePerChannel'] = float(command['time']) / float(command['datapoints2'])
                                except:
                                    command['timePerChannel'] = 0
                            if command['id'] == 2:
                                try:
                                    command['timePerChannel'] = float(command['final_temp']) / float(command['heating_rate']) + float(command['time_final_temp'])
                                except:
                                    command['timePerChannel'] = 0
                        process_order_id += 1
                        merge.append(command)
                    tuple_[1].append(merge)
                # sample
                sample_id = sample[2]['sample']

                tuple_[0] = sample_id
                table.append(tuple_)
        return general, table
