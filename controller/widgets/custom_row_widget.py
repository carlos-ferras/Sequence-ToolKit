#!/usr/bin/python3
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from PyQt5 import QtWidgets, QtCore

from view.widgets.ui_custom_row_widget import Ui_custom_row_widget
from controller.widgets.custom_row_widget_item import CustomRowWidgetItem


class CustomRowWidget(QtWidgets.QWidget, Ui_custom_row_widget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent.main_window)
        self.setupUi(self)

        self.parent_windows = parent
        self.items = []
        self.visit_item_pos = None

    def count(self):
        return len(self.items)

    def addWidget(self, date_path):
        item = CustomRowWidgetItem(date_path, self.parent_windows, self)
        self.items.append(item)
        self.gridLayout.addWidget(item, 0, self.count(), 1, 1, QtCore.Qt.AlignLeft)

    def addSpacer(self):
        horizontal_spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(horizontal_spacer, 0, self.count(), 1, 1, QtCore.Qt.AlignLeft)

    def mouseMoveEvent(self, event):
        found = False
        for i in range(len(self.items)):
            if event.pos().y() in range(self.items[i].pos().y(), self.items[i].height() + self.items[i].pos().y()):
                if event.pos().x() in range(self.items[i].pos().x(), self.items[i].width() + self.items[i].pos().x()):
                    found = True
                    if i != self.visit_item_pos:
                        if self.visit_item_pos is not None:
                            self.items[self.visit_item_pos].mouseLeave()
                        self.visit_item_pos = i
                        self.items[self.visit_item_pos].mouseEnter()
                    break
        if not found:
            if self.visit_item_pos is not None:
                self.items[self.visit_item_pos].mouseLeave()
                self.visit_item_pos = None

        for widget in self.parent_windows.row_widgets:
            if widget != self:
                if widget.visit_item_pos is not None:
                    widget.items[widget.visit_item_pos].mouseLeave()
                    widget.visit_item_pos = None



