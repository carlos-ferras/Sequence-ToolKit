#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import os
from PyQt5 import QtGui

import img_rc
from view.dialogs.base_dialog import BaseDialog
from view.stk.dialogs.ui_properties import Ui_properties
from xml.etree import cElementTree as cET


class Properties(BaseDialog, Ui_properties):
    def __init__(self, date_path, parent=None):
        BaseDialog.__init__(self, parent)
        self.setupUi(self)

        self.push_button_close.clicked.connect(self.close)

        file_type = date_path[1].split('.')[-1]
        icon = QtGui.QPixmap(":/resources/img/file_type/" + file_type + ".svg")
        self.file_icon.setPixmap(icon)

        self.file_name.setText(os.path.basename(date_path[1]))
        self.location.setText(date_path[1])
        self.accessed.setText(date_path[0])

        size = self.humanReadableSize(os.stat(date_path[1]).st_size)
        self.file_size.setText(size)

        self.loadSequenceData(date_path[1])

    def humanReadableSize(self, size):
        sufixes = {1024: ["KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]}
        mult = 1024.0
        for sufx in sufixes[mult]:
            size /= mult
            if size < mult:
                return "{0:.5f} {1}".format(size, sufx)

    def loadSequenceData(self, path):
        tree = cET.parse(path)
        root = tree.getroot()

        try:
            tree = self.build(root)
            self.name.setText(self.getCleanData(tree[1][0][1]))
            self.status.setText(self.getCleanData(tree[1][1][1]))
            self.creaton_date.setText(self.getCleanData(tree[1][2][1]))
            self.last_modification.setText(self.getCleanData(tree[1][3][1]))
            self.owner.setText(self.getCleanData(tree[1][4][1]))
            self.amount.setText(self.getCleanData(tree[1][5][1]))
            self.reader_id.setText(self.getCleanData(tree[1][6][1]))
            self.nitrogen_use.setText(tree[1][7][1])
            self.dose_rate.setText(tree[1][8][1])
            self.external_dose_rate.setText(tree[1][9][1])
            self.protocol.setText(self.getCleanData(tree[1][10][1]))
        except:
            raise RuntimeError('General data of the sequence can be read.')

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
            return '-'
        return str(data)
