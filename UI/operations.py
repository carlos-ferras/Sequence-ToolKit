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
		Dialog.resize(160, 260)
		Dialog.setMaximumSize(160, 260)
		Dialog.setMinimumSize(160, 260)			
		self.frame = QtGui.QFrame(Dialog)
		self.frame.setGeometry(QtCore.QRect(0, 0, 159, 260))		
		self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
		self.frame.setFrameShadow(QtGui.QFrame.Raised)
		self.frame.setObjectName(_fromUtf8("frame"))
		self.verticalLayoutWidget = QtGui.QWidget(self.frame)
		self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 159, 260))
		self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
		self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
		self.verticalLayout.setSpacing(0)
		self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
		self.verticalLayout.setContentsMargins(2, 3, 2, 3)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		
		font = QtGui.QFont()
		font.setFamily(_fromUtf8("Novason"))
		font.setPointSize(12)
		font.setBold(False)
		font.setItalic(False)
		font.setUnderline(False)
		font.setWeight(53)
		font.setStrikeOut(False)
		font.setKerning(False)
		font.setStyleStrategy(QtGui.QFont.PreferDefault)		
		
		self.pushButton_2 = QtGui.QPushButton(self.verticalLayoutWidget)
		self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
		self.pushButton_2.setFont(font)
		self.verticalLayout.addWidget(self.pushButton_2)		
		self.pushButton_3 = QtGui.QPushButton(self.verticalLayoutWidget)
		self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
		self.pushButton_3.setFont(font)
		self.verticalLayout.addWidget(self.pushButton_3)		
		self.pushButton_4 = QtGui.QPushButton(self.verticalLayoutWidget)
		self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
		self.pushButton_4.setFont(font)
		self.verticalLayout.addWidget(self.pushButton_4)
		self.pushButton_7 = QtGui.QPushButton(self.verticalLayoutWidget)
		self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))
		self.pushButton_7.setFont(font)
		self.verticalLayout.addWidget(self.pushButton_7)		
		self.pushButton_10 = QtGui.QPushButton(self.verticalLayoutWidget)
		self.pushButton_10.setObjectName(_fromUtf8("pushButton_10"))
		self.pushButton_10.setFont(font)
		self.verticalLayout.addWidget(self.pushButton_10)
		self.pushButton = QtGui.QPushButton(self.verticalLayoutWidget)
		self.pushButton.setObjectName(_fromUtf8("pushButton"))
		self.pushButton.setFont(font)
		self.verticalLayout.addWidget(self.pushButton)
		self.pushButton_8 = QtGui.QPushButton(self.verticalLayoutWidget)
		self.pushButton_8.setObjectName(_fromUtf8("pushButton_8"))
		self.pushButton_8.setFont(font)
		self.verticalLayout.addWidget(self.pushButton_8)
		self.pushButton_9 = QtGui.QPushButton(self.verticalLayoutWidget)
		self.pushButton_9.setObjectName(_fromUtf8("pushButton_9"))
		self.pushButton_9.setFont(font)
		self.verticalLayout.addWidget(self.pushButton_9)
		self.pushButton_5 = QtGui.QPushButton(self.verticalLayoutWidget)
		self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
		self.pushButton_5.setFont(font)
		self.verticalLayout.addWidget(self.pushButton_5)
		
		self.retranslateUi(Dialog)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Process    ", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("MainWindow", "TL", None, QtGui.QApplication.UnicodeUTF8))
	self.pushButton_10.setText(QtGui.QApplication.translate("MainWindow", "ESL", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("MainWindow", "OSL", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_5.setText(QtGui.QApplication.translate("MainWindow", "Pause", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_4.setText(QtGui.QApplication.translate("MainWindow", "POSL", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_7.setText(QtGui.QApplication.translate("MainWindow", "LMOSL", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Pre Heat", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_9.setText(QtGui.QApplication.translate("MainWindow", "Irradiation", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_8.setText(QtGui.QApplication.translate("MainWindow", "Illumination", None, QtGui.QApplication.UnicodeUTF8))
       
