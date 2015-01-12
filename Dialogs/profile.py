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

from PyQt4 import QtCore  
from PyQt4 import QtGui 
from UI import profile

class Profile(profile.Ui_Dialog):
	"""Ventana para seleccionar fuente"""
	def __init__(self,parameters,parent=None):
		self.form1 =QtGui.QMainWindow(parent)
		self.setupUi(self.form1)
		self.fill(parameters)		
		self.form1.show()
		
		self.pushButton.setShortcut("Escape")
		self.pushButton.clicked.connect(self.form1.close)
		
		self.pushButton_2.setShortcut("Enter")
		
		self.check.clicked.connect(self.check_uncheck_all)

	def fill(self,parameters):
		for i in parameters:
			item = self.listWidget.item( i )
			item.setCheckState(2)			
	
	
	def fill_data(self):
		data=[]
		for i in range(self.listWidget.count()):
			item = self.listWidget.item( i )
			if item.checkState():
				data.append(i)
		return data
		
		
	def check_uncheck_all(self):		
		for i in range(self.listWidget.count()): 
			if self.check.isChecked():
				self.listWidget.item(i).setCheckState(QtCore.Qt.Checked)
			else:
				self.listWidget.item(i).setCheckState(QtCore.Qt.Unchecked)
		
		
		
		
		
		
		