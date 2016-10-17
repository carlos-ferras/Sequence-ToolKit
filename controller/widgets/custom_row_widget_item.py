#!/usr/bin/python3
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import os
from functools import partial
from PyQt5 import QtWidgets, QtGui, QtCore

from view.widgets.ui_custom_row_widget_item import Ui_custom_row_widget_item
from controller.stk.dialogs.properties import Properties


class CustomRowWidgetItem(QtWidgets.QWidget, Ui_custom_row_widget_item):
    def __init__(self, date_path, parent_windows, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.parent_windows = parent_windows
        self.date_path = date_path
        self.buttons = []

        text = os.path.basename(date_path[1])
        if len(text) > 18:
            text = '...' + text[-15:]
        self.file_type = date_path[1].split('.')[-1]

        icon = QtGui.QPixmap(":/resources/img/file_type/" + self.file_type + ".svg")
        self.file_icon.setPixmap(icon)

        self.action_properties.triggered.connect(self.properties)
        self.customContextMenuRequested.connect(self.popup)

        self.path.setText(text)
        self.initButtons()

    def initButtons(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(
            ":/resources/img/icons/open.svg"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off
        )

        if self.file_type == 'rlf':
            open_with_genvis = QtWidgets.QPushButton('GenVis')
            open_with_genvis.setIcon(icon)
            open_with_genvis.setGeometry(0, 0, 0, 0)
            open_with_genvis.setParent(self.parent())
            open_with_genvis.clicked.connect(partial(self.parent_windows.openWithGenVis, self.date_path[1]))

            self.buttons.append(open_with_genvis)

        elif self.file_type == 'slf':
            open_with_gensec = QtWidgets.QPushButton('GenSec')
            open_with_gensec.setIcon(icon)
            open_with_gensec.setGeometry(0, 0, 0, 0)
            open_with_gensec.setParent(self.parent())
            open_with_gensec.clicked.connect(partial(self.parent_windows.openWithGenSec, self.date_path[1]))

            open_with_genrep = QtWidgets.QPushButton('GenRep')
            open_with_genrep.setIcon(icon)
            open_with_genrep.setGeometry(0, 0, 0, 0)
            open_with_genrep.setParent(self.parent())
            open_with_genrep.clicked.connect(partial(self.parent_windows.openWithGenRep, self.date_path[1]))

            self.buttons.append(open_with_genrep)
            self.buttons.append(open_with_gensec)

    def showButton(self, index):
        animator = QtCore.QPropertyAnimation(self.buttons[index], b'geometry', self.buttons[index])
        animator.setCurrentTime(-80)
        animator.setDuration(100)
        animator.setStartValue(
            QtCore.QRectF(self.pos().x() + 25, (self.pos().y() + 170) - ((index + 1) * 39), 0, 32.0)
        )
        animator.setEndValue(
            QtCore.QRectF(self.pos().x() + 25, (self.pos().y() + 170) - ((index + 1) * 39), 120.0, 32.0)
        )
        animator.start()

    def hideButton(self, button):
        animator = QtCore.QPropertyAnimation(button, b'geometry', button)
        animator.setDuration(100)
        animator.setStartValue(button.geometry())
        animator.setEndValue(QtCore.QRectF(button.pos().x(), button.pos().y(), 0, 32.0))
        animator.start()

    def mouseEnter(self):
        for i in range(len(self.buttons)):
            self.showButton(i)

        self.parent_windows.statusbar.showMessage(
            self.date_path[1] +
            '  [ ' +
            QtCore.QCoreApplication.translate(
                'custom_row_widget_item',
                'Accessed: {0}').format(self.date_path[0]) +
            ' ]'
        )

    def mouseLeave(self):
        try:
            for button in self.buttons:
                self.hideButton(button)
        except:
            pass

        self.parent_windows.statusbar.clearMessage()

    def properties(self):
        dialog = Properties(self.date_path, self)
        self.mouseLeave()
        dialog.exec_()

    def popup(self, pos):
        x = pos.x()
        y = pos.y()
        pos = QtCore.QPoint(x, y)

        menu = QtWidgets.QMenu()
        menu.addAction(self.action_properties)
        menu.exec_(self.mapToGlobal(pos))