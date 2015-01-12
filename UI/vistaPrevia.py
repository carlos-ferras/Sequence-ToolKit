#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#~ Copyright (C) 2014 Carlos Manuel Ferras Hernandez <c4rlos.ferra5@gmail.com>
#~ This file is part of Secuence-ToolKit.

#~ Secuence-ToolKit is free software: you can redistribute it and/or modify
#~ it under the terms of the GNU General Public License as published by
#~ the Free Software Foundation, either version 3 of the License, or
#~ (at your option) any later version.

#~ Secuence-ToolKit is distributed in the hope that it will be useful,
#~ but WITHOUT ANY WARRANTY; without even the implied warranty of
#~ MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#~ GNU General Public License for more details.

#~ You should have received a copy of the GNU General Public License
#~ along with Secuence-ToolKit.  If not, see <http://www.gnu.org/licenses/>.

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
	x= mainScreenSize.width()/2-350
	y= mainScreenSize.height()/2-273
	Dialog.setGeometry(QtCore.QRect(x, y, 700,546))
        Dialog.setMinimumSize(QtCore.QSize(700, 546))
        Dialog.setMaximumSize(QtCore.QSize(700, 546))
        self.textEdit = QtGui.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(0, 40, 700, 511))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Novason"))
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.textEdit.setFont(font)
        self.textEdit.setReadOnly(True)
        self.textEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
       
	self.toolButton = QtGui.QToolButton(Dialog)
	icon = QtGui.QIcon()
	icon.addPixmap(QtGui.QPixmap(_fromUtf8("pixmaps/icons/save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
	self.toolButton.setIcon(icon)
	self.toolButton.setIconSize(QtCore.QSize(31, 31))
	self.toolButton.setGeometry(QtCore.QRect(0, 5, 31, 31))
	self.toolButton.setText(_fromUtf8(""))
	self.toolButton.setObjectName(_fromUtf8("toolButton"))
	self.toolButton.setToolTip(QtGui.QApplication.translate("MainWindow",'Save', None, QtGui.QApplication.UnicodeUTF8))
	self.toolButton.setStyleSheet(TOOLBUTTON_STYLE)
	
	self.toolButton_2 = QtGui.QToolButton(Dialog)
	icon = QtGui.QIcon()
	icon.addPixmap(QtGui.QPixmap(_fromUtf8("pixmaps/icons/save_as.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
	self.toolButton_2.setIcon(icon)
	self.toolButton_2.setIconSize(QtCore.QSize(31, 31))
	self.toolButton_2.setGeometry(QtCore.QRect(40, 5, 31, 31))
	self.toolButton_2.setText(_fromUtf8(""))
	self.toolButton_2.setObjectName(_fromUtf8("toolButton_2"))
	self.toolButton_2.setToolTip(QtGui.QApplication.translate("MainWindow",'Save as', None, QtGui.QApplication.UnicodeUTF8))
	self.toolButton_2.setStyleSheet(TOOLBUTTON_STYLE)

	

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Preview", None, QtGui.QApplication.UnicodeUTF8))
        self.textEdit.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Novason\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:600;\"><br /></p></body></html>")

