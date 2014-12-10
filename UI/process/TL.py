#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#~ Copyright (C) 2014 Carlos Manuel Ferras Hernandez <c4rlos.ferra5@gmail.com>
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
	x= mainScreenSize.width()/2-273
	y= mainScreenSize.height()/2-85
	Dialog.setGeometry(QtCore.QRect(x, y, 546, 169))
        Dialog.setMinimumSize(QtCore.QSize(546, 169))
        Dialog.setMaximumSize(QtCore.QSize(546, 169))
        self.frame = QtGui.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(6, 10, 444, 151))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
	self.frame.setStyleSheet(PROCESS_WIN_STYLE)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.doubleSpinBox = QtGui.QDoubleSpinBox(self.frame)
        self.doubleSpinBox.setGeometry(QtCore.QRect(285, 67, 62, 27))
        self.doubleSpinBox.setMinimum(0.1)
        self.doubleSpinBox.setMaximum(20.0)
        self.doubleSpinBox.setObjectName(_fromUtf8("doubleSpinBox"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(160, 70, 131, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(10, 20, 141, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(235, 20, 151, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_5 = QtGui.QLabel(self.frame)
        self.label_5.setGeometry(QtCore.QRect(10, 70, 81, 17))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.doubleSpinBox_2 = QtGui.QDoubleSpinBox(self.frame)
        self.doubleSpinBox_2.setGeometry(QtCore.QRect(155, 16, 62, 27))
        self.doubleSpinBox_2.setMaximum(600.0)
        self.doubleSpinBox_2.setObjectName(_fromUtf8("doubleSpinBox_2"))
        self.doubleSpinBox_3 = QtGui.QDoubleSpinBox(self.frame)
        self.doubleSpinBox_3.setGeometry(QtCore.QRect(375, 16, 62, 27))
        self.doubleSpinBox_3.setMaximum(999999999.0)
        self.doubleSpinBox_3.setObjectName(_fromUtf8("doubleSpinBox_3"))
        self.spinBox = QtGui.QSpinBox(self.frame)
        self.spinBox.setGeometry(QtCore.QRect(70, 67, 54, 27))
        self.spinBox.setMaximum(512)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.check=QtGui.QCheckBox(self.frame)
        self.check.setGeometry(QtCore.QRect(10, 110, 150, 30))
	
	self.pushButton = QtGui.QPushButton(Dialog)
	self.pushButton.setStyleSheet(PROCESS_BUTTONS_STYLE)
        self.pushButton.setGeometry(QtCore.QRect(454, 10, 91, 26))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(Dialog)
	self.pushButton_2.setStyleSheet(PROCESS_BUTTONS_STYLE)
        self.pushButton_2.setGeometry(QtCore.QRect(454, 50, 91, 26))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(Dialog)
	self.pushButton_3.setStyleSheet(PROCESS_BUTTONS_STYLE)
        self.pushButton_3.setGeometry(QtCore.QRect(454, 90, 88, 26))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("MainWindow", "TL", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Accept", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("MainWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Heating Rate (°C/s)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Final Temperature (°C)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Time at Final Temp (s)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Channel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("MainWindow", "&Sample Info.", None, QtGui.QApplication.UnicodeUTF8))
	self.check.setText(QtGui.QApplication.translate("MainWindow", "Save Temp.", None, QtGui.QApplication.UnicodeUTF8))

