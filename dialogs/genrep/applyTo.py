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

from PyQt4 import QtCore  
from PyQt4 import QtGui 
from ui.genrep import uiApplyTo

class classApplyTo(uiApplyTo.classUiApplyTo):
	"""Ventana para seleccionar fuente"""
	def __init__(self,parameters,parent=None):
		self.form1 =QtGui.QMainWindow(parent)
		self.setupUi(self.form1)
		
		self.fill()
		self.form1.show()
		
		self.pushButton.setShortcut("Escape")
		self.pushButton.clicked.connect(self.form1.close)
		self.pushButton_2.setShortcut("Enter")
		

		self.criterions=[
			'Sample ID',
			"Process Order", 
			"Data Type",
		]
		
		self.criterions+=parameters
		
		self.levels=0
		self.selecteds=[-1,-1,-1,-1]
		
		self.comboBox.currentIndexChanged.connect(self.cbox1)
		self.comboBox_2.currentIndexChanged.connect(self.cbox2)
		self.comboBox_3.currentIndexChanged.connect(self.cbox3)
		self.comboBox_4.currentIndexChanged.connect(self.cbox4)
		
		self.fill_select()
		
	def fill(self):
		pass
		
	def fill_data(self):
		filters=[]
		if self.comboBox.currentIndex() >0 :
			filters.append([str(self.comboBox.currentText()),str(self.comboBox_5.currentText()),str(self.lineEdit.text())])
			if self.comboBox_2.currentIndex() >0  and not(self.comboBox_2.currentIndex() in self.selecteds[:1]):
				filters.append([str(self.comboBox_2.currentText()),str(self.comboBox_6.currentText()),str(self.lineEdit_2.text())])
				if self.comboBox_3.currentIndex() >0 and not(self.comboBox_3.currentIndex() in self.selecteds[:2]) :
					filters.append([str(self.comboBox_3.currentText()),str(self.comboBox_7.currentText()),str(self.lineEdit_3.text())])
					if self.comboBox_4.currentIndex() >0 and not(self.comboBox_4.currentIndex() in self.selecteds[:3]) :
						filters.append([str(self.comboBox_4.currentText()),str(self.comboBox_8.currentText()),str(self.lineEdit_4.text())])
		return filters
		
	def fill_select(self):
		for c in self.criterions:
			if not self.criterions.index(c) in self.selecteds:
				self.comboBox.addItem(c)
				self.comboBox_2.addItem(c)
				self.comboBox_3.addItem(c)
				self.comboBox_4.addItem(c)
		
	def cbox1(self):
		if self.comboBox.currentIndex() >0:
			self.comboBox_5.setEnabled(True)
			self.lineEdit.setEnabled(True)
			if self.levels==0:
				self.selecteds[0]=self.comboBox.currentIndex()
				self.setLevel(1)
		else:
			self.comboBox_5.setEnabled(False)
			self.lineEdit.setEnabled(False)
			self.selecteds[0]=-1
			self.setLevel(0)
			
	def cbox2(self):
		if self.comboBox_2.currentIndex() >0:
			self.comboBox_6.setEnabled(True)
			self.lineEdit_2.setEnabled(True)
			if self.levels==1:
				self.selecteds[1]=self.comboBox_2.currentIndex()
				self.setLevel(2)
		else:
			self.comboBox_6.setEnabled(False)
			self.lineEdit_2.setEnabled(False)
			self.selecteds[1]=-1
			self.setLevel(1)
			
	def cbox3(self):
		if self.comboBox_3.currentIndex() >0:
			self.comboBox_7.setEnabled(True)
			self.lineEdit_3.setEnabled(True)
			if self.levels==2:
				self.selecteds[2]=self.comboBox_3.currentIndex()
				self.setLevel(3)
		else:
			self.comboBox_7.setEnabled(False)
			self.lineEdit_3.setEnabled(False)
			self.selecteds[2]=-1
			self.setLevel(2)
			
	def cbox4(self):
		if self.comboBox_4.currentIndex() >0:
			self.comboBox_8.setEnabled(True)
			self.lineEdit_4.setEnabled(True)
			if self.levels==3:
				self.selecteds[3]=self.comboBox_4.currentIndex()
				self.setLevel(4)
		else:
			self.comboBox_8.setEnabled(False)
			self.lineEdit_4.setEnabled(False)
			self.selecteds[3]=-1
			self.setLevel(3)
			
	def setLevel(self,level):
		self.levels=level
		if level==1 and self.comboBox_2.currentIndex() >0:
			self.setLevel(2)
		elif level==2 and self.comboBox_3.currentIndex() >0:
			self.setLevel(3)
		elif level==3 and self.comboBox_4.currentIndex() >0:
			self.setLevel(4)


	
