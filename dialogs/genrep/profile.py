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
from ui.genrep import uiProfile
import time
import os

class classProfile(uiProfile.classUiProfile):
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
		self.pushButton_3.clicked.connect(self.load)
		self.pushButton_4.clicked.connect(self.save)
		
		self.dir='/'

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
		
		
	def save(self):
		s=''
		dir=str(QtGui.QFileDialog.getSaveFileName(
					self.form1,
					QtGui.QApplication.translate('MainWindow',"Save"),
					self.dir+s.join(str(time.time()).split('.'))+'.grprofile',
					QtGui.QApplication.translate('MainWindow','File')+' grprofile (*.grprofile)',
				))	
		if dir:
			self.dir=os.path.dirname(dir)
			
			file=open(dir,'w+').close()
			file=open(dir,'w+')
			file.write(str(self.fill_data()))
			file.close()
			
	
	def load(self):		
		dir=str(QtGui.QFileDialog.getOpenFileName(
					self.form1,
					QtGui.QApplication.translate('MainWindow',"Load") +" GenRep"+QtGui.QApplication.translate('MainWindow',"Profile") ,
					self.dir,
					QtGui.QApplication.translate('MainWindow','File')+' grprofile (*.grprofile)', 
				))
		
		self.dir=os.path.dirname(dir)		
		
		if os.path.exists(dir):
			file=open(dir,'r')
			data=[]
			try:				
				line =file.readline()
				temp=str(line.split("[")[1].split("]")[0])
				ints=[int(i) for i in temp.split(',')]
				if ints[0]!='':
					data=ints
			except:
				pass
			self.fill(data)
			file.close()
		
		
		