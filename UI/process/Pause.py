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
	x= mainScreenSize.width()/2-117
	y= mainScreenSize.height()/2-60
	Dialog.setGeometry(QtCore.QRect(x, y, 234, 120))
        Dialog.setMinimumSize(QtCore.QSize(234, 120))
        Dialog.setMaximumSize(QtCore.QSize(234, 120))
        self.frame = QtGui.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(6, 10, 131, 104))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
	self.frame.setStyleSheet(PROCESS_WIN_STYLE)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.label_11 = QtGui.QLabel(self.frame)
        self.label_11.setGeometry(QtCore.QRect(10, 20, 61, 17))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.doubleSpinBox = QtGui.QDoubleSpinBox(self.frame)
        self.doubleSpinBox.setGeometry(QtCore.QRect(65, 16, 62, 27))
        self.doubleSpinBox.setMaximum(999999999.0)
        self.doubleSpinBox.setObjectName(_fromUtf8("doubleSpinBox"))
        self.pushButton = QtGui.QPushButton(Dialog)
	self.pushButton.setStyleSheet(PROCESS_BUTTONS_STYLE)
        self.pushButton.setGeometry(QtCore.QRect(140, 10, 91, 26))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(Dialog)
	self.pushButton_2.setStyleSheet(PROCESS_BUTTONS_STYLE)
        self.pushButton_2.setGeometry(QtCore.QRect(140, 50, 91, 26))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(Dialog)
	self.pushButton_3.setStyleSheet(PROCESS_BUTTONS_STYLE)
        self.pushButton_3.setGeometry(QtCore.QRect(140, 90, 88, 26))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Pause", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("MainWindow", "Time (s)", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Accept", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("MainWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("MainWindow", "&Sample Info.", None, QtGui.QApplication.UnicodeUTF8))

