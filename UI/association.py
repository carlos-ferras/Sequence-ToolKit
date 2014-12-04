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
#~ along with LF02_package.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4 import QtCore, QtGui
from style import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        widget=QtGui.QDesktopWidget()
	mainScreenSize = widget.availableGeometry(widget.primaryScreen())
	self.x= mainScreenSize.width()/2-238
	self.y= mainScreenSize.height()/2-110
	Dialog.setGeometry(QtCore.QRect(self.x, self.y, 477, 101))	
	Dialog.setMinimumSize(QtCore.QSize(477, 101))
        Dialog.setMaximumSize(QtCore.QSize(477, 101))
	
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(10, 30, 231, 27))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
	self.comboBox_5 = QtGui.QComboBox(Dialog)
        self.comboBox_5.setGeometry(QtCore.QRect(250, 30, 131, 27))
        self.comboBox_5.setObjectName(_fromUtf8("comboBox_5"))
        self.comboBox_5.addItem(_fromUtf8(""))
        self.comboBox_5.addItem(_fromUtf8(""))
        self.comboBox_5.addItem(_fromUtf8(""))
        self.comboBox_5.addItem(_fromUtf8(""))
	self.comboBox_5.setEnabled(False)
	self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(390, 30, 51, 23))
        self.lineEdit.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
	self.lineEdit.setEnabled(False)
	
	self.comboBox_2 = QtGui.QComboBox(Dialog)
        self.comboBox_2.setGeometry(QtCore.QRect(10, 70, 231, 27))
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.comboBox_2.addItem(_fromUtf8(""))
	self.comboBox_2.setVisible(False)
	self.comboBox_6 = QtGui.QComboBox(Dialog)
        self.comboBox_6.setGeometry(QtCore.QRect(250, 70, 131, 27))
        self.comboBox_6.setObjectName(_fromUtf8("comboBox_6"))
        self.comboBox_6.addItem(_fromUtf8(""))
        self.comboBox_6.addItem(_fromUtf8(""))
        self.comboBox_6.addItem(_fromUtf8(""))
        self.comboBox_6.addItem(_fromUtf8(""))
	self.comboBox_6.setVisible(False)
	self.comboBox_6.setEnabled(False)
	self.lineEdit_2 = QtGui.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(390, 70, 51, 23))
        self.lineEdit_2.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
	self.lineEdit_2.setVisible(False)
	self.lineEdit_2.setEnabled(False)
	
        self.comboBox_3 = QtGui.QComboBox(Dialog)
        self.comboBox_3.setGeometry(QtCore.QRect(10, 110, 231, 27))
        self.comboBox_3.setObjectName(_fromUtf8("comboBox_3"))
        self.comboBox_3.addItem(_fromUtf8(""))
	self.comboBox_3.setVisible(False)
	self.comboBox_7 = QtGui.QComboBox(Dialog)
        self.comboBox_7.setGeometry(QtCore.QRect(250, 110, 131, 27))
        self.comboBox_7.setObjectName(_fromUtf8("comboBox_7"))
        self.comboBox_7.addItem(_fromUtf8(""))
        self.comboBox_7.addItem(_fromUtf8(""))
        self.comboBox_7.addItem(_fromUtf8(""))
        self.comboBox_7.addItem(_fromUtf8(""))	
	self.comboBox_7.setVisible(False)
	self.comboBox_7.setEnabled(False)
	self.lineEdit_3 = QtGui.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(390, 110, 51, 23))
        self.lineEdit_3.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
	self.lineEdit_3.setVisible(False)
	self.lineEdit_3.setEnabled(False)
	
        self.comboBox_4 = QtGui.QComboBox(Dialog)
        self.comboBox_4.setGeometry(QtCore.QRect(10, 150, 231, 27))
        self.comboBox_4.setObjectName(_fromUtf8("comboBox_4"))
        self.comboBox_4.addItem(_fromUtf8(""))
	self.comboBox_4.setVisible(False)
	self.comboBox_8 = QtGui.QComboBox(Dialog)
        self.comboBox_8.setGeometry(QtCore.QRect(250, 150, 131, 27))
        self.comboBox_8.setObjectName(_fromUtf8("comboBox_8"))
        self.comboBox_8.addItem(_fromUtf8(""))
        self.comboBox_8.addItem(_fromUtf8(""))
        self.comboBox_8.addItem(_fromUtf8(""))
        self.comboBox_8.addItem(_fromUtf8(""))
	self.comboBox_8.setVisible(False)
	self.comboBox_8.setEnabled(False)
	self.lineEdit_4 = QtGui.QLineEdit(Dialog)
        self.lineEdit_4.setGeometry(QtCore.QRect(390, 150, 51, 23))
        self.lineEdit_4.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
	self.lineEdit_4.setVisible(False)
	self.lineEdit_4.setEnabled(False)
	
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 101, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(250, 10, 131, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))        
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(390, 10, 51, 17))
        self.label_3.setObjectName(_fromUtf8("label_3"))	
        
        
        self.toolButton = QtGui.QToolButton(Dialog)
        self.toolButton.setGeometry(QtCore.QRect(450, 30, 31, 21))
        self.toolButton.setText(_fromUtf8(""))
        self.toolButton.setStyleSheet(TOOLBUTTON_STYLE)
	icon = QtGui.QIcon()
	icon.addPixmap(QtGui.QPixmap("pixmaps/icons/plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
	self.toolButton.setIcon(icon)
        
	self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(390, 70, 85, 27))
        self.pushButton.setStyleSheet(BUTTON_STYLE)
        self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(300, 70, 85, 27))
        self.pushButton_2.setStyleSheet(BUTTON_STYLE)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Group Cells", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Criterion", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Condition", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Value", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Cancelar", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("Dialog", "Aceptar", None, QtGui.QApplication.UnicodeUTF8))
	self.toolButton.setToolTip(QtGui.QApplication.translate("Dialog", "Add Criterion", None, QtGui.QApplication.UnicodeUTF8))

	self.comboBox.setItemText(0, QtGui.QApplication.translate("Dialog", "<<select>>", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2.setItemText(0, QtGui.QApplication.translate("Dialog", "<<select>>", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_3.setItemText(0, QtGui.QApplication.translate("Dialog", "<<select>>", None, QtGui.QApplication.UnicodeUTF8))
	self.comboBox_4.setItemText(0, QtGui.QApplication.translate("Dialog", "<<select>>", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_5.setItemText(0, QtGui.QApplication.translate("Dialog", "Same", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_5.setItemText(1, QtGui.QApplication.translate("Dialog", "Different", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_5.setItemText(2, QtGui.QApplication.translate("Dialog", "Numeric Value", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_5.setItemText(3, QtGui.QApplication.translate("Dialog", "String Value", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_6.setItemText(0, QtGui.QApplication.translate("Dialog", "Same", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_6.setItemText(1, QtGui.QApplication.translate("Dialog", "Different", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_6.setItemText(2, QtGui.QApplication.translate("Dialog", "Numeric Value", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_6.setItemText(3, QtGui.QApplication.translate("Dialog", "String Value", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_7.setItemText(0, QtGui.QApplication.translate("Dialog", "Same", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_7.setItemText(1, QtGui.QApplication.translate("Dialog", "Different", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_7.setItemText(2, QtGui.QApplication.translate("Dialog", "Numeric Value", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_7.setItemText(3, QtGui.QApplication.translate("Dialog", "String Value", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_8.setItemText(0, QtGui.QApplication.translate("Dialog", "Same", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_8.setItemText(1, QtGui.QApplication.translate("Dialog", "Different", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_8.setItemText(2, QtGui.QApplication.translate("Dialog", "Numeric Value", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_8.setItemText(3, QtGui.QApplication.translate("Dialog", "String Value", None, QtGui.QApplication.UnicodeUTF8))
        
