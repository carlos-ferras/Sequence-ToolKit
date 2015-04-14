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

class classUiProcess(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        widget=QtGui.QDesktopWidget()
	mainScreenSize = widget.availableGeometry(widget.primaryScreen())
	x= mainScreenSize.width()/2-251
	y= mainScreenSize.height()/2-79
	Dialog.setGeometry(QtCore.QRect(x, y, 502, 158))
        Dialog.setMinimumSize(QtCore.QSize(502, 158))
        Dialog.setMaximumSize(QtCore.QSize(502, 158))
        self.frame = QtGui.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(6, 10, 400, 141))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.comboBox = QtGui.QComboBox(self.frame)
        self.comboBox.setGeometry(QtCore.QRect(130, 16, 78, 27))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.label_4 = QtGui.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(10, 20, 121, 17))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.doubleSpinBox = QtGui.QDoubleSpinBox(self.frame)
        self.doubleSpinBox.setGeometry(QtCore.QRect(335, 104, 61, 27))
        self.doubleSpinBox.setMinimum(0.1)
        self.doubleSpinBox.setMaximum(20.0)
        self.doubleSpinBox.setObjectName(_fromUtf8("doubleSpinBox"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(210, 110, 121, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.doubleSpinBox_2 = QtGui.QDoubleSpinBox(self.frame)
        self.doubleSpinBox_2.setGeometry(QtCore.QRect(156, 64, 62, 27))
        self.doubleSpinBox_2.setMaximum(600.0)
        self.doubleSpinBox_2.setObjectName(_fromUtf8("doubleSpinBox_2"))
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 141, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.line = QtGui.QFrame(self.frame)
        self.line.setGeometry(QtCore.QRect(10, 50, 210, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(10, 110, 150, 17))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.doubleSpinBox_3 = QtGui.QDoubleSpinBox(self.frame)
        self.doubleSpinBox_3.setGeometry(QtCore.QRect(115, 104, 62, 27))
        self.doubleSpinBox_3.setMaximum(99999999.0)
        self.doubleSpinBox_3.setObjectName(_fromUtf8("doubleSpinBox_3"))
        self.label_11 = QtGui.QLabel(self.frame)
        self.label_11.setGeometry(QtCore.QRect(230, 20, 61, 17))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.label_5 = QtGui.QLabel(self.frame)
        self.label_5.setGeometry(QtCore.QRect(243, 70, 61, 17))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.line_2 = QtGui.QFrame(self.frame)
        self.line_2.setGeometry(QtCore.QRect(222, 90, 171, 16))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.label_6 = QtGui.QLabel(self.frame)
        self.label_6.setGeometry(QtCore.QRect(313, 70, 61, 17))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.doubleSpinBox_4 = QtGui.QDoubleSpinBox(self.frame)
        self.doubleSpinBox_4.setGeometry(QtCore.QRect(287, 16, 62, 27))
        self.doubleSpinBox_4.setMaximum(999999999.0)
        self.doubleSpinBox_4.setObjectName(_fromUtf8("doubleSpinBox_4"))
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(410, 10, 91, 26))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(410, 50, 91, 26))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(410, 90, 88, 26))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Irradiation", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(0, "Beta")
        self.comboBox.setItemText(1, "External")
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Irradiation Source", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Heating Rate (°C/s)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Final Temperature (°C)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Stabilization (s)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("MainWindow", "Time (s)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Dose (Gy)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText("0")
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "&Accept", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("MainWindow", "&Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("MainWindow", "&Info", None, QtGui.QApplication.UnicodeUTF8))

