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

import sys
from UI.process import Ilumination
from Dialogs.process import infoWin
from PyQt4 import QtGui
from PyQt4 import QtCore
from functools import partial

class ilumWin(Ilumination.Ui_Dialog):
	def __init__(self,parent,campos):
		self.form1 =QtGui.QMainWindow()
		self.setupUi(self.form1)		
		self.form1.show()
				
		self.id=8
		self.date_type=''
		self.comments=''
		
		if campos:
			self.rellenar(campos)
		
		self.pushButton_3.clicked.connect(self.info)
		self.pushButton_2.clicked.connect(self.form1.close)
		
		self.pushButton.setShortcut("Enter")
		self.pushButton_2.setShortcut("Escape")
		
	def info(self):
		self.infoWin=infoWin.infoWin(self.date_type,self.comments)
		self.infoWin.pushButton.clicked.connect(self.extra)
		
	def extra(self):
		self.date_type=self.infoWin.lineEdit.text()
		self.comments=self.infoWin.lineEdit_2.text()
		self.infoWin.form1.close()
		
	def close(self):
		try:
			self.infoWin.form1.close()
		except:
			pass
		self.form1.close()
		
	def rellenar(self,campos):
		self.doubleSpinBox_4.setValue(campos["time"])
		self.doubleSpinBox_3.setValue(campos["stabilization"])
		self.doubleSpinBox_2.setValue(campos["final_temp"])
		self.spinBox_5.setValue(campos["start_optical_power"])
		self.doubleSpinBox.setValue(campos["heating_rate"])
		if campos["light_source"]=='Blue':
			light=0
		elif campos["light_source"]=='IR':
			light=1
		else:
			light=2
		self.comboBox.setCurrentIndex(light)
		self.date_type=campos["date_type"]
		self.comments=campos["comments"]
		
	def data(self):
		all={
			"id":self.id,
			"time":self.doubleSpinBox_4.value(),	
			"stabilization":self.doubleSpinBox_3.value(),	
			"final_temp":self.doubleSpinBox_2.value(),
			"time_final_temp":self.doubleSpinBox_4.value()+self.doubleSpinBox_3.value(),
			"start_optical_power":self.spinBox_5.value(),		
			"heating_rate":self.doubleSpinBox.value(),	
			"light_source":str(self.comboBox.currentText()),	
			"date_type":self.date_type,
			"comments":self.comments
		}
		
		return "Ilumination,  "+str(self.comboBox.currentText())+", "+str(self.spinBox_5.value())+"%",all
