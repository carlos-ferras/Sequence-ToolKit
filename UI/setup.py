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
from process.style import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
	
	widget=QtGui.QDesktopWidget()
	mainScreenSize = widget.availableGeometry(widget.primaryScreen())
	x= mainScreenSize.width()/2-192
	y= mainScreenSize.height()/2-123
	Dialog.setGeometry(QtCore.QRect(x, y, 450, 247))	
	Dialog.setMinimumSize(QtCore.QSize(450, 247))
        Dialog.setMaximumSize(QtCore.QSize(450, 247))
	
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 450, 210))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        
	self.tab = QtGui.QWidget()
        self.tabWidget.addTab(self.tab, _fromUtf8(""))	
	self.radiobutton=QtGui.QRadioButton(self.tab)	
	self.radiobutton.setGeometry(QtCore.QRect(10, 10, 200, 30))
	self.radiobutton_1=QtGui.QRadioButton(self.tab)
	self.radiobutton_1.setGeometry(QtCore.QRect(10, 40, 200, 30))
	self.radiobutton_2=QtGui.QRadioButton(self.tab)
	self.radiobutton_2.setGeometry(QtCore.QRect(10, 70, 200, 30))
	
        self.tab_2 = QtGui.QWidget()
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
	self.label_11=QtGui.QLabel(self.tab_2)
	self.label_11.setGeometry(QtCore.QRect(10, 10, 200, 30))
	self.radiobutton_3=QtGui.QRadioButton(self.tab_2)
	self.radiobutton_3.setGeometry(QtCore.QRect(10, 40, 200, 30))
	self.radiobutton_4=QtGui.QRadioButton(self.tab_2)
	self.radiobutton_4.setGeometry(QtCore.QRect(10,70, 200, 30))
	
	self.tab_3 = QtGui.QWidget()
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
	self.label=QtGui.QLabel(self.tab_3)
	self.label.setGeometry(QtCore.QRect(10, 10, 200, 30))
	self.radiobutton_5=QtGui.QRadioButton(self.tab_3)
	self.radiobutton_5.setGeometry(QtCore.QRect(10, 40, 200, 30))
	self.radiobutton_6=QtGui.QRadioButton(self.tab_3)
	self.radiobutton_6.setGeometry(QtCore.QRect(10, 70, 200, 30))
	self.radiobutton_7=QtGui.QRadioButton(self.tab_3)
	self.radiobutton_7.setGeometry(QtCore.QRect(10, 100, 200, 30))
	self.line = QtGui.QFrame(self.tab_3)
        self.line.setGeometry(QtCore.QRect(80, 10, 10, 160))
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
	self.label_0=QtGui.QLabel(self.tab_3)
	self.label_0.setGeometry(QtCore.QRect(100, 10, 200, 30))
	self.label_1=QtGui.QLabel(self.tab_3)
	self.label_1.setGeometry(QtCore.QRect(100, 40, 200, 30))
	self.label_2=QtGui.QLabel(self.tab_3)
	self.label_2.setGeometry(QtCore.QRect(100, 70, 200, 30))
	self.label_3=QtGui.QLabel(self.tab_3)
	self.label_3.setGeometry(QtCore.QRect(100, 100, 200, 30))
	self.label_4=QtGui.QLabel(self.tab_3)
	self.label_4.setGeometry(QtCore.QRect(100, 130, 200, 30))
	self.radiobutton_8=QtGui.QRadioButton(self.tab_3)
	self.radiobutton_8.setGeometry(QtCore.QRect(190, 40, 200, 30))
	self.radiobutton_9=QtGui.QRadioButton(self.tab_3)
	self.radiobutton_9.setGeometry(QtCore.QRect(190, 70, 200, 30))
	self.radiobutton_10=QtGui.QRadioButton(self.tab_3)
	self.radiobutton_10.setGeometry(QtCore.QRect(190, 100, 200, 30))
	self.radiobutton_11=QtGui.QRadioButton(self.tab_3)
	self.radiobutton_11.setGeometry(QtCore.QRect(190, 130, 200, 30))
	self.radiobutton_12=QtGui.QRadioButton(self.tab_3)
	self.radiobutton_12.setGeometry(QtCore.QRect(280, 40, 200, 30))
	self.radiobutton_13=QtGui.QRadioButton(self.tab_3)
	self.radiobutton_13.setGeometry(QtCore.QRect(280, 70, 200, 30))
	self.radiobutton_14=QtGui.QRadioButton(self.tab_3)
	self.radiobutton_14.setGeometry(QtCore.QRect(280, 100, 200, 30))
	self.radiobutton_15=QtGui.QRadioButton(self.tab_3)
	self.radiobutton_15.setGeometry(QtCore.QRect(280, 130, 200, 30))
	self.doublesb_1=QtGui.QDoubleSpinBox(self.tab_3)
	self.doublesb_1.setGeometry(QtCore.QRect(350, 40, 80, 30))
	self.doublesb_2=QtGui.QDoubleSpinBox(self.tab_3)
	self.doublesb_2.setGeometry(QtCore.QRect(350, 70, 80, 30))
	self.doublesb_3=QtGui.QDoubleSpinBox(self.tab_3)
	self.doublesb_3.setGeometry(QtCore.QRect(350, 100, 80, 30))
	self.doublesb_4=QtGui.QDoubleSpinBox(self.tab_3)
	self.doublesb_4.setGeometry(QtCore.QRect(350, 130, 80, 30))
	
	self.tab_4 = QtGui.QWidget()
        self.tabWidget.addTab(self.tab_4, _fromUtf8(""))
	self.label_5=QtGui.QLabel(self.tab_4)
	self.label_5.setGeometry(QtCore.QRect(10, 10, 200, 30))
	self.radiobutton_16=QtGui.QRadioButton(self.tab_4)
	self.radiobutton_16.setGeometry(QtCore.QRect(10, 40, 200, 30))
	self.radiobutton_17=QtGui.QRadioButton(self.tab_4)
	self.radiobutton_17.setGeometry(QtCore.QRect(10, 70, 200, 30))
	self.radiobutton_18=QtGui.QRadioButton(self.tab_4)
	self.radiobutton_18.setGeometry(QtCore.QRect(10, 100, 200, 30))
	self.line_1 = QtGui.QFrame(self.tab_4)
        self.line_1.setGeometry(QtCore.QRect(80, 10, 10, 160))
        self.line_1.setFrameShape(QtGui.QFrame.VLine)
        self.line_1.setFrameShadow(QtGui.QFrame.Sunken)
	self.label_6=QtGui.QLabel(self.tab_4)
	self.label_6.setGeometry(QtCore.QRect(100, 10, 200, 30))
	self.label_7=QtGui.QLabel(self.tab_4)
	self.label_7.setGeometry(QtCore.QRect(100, 40, 200, 30))
	self.label_8=QtGui.QLabel(self.tab_4)
	self.label_8.setGeometry(QtCore.QRect(100, 70, 200, 30))
	self.label_9=QtGui.QLabel(self.tab_4)
	self.label_9.setGeometry(QtCore.QRect(100, 100, 200, 30))
	self.label_10=QtGui.QLabel(self.tab_4)
	self.label_10.setGeometry(QtCore.QRect(100, 130, 200, 30))
	self.radiobutton_19=QtGui.QRadioButton(self.tab_4)
	self.radiobutton_19.setGeometry(QtCore.QRect(190, 40, 200, 30))
	self.radiobutton_20=QtGui.QRadioButton(self.tab_4)
	self.radiobutton_20.setGeometry(QtCore.QRect(190, 70, 200, 30))
	self.radiobutton_21=QtGui.QRadioButton(self.tab_4)
	self.radiobutton_21.setGeometry(QtCore.QRect(190, 100, 200, 30))
	self.radiobutton_22=QtGui.QRadioButton(self.tab_4)
	self.radiobutton_22.setGeometry(QtCore.QRect(190, 130, 200, 30))
	self.radiobutton_23=QtGui.QRadioButton(self.tab_4)
	self.radiobutton_23.setGeometry(QtCore.QRect(280, 40, 200, 30))
	self.radiobutton_24=QtGui.QRadioButton(self.tab_4)
	self.radiobutton_24.setGeometry(QtCore.QRect(280, 70, 200, 30))
	self.radiobutton_25=QtGui.QRadioButton(self.tab_4)
	self.radiobutton_25.setGeometry(QtCore.QRect(280, 100, 200, 30))
	self.radiobutton_26=QtGui.QRadioButton(self.tab_4)
	self.radiobutton_26.setGeometry(QtCore.QRect(280, 130, 200, 30))
	self.doublesb_5=QtGui.QDoubleSpinBox(self.tab_4)
	self.doublesb_5.setGeometry(QtCore.QRect(350, 40, 80, 30))
	self.doublesb_6=QtGui.QDoubleSpinBox(self.tab_4)
	self.doublesb_6.setGeometry(QtCore.QRect(350, 70, 80, 30))
	self.doublesb_7=QtGui.QDoubleSpinBox(self.tab_4)
	self.doublesb_7.setGeometry(QtCore.QRect(350, 100, 80, 30))
	self.doublesb_8=QtGui.QDoubleSpinBox(self.tab_4)
	self.doublesb_8.setGeometry(QtCore.QRect(350, 130, 80, 30))
	
	self.pushButton = QtGui.QPushButton(Dialog)
	self.pushButton.setStyleSheet(PROCESS_BUTTONS_STYLE)
        self.pushButton.setGeometry(QtCore.QRect(260, 215, 91, 30))		
	self.pushButton_2 = QtGui.QPushButton(Dialog)
	self.pushButton.setStyleSheet(PROCESS_BUTTONS_STYLE)
        self.pushButton_2.setGeometry(QtCore.QRect(355, 215, 91, 30))	

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Form", "SetUp", None, QtGui.QApplication.UnicodeUTF8))
        
	self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("Form", "Curve to Show", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("Form", "For TL", None, QtGui.QApplication.UnicodeUTF8))
	self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("Form", "Format Horizontal Axis", None, QtGui.QApplication.UnicodeUTF8))
	self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QtGui.QApplication.translate("Form", "Format Vertical Axis", None, QtGui.QApplication.UnicodeUTF8))
	
	self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Accept", None, QtGui.QApplication.UnicodeUTF8))
	self.pushButton_2.setText(QtGui.QApplication.translate("MainWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
	
	self.radiobutton.setText(QtGui.QApplication.translate("MainWindow", "Curve", None, QtGui.QApplication.UnicodeUTF8)+' 1')
	self.radiobutton_1.setText(QtGui.QApplication.translate("MainWindow", "Curve", None, QtGui.QApplication.UnicodeUTF8)+' 2')
	self.radiobutton_2.setText(QtGui.QApplication.translate("MainWindow", "Curve", None, QtGui.QApplication.UnicodeUTF8)+' 3')
	
	self.label_11.setText(QtGui.QApplication.translate("MainWindow", "Show", None, QtGui.QApplication.UnicodeUTF8))
	self.radiobutton_3.setText(QtGui.QApplication.translate("MainWindow", "Curve vs Time", None, QtGui.QApplication.UnicodeUTF8))
	self.radiobutton_4.setText(QtGui.QApplication.translate("MainWindow", "Curve vs Temperature", None, QtGui.QApplication.UnicodeUTF8))
	
	self.label.setText(QtGui.QApplication.translate("MainWindow", "Scale", None, QtGui.QApplication.UnicodeUTF8))
	self.radiobutton_5.setText(QtGui.QApplication.translate("MainWindow", "Lineal", None, QtGui.QApplication.UnicodeUTF8))
	self.radiobutton_6.setText(QtGui.QApplication.translate("MainWindow", "Log10", None, QtGui.QApplication.UnicodeUTF8))
	self.radiobutton_7.setText(QtGui.QApplication.translate("MainWindow", "Ln", None, QtGui.QApplication.UnicodeUTF8))
	self.label_1.setText(QtGui.QApplication.translate("MainWindow", "Minimum", None, QtGui.QApplication.UnicodeUTF8))
	self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Maximum", None, QtGui.QApplication.UnicodeUTF8))
	self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Greater unity", None, QtGui.QApplication.UnicodeUTF8))
	self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Smallest unit", None, QtGui.QApplication.UnicodeUTF8))
	self.radiobutton_8.setText(QtGui.QApplication.translate("MainWindow", "Automatic", None, QtGui.QApplication.UnicodeUTF8))
	self.radiobutton_9.setText(QtGui.QApplication.translate("MainWindow", "Automatic", None, QtGui.QApplication.UnicodeUTF8))
	self.radiobutton_10.setText(QtGui.QApplication.translate("MainWindow", "Automatic", None, QtGui.QApplication.UnicodeUTF8))
	self.radiobutton_11.setText(QtGui.QApplication.translate("MainWindow", "Automatic", None, QtGui.QApplication.UnicodeUTF8))
	self.radiobutton_12.setText(QtGui.QApplication.translate("MainWindow", "Fixed", None, QtGui.QApplication.UnicodeUTF8))
	self.radiobutton_13.setText(QtGui.QApplication.translate("MainWindow", "Fixed", None, QtGui.QApplication.UnicodeUTF8))
	self.radiobutton_14.setText(QtGui.QApplication.translate("MainWindow", "Fixed", None, QtGui.QApplication.UnicodeUTF8))
	self.radiobutton_15.setText(QtGui.QApplication.translate("MainWindow", "Fixed", None, QtGui.QApplication.UnicodeUTF8))
	self.label_0.setText(QtGui.QApplication.translate("MainWindow", "Axis values", None, QtGui.QApplication.UnicodeUTF8))
	
	self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Scale", None, QtGui.QApplication.UnicodeUTF8))
	self.radiobutton_16.setText(QtGui.QApplication.translate("MainWindow", "Lineal", None, QtGui.QApplication.UnicodeUTF8))
	self.radiobutton_17.setText(QtGui.QApplication.translate("MainWindow", "Log10", None, QtGui.QApplication.UnicodeUTF8))
	self.radiobutton_18.setText(QtGui.QApplication.translate("MainWindow", "Ln", None, QtGui.QApplication.UnicodeUTF8))
	self.label_7.setText(QtGui.QApplication.translate("MainWindow", "Minimum", None, QtGui.QApplication.UnicodeUTF8))
	self.label_8.setText(QtGui.QApplication.translate("MainWindow", "Maximum", None, QtGui.QApplication.UnicodeUTF8))
	self.label_9.setText(QtGui.QApplication.translate("MainWindow", "Greater unity", None, QtGui.QApplication.UnicodeUTF8))
	self.label_10.setText(QtGui.QApplication.translate("MainWindow", "Smallest unit", None, QtGui.QApplication.UnicodeUTF8))
	self.radiobutton_19.setText(QtGui.QApplication.translate("MainWindow", "Automatic", None, QtGui.QApplication.UnicodeUTF8))
	self.radiobutton_20.setText(QtGui.QApplication.translate("MainWindow", "Automatic", None, QtGui.QApplication.UnicodeUTF8))
	self.radiobutton_21.setText(QtGui.QApplication.translate("MainWindow", "Automatic", None, QtGui.QApplication.UnicodeUTF8))
	self.radiobutton_22.setText(QtGui.QApplication.translate("MainWindow", "Automatic", None, QtGui.QApplication.UnicodeUTF8))
	self.radiobutton_23.setText(QtGui.QApplication.translate("MainWindow", "Fixed", None, QtGui.QApplication.UnicodeUTF8))
	self.radiobutton_24.setText(QtGui.QApplication.translate("MainWindow", "Fixed", None, QtGui.QApplication.UnicodeUTF8))
	self.radiobutton_25.setText(QtGui.QApplication.translate("MainWindow", "Fixed", None, QtGui.QApplication.UnicodeUTF8))
	self.radiobutton_26.setText(QtGui.QApplication.translate("MainWindow", "Fixed", None, QtGui.QApplication.UnicodeUTF8))
	self.label_6.setText(QtGui.QApplication.translate("MainWindow", "Axis values", None, QtGui.QApplication.UnicodeUTF8))
	
	
	
	