#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals


class CustomIndex:
    def __init__(self, row, column):
        self._row = row
        self._column = column

    def row(self):
        return self._row

    def column(self):
        return self._column


class CustomData:
    def __init__(self, position, text, process_data):
        self.position = position
        self.text = text
        self.process_data = process_data


class CustomDataSet:
    def __init__(self):
        self.custom_data_set = []

    def setData(self, row, column, text, process_data, append_to_last=False):
        position = CustomIndex(row, column)
        custom_data = CustomData(position, text, process_data)

        if append_to_last:
            self.custom_data_set[-1].append(custom_data)
        else:
            self.custom_data_set.append([custom_data])

    def __str__(self):
        line = ''
        for group in self.custom_data_set:
            for mime in group:
                line += '; ' + mime.text
        return line[2:]

