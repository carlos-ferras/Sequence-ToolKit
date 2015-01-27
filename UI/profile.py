#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#~ Copyright (C) 2014 Carlos Manuel Ferras Hernandez <c4rlos.ferra5@gmail.com>
#~ This file is part of Sequence-ToolKit.

#~ Sequence-ToolKit is free software: you can redistribute it and/or modify
#~ it under the terms of the GNU General Public License as published by
#~ the Free Software Foundation, either version 3 of the License, or
#~ (at your option) any later version.

#~ Sequence-ToolKit is distributed in the hope that it will be useful,
#~ but WITHOUT ANY WARRANTY; without even the implied warranty of
#~ MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#~ GNU General Public License for more details.

#~ You should have received a copy of the GNU General Public License
#~ along with Sequence-ToolKit.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
	
	widget=QtGui.QDesktopWidget()
	mainScreenSize = widget.availableGeometry(widget.primaryScreen())
	x= mainScreenSize.width()/2-168
	y= mainScreenSize.height()/2-115
	Dialog.setGeometry(QtCore.QRect(x, y, 336, 235))	
	Dialog.setMinimumSize(QtCore.QSize(336, 235))
        Dialog.setMaximumSize(QtCore.QSize(336, 235))
	
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(25, 10, 241, 17))
	
	self.check=QtGui.QCheckBox(Dialog)
	self.check.setGeometry(QtCore.QRect(3, 2, 20, 30))
	
        self.listWidget = QtGui.QListWidget(Dialog)
        self.listWidget.setGeometry(QtCore.QRect(0, 30, 241, 201))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.listWidget.addItem(item)
        
	self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(245, 8, 85, 27))
	self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(245, 43, 85, 27))
        self.pushButton_3 = QtGui.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(245, 78, 85, 27))
	self.pushButton_4 = QtGui.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(245, 113, 85, 27))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Profile", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Select the Parameters", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(QtGui.QApplication.translate("Dialog", "Beta Irradiation Time (s)", None, QtGui.QApplication.UnicodeUTF8))
        item = self.listWidget.item(1)
        item.setText(QtGui.QApplication.translate("Dialog", "Beta Dose (Gy)", None, QtGui.QApplication.UnicodeUTF8))
        item = self.listWidget.item(2)
        item.setText(QtGui.QApplication.translate("Dialog", "External Irradiation Time (s)", None, QtGui.QApplication.UnicodeUTF8))
        item = self.listWidget.item(3)
        item.setText(QtGui.QApplication.translate("Dialog", "External Dose (Gy)", None, QtGui.QApplication.UnicodeUTF8))
        item = self.listWidget.item(4)
        item.setText(QtGui.QApplication.translate("Dialog", "Preheating Temperature (°C)", None, QtGui.QApplication.UnicodeUTF8))
        item = self.listWidget.item(5)
        item.setText(QtGui.QApplication.translate("Dialog", "Measuring Temperature (°C)", None, QtGui.QApplication.UnicodeUTF8))
        item = self.listWidget.item(6)
        item.setText(QtGui.QApplication.translate("Dialog", "Preheating Rate (°C/s)", None, QtGui.QApplication.UnicodeUTF8))
        item = self.listWidget.item(7)
        item.setText(QtGui.QApplication.translate("Dialog", "Heating Rate (°C/s)", None, QtGui.QApplication.UnicodeUTF8))
        item = self.listWidget.item(8)
        item.setText(QtGui.QApplication.translate("Dialog", "Light Source", None, QtGui.QApplication.UnicodeUTF8))
        item = self.listWidget.item(9)
        item.setText(QtGui.QApplication.translate("Dialog", "Optical Power (%)", None, QtGui.QApplication.UnicodeUTF8))
        item = self.listWidget.item(10)
        item.setText(QtGui.QApplication.translate("Dialog", "Electric Stimulation (V)", None, QtGui.QApplication.UnicodeUTF8))
        item = self.listWidget.item(11)
        item.setText(QtGui.QApplication.translate("Dialog", "Electric Frequency (KHz)", None, QtGui.QApplication.UnicodeUTF8))
        item = self.listWidget.item(12)
        item.setText(QtGui.QApplication.translate("Dialog", "Time of Beta irradiation", None, QtGui.QApplication.UnicodeUTF8))
        item = self.listWidget.item(13)
        item.setText(QtGui.QApplication.translate("Dialog", "Time of External irradiation", None, QtGui.QApplication.UnicodeUTF8))
        item = self.listWidget.item(14)
        item.setText(QtGui.QApplication.translate("Dialog", "Time of Measurement", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("Dialog", "Accept", None, QtGui.QApplication.UnicodeUTF8))
	self.pushButton_3.setText(QtGui.QApplication.translate("Dialog", "Load", None, QtGui.QApplication.UnicodeUTF8))
	self.pushButton_4.setText(QtGui.QApplication.translate("Dialog", "Save", None, QtGui.QApplication.UnicodeUTF8))

