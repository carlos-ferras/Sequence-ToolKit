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

import sys
from ui.gensec.process  import uiIrradiation
import infoWin
from PyQt4 import QtGui
from PyQt4 import QtCore

class classIrradiation(uiIrradiation.classUiProcess):
	def __init__(self,parent,source,campos,doserate,doserateE):
		self.form1 =QtGui.QMainWindow()
		self.setupUi(self.form1)		
		self.form1.show()		
		
		self.id=1
		self.date_type=''
		self.comments=''
		self.doserate=doserate
		self.doserateE=doserateE
		self.calc=doserate
		
		if campos:
			self.rellenar(campos)
		
		if source:
			self.comboBox.setCurrentIndex(1)
			self.sourceChange()
		
		self.comboBox.currentIndexChanged.connect(self.sourceChange)
		self.pushButton_3.clicked.connect(self.info)
		self.pushButton_2.clicked.connect(self.form1.close)
		
		self.doubleSpinBox_4.valueChanged.connect(self.dose)
		
		self.pushButton.setShortcut("Enter")
		self.pushButton_2.setShortcut("Escape")
		
	def dose(self):
		self.label_6.setText(str(self.doubleSpinBox_4.value()*self.calc))
		
	def info(self):
		self.infoWin=infoWin.classInformation(self.date_type,self.comments)
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
		if campos["source"]=='Beta':
			source=0
		else:
			source=1
		self.comboBox.setCurrentIndex(source)
		self.doubleSpinBox_4.setValue(campos["time"])
		self.doubleSpinBox_2.setValue(campos["final_temp"])
		self.doubleSpinBox_3.setValue(campos["stabilization"])
		self.doubleSpinBox.setValue(campos["heating_rate"])
		self.date_type=campos["date_type"]
		self.comments=campos["comments"]
		self.dose()
		
	def data(self):
		all={
			"id":self.id,
			"source":str(self.comboBox.currentText()), 
			"time":self.doubleSpinBox_4.value(),
			"final_temp":self.doubleSpinBox_2.value(),
			"time_final_temp":self.doubleSpinBox_4.value()+self.doubleSpinBox_3.value(),
			"stabilization":self.doubleSpinBox_3.value(),
			"heating_rate":self.doubleSpinBox.value(),  
			"doserate":self.label_6.text(),
			"date_type":self.date_type,
			"comments":self.comments			
		}
		
		if self.id==1:
			source='Beta Irradiation,  '
			value=str(self.doubleSpinBox_4.value())+" s"
		else:
			dose=float(self.label_6.text())
			source='External Irradiation,  '
			value=str(self.doubleSpinBox_4.value()*dose)+" Gy"
			all[3]=0
			all[4]=0
			all[5]=0
		
		return source+value,all
		
	def setDose(self,text):
		self.label_6.setText(text)
		
	def sourceChange(self):
		if self.comboBox.currentIndex():
			self.id=0
			
			self.doubleSpinBox.setHidden(True)
			self.doubleSpinBox_2.setHidden(True)
			self.doubleSpinBox_3.setHidden(True)
			
			self.label.setHidden(True)
			self.label_2.setHidden(True)
			self.label_3.setHidden(True)
			
			self.line.setHidden(True)
			self.line_2.setHidden(True)
			
			self.frame.setGeometry(QtCore.QRect(6, 10, 400, 105))

			self.form1.resize(502, 125)
			self.form1.setMinimumSize(QtCore.QSize(502, 125))
			self.form1.setMaximumSize(QtCore.QSize(502, 125))
			
			self.calc=self.doserateE
		else:
			self.id=1
			
			self.doubleSpinBox.setHidden(False)
			self.doubleSpinBox_2.setHidden(False)
			self.doubleSpinBox_3.setHidden(False)
			
			self.label.setHidden(False)
			self.label_2.setHidden(False)
			self.label_3.setHidden(False)
			
			self.line.setHidden(False)
			self.line_2.setHidden(False)
			
			self.frame.setGeometry(QtCore.QRect(6, 10, 400, 141))
			
			self.form1.resize(502, 158)
			self.form1.setMinimumSize(QtCore.QSize(502, 158))
			self.form1.setMaximumSize(QtCore.QSize(502, 158))
			
			self.calc=self.doserate
		self.dose()
