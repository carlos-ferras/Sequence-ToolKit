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

import sys
from UI.process import ESL
from Dialogs.process import infoWin
from PyQt4 import QtGui
from PyQt4 import QtCore
from functools import partial

class eslWin(ESL.Ui_Dialog):
	def __init__(self,parent,campos):
		self.form1 =QtGui.QMainWindow()
		self.setupUi(self.form1)		
		self.form1.show()		
		
		self.id=6
		self.date_type=''
		self.comments=''
		self.timePerCanel=0
		
		if campos:
			self.rellenar(campos)
		
		self.pushButton_3.clicked.connect(self.info)
		self.pushButton_2.clicked.connect(self.form1.close)		
		self.spinBox.valueChanged.connect(self.actTimePerChannel)
		self.doubleSpinBox_6.valueChanged.connect(self.actTimePerChannel)
		self.comboBox_2.currentIndexChanged.connect(self.actTimePerChannel)
	
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
		
	def actTimePerChannel(self):
		try:
			self.timePerCanel=self.doubleSpinBox_6.value()/self.spinBox.value()			
		except:
			pass
		unidad=str(self.comboBox_2.currentText())
		self.label_6.setText(str(round(self.timePerCanel,2))+' '+unidad)
	
	def rellenar(self,campos):
		self.doubleSpinBox_4.setValue(campos["excV"])
		self.doubleSpinBox_5.setValue(campos["excF"])
		self.doubleSpinBox_6.setValue(self.setTime(campos["time"],campos["time_unid"]))		
		if campos["time_unid"]=='ms':
			unit=0
		elif campos["time_unid"]=='s':
			unit=1
		else:
			unit=2		
		self.comboBox_2.setCurrentIndex(unit)
		self.doubleSpinBox.setValue(campos["heating_rate"])
		self.doubleSpinBox_3.setValue(campos["stabilization"])
		self.doubleSpinBox_2.setValue(campos["final_temp"])
		self.checkBox.setChecked(campos["record_ruring"])
		self.spinBox.setValue(campos["datapoints2"])
		self.checkBox_2.setChecked(campos["light_co_simult"])
		if campos["light_source"]=='Blue':
			light=0
		elif campos["light_source"]=='IR':
			light=1
		else:
			light=2
		self.comboBox.setCurrentIndex(light)	
		self.spinBox_5.setValue(campos["start_optical_power"])	
		self.date_type=campos["date_type"]
		self.comments=campos["comments"]
		self.timePerCanel=campos["timePerCanel"]
		
		self.actTimePerChannel()
		
	def setTime(self,time,unidad):
		if unidad=='ms':
			return float(time)/0.001
		elif unidad=='s':
			return float(time)
		elif unidad=='us':
			return float(time)/0.000001	
	
	def getTime(self):
		time=self.doubleSpinBox_6.value()
		if self.comboBox_2.currentIndex ()==0:
			time*=0.001
		elif self.comboBox_2.currentIndex ()==1:
			pass
		elif self.comboBox_2.currentIndex ()==2:
			time=self.toString(time*0.000001)
		return time
		
	def toString(self,f):
		if int(f)<1:
			s=str(f+1)
			temp=s.split('.')
			temp[0]='0'
			s=temp[0]+'.'+temp[1]
		else:
			s=str(f)
		return s
	
	def data(self):
		all={
			"id":self.id,
			"excV":self.doubleSpinBox_4.value(),
			"excF":self.doubleSpinBox_5.value(),
			"time":self.getTime(),
			"time_unid":str(self.comboBox_2.currentText()),
			"heating_rate":self.doubleSpinBox.value(),
			"stabilization":self.doubleSpinBox_3.value(),
			"final_temp":self.doubleSpinBox_2.value(),
			"time_final_temp":self.toString(float(self.getTime())+self.doubleSpinBox_3.value()),
			"record_ruring":self.checkBox.checkState(),	
			"datapoints2":self.spinBox.value(),	
			"light_co_simult":self.checkBox_2.checkState(),
			"light_source":str(self.comboBox.currentText()), 
			"start_optical_power":self.spinBox_5.value(),		
			"date_type":self.date_type,
			"comments":self.comments,
			"timePerCanel":self.timePerCanel
		}
		
		return "ESL,  "+str(self.doubleSpinBox_5.value())+"KHz, "+str(self.doubleSpinBox_4.value())+"V",all
		
		