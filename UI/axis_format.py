# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'axis_format.ui'
#
# Created: Mon Dec  1 11:41:16 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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
	
        self.tab_2 = QtGui.QWidget()
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
	
	self.tab_3 = QtGui.QWidget()
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
	
	self.tab_4 = QtGui.QWidget()
        self.tabWidget.addTab(self.tab_4, _fromUtf8(""))
	
	
	self.checkbox=QtGui.QCheckBox(Dialog)
	self.checkbox.setGeometry(QtCore.QRect(10, 215, 200, 30))
	
	self.pushButton = QtGui.QPushButton(Dialog)
	#self.pushButton.setStyleSheet(PROCESS_BUTTONS_STYLE)
        self.pushButton.setGeometry(QtCore.QRect(260, 215, 91, 30))	
	self.pushButton_2 = QtGui.QPushButton(Dialog)
	#self.pushButton.setStyleSheet(PROCESS_BUTTONS_STYLE)
        self.pushButton_2.setGeometry(QtCore.QRect(355, 215, 91, 30))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Form", "SetUp", None, QtGui.QApplication.UnicodeUTF8))
        
	self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("Form", "Curve to Show", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("Form", "For TL", None, QtGui.QApplication.UnicodeUTF8))
	self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("Form", "Format Horizontal Axis", None, QtGui.QApplication.UnicodeUTF8))
	self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QtGui.QApplication.translate("Form", "Format Vertical Axis", None, QtGui.QApplication.UnicodeUTF8))
	self.checkbox.setText(QtGui.QApplication.translate("MainWindow", "Not show this message again", None, QtGui.QApplication.UnicodeUTF8))
	self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Accept", None, QtGui.QApplication.UnicodeUTF8))
	self.pushButton_2.setText(QtGui.QApplication.translate("MainWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
