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
		
		
		
		
		
		
		
		
		
		