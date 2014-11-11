#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#~ Copyright (C) 2014 Carlos Manuel Ferras Hernandez
#~ This file is part of LF02_package.

#~ LF02_package is free software: you can redistribute it and/or modify
#~ it under the terms of the GNU General Public License as published by
#~ the Free Software Foundation, either version 3 of the License, or
#~ (at your option) any later version.

#~ LF02_package is distributed in the hope that it will be useful,
#~ but WITHOUT ANY WARRANTY; without even the implied warranty of
#~ MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#~ GNU General Public License for more details.

#~ You should have received a copy of the GNU General Public License
#~ along with LF02_package.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4 import QtCore, QtGui
from style import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        widget=QtGui.QDesktopWidget()
	mainScreenSize = widget.availableGeometry(widget.primaryScreen())
	x= mainScreenSize.width()/2-262
	y= mainScreenSize.height()/2-77
	Dialog.setGeometry(QtCore.QRect(x, y, 524, 157))
        Dialog.setMinimumSize(QtCore.QSize(524, 157))
        Dialog.setMaximumSize(QtCore.QSize(524, 157))
        self.frame = QtGui.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(6, 10, 420, 141))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
	self.frame.setStyleSheet(PROCESS_WIN_STYLE)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.doubleSpinBox = QtGui.QDoubleSpinBox(self.frame)
        self.doubleSpinBox.setGeometry(QtCore.QRect(135, 55, 61, 27))
        self.doubleSpinBox.setMinimum(0.1)
        self.doubleSpinBox.setMaximum(20.0)
        self.doubleSpinBox.setObjectName(_fromUtf8("doubleSpinBox"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(10, 60, 131, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 141, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(10, 110, 101, 17))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.doubleSpinBox_2 = QtGui.QDoubleSpinBox(self.frame)
        self.doubleSpinBox_2.setGeometry(QtCore.QRect(155, 6, 62, 27))
        self.doubleSpinBox_2.setMaximum(600.0)
        self.doubleSpinBox_2.setObjectName(_fromUtf8("doubleSpinBox_2"))
        self.doubleSpinBox_3 = QtGui.QDoubleSpinBox(self.frame)
        self.doubleSpinBox_3.setGeometry(QtCore.QRect(115, 106, 62, 27))
        self.doubleSpinBox_3.setMaximum(999999999.0)
        self.doubleSpinBox_3.setObjectName(_fromUtf8("doubleSpinBox_3"))
        self.label_10 = QtGui.QLabel(self.frame)
        self.label_10.setGeometry(QtCore.QRect(230, 60, 121, 17))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.comboBox = QtGui.QComboBox(self.frame)
        self.comboBox.setGeometry(QtCore.QRect(315, 55, 61, 27))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.label_11 = QtGui.QLabel(self.frame)
        self.label_11.setGeometry(QtCore.QRect(230, 110, 61, 17))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.label_12 = QtGui.QLabel(self.frame)
        self.label_12.setGeometry(QtCore.QRect(230, 10, 131, 17))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.spinBox_5 = QtGui.QSpinBox(self.frame)
        self.spinBox_5.setGeometry(QtCore.QRect(350, 6, 61, 27))
        self.spinBox_5.setMaximum(100)
        self.spinBox_5.setObjectName(_fromUtf8("spinBox_5"))
        self.line = QtGui.QFrame(self.frame)
        self.line.setGeometry(QtCore.QRect(212, 10, 20, 121))
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.doubleSpinBox_4 = QtGui.QDoubleSpinBox(self.frame)
        self.doubleSpinBox_4.setGeometry(QtCore.QRect(287, 106, 62, 27))
        self.doubleSpinBox_4.setMaximum(999999999.0)
        self.doubleSpinBox_4.setObjectName(_fromUtf8("doubleSpinBox_4"))
        self.pushButton = QtGui.QPushButton(Dialog)
	self.pushButton.setStyleSheet(PROCESS_BUTTONS_STYLE)
        self.pushButton.setGeometry(QtCore.QRect(430, 10, 91, 26))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(Dialog)
	self.pushButton_2.setStyleSheet(PROCESS_BUTTONS_STYLE)
        self.pushButton_2.setGeometry(QtCore.QRect(430, 50, 91, 26))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(Dialog)
	self.pushButton_3.setStyleSheet(PROCESS_BUTTONS_STYLE)
        self.pushButton_3.setGeometry(QtCore.QRect(430, 90, 88, 26))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Ilumination", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Heating Rate (°C/s)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Final Temperature (°C)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Stabilization (s)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("MainWindow", "Ligth Source", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(0, "Blue")
        self.comboBox.setItemText(1, "IR")
        self.comboBox.setItemText(2, "AUX")
        self.label_11.setText(QtGui.QApplication.translate("MainWindow", "Time (s)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("MainWindow", "Optical Power (%)", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Accept", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("MainWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("MainWindow", "&Sample Info.", None, QtGui.QApplication.UnicodeUTF8))

