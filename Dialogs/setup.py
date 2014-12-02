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
from UI import setup

class Setup(setup.Ui_Form):
	"""Ventana para seleccionar fuente"""
	def __init__(self,curve_to_show,show_tl,h_scale,h_min,h_max,h_great_unit,h_small_unit,v_scale,v_min,v_max,v_great_unit,v_small_unit,parent=None):
		self.form1 =QtGui.QMainWindow(parent)
		self.setupUi(self.form1)
		
		self.fill(curve_to_show,show_tl,h_scale,h_min,h_max,h_great_unit,h_small_unit,v_scale,v_min,v_max,v_great_unit,v_small_unit)
		self.form1.show()
		
		self.pushButton_2.setShortcut("Escape")
		self.pushButton_2.clicked.connect(self.form1.close)
		
		self.pushButton.setShortcut("Enter")
		
		self.radiobutton_12.toggled.connect(self.radio1)
		self.radiobutton_13.toggled.connect(self.radio2)
		self.radiobutton_14.toggled.connect(self.radio3)
		self.radiobutton_15.toggled.connect(self.radio4)
		self.radiobutton_23.toggled.connect(self.radio5)
		self.radiobutton_24.toggled.connect(self.radio6)
		self.radiobutton_25.toggled.connect(self.radio7)
		self.radiobutton_26.toggled.connect(self.radio8)
		
	def fill(self,curve_to_show,show_tl,h_scale,h_min,h_max,h_great_unit,h_small_unit,v_scale,v_min,v_max,v_great_unit,v_small_unit):
		if curve_to_show==1:
			self.radiobutton.setChecked(True)
		elif curve_to_show==2:
			self.radiobutton_1.setChecked(True)
		elif curve_to_show==3:
			self.radiobutton_2.setChecked(True)
			
			
		if show_tl==0:
			self.radiobutton_3.setChecked(True)
		elif show_tl==1:
			self.radiobutton_4.setChecked(True)
			
			
		if h_scale=='lineal':
			self.radiobutton_5.setChecked(True)
		elif h_scale=='log10':
			self.radiobutton_6.setChecked(True)
		elif h_scale=='ln':
			self.radiobutton_7.setChecked(True)
			
		if h_min==-1:
			self.radiobutton_8.setChecked(True)
		elif h_min!=None:
			self.radiobutton_12.setChecked(True)
			self.doublesb_1.setValue(h_min)
			self.doublesb_1.setEnabled(True)
			
		if h_max==-1:
			self.radiobutton_9.setChecked(True)
		elif h_max!=None:
			self.radiobutton_13.setChecked(True)
			self.doublesb_2.setValue(h_max)
			self.doublesb_2.setEnabled(True)
				
		if h_great_unit==-1:
			self.radiobutton_10.setChecked(True)
		elif h_great_unit!=None:
			self.radiobutton_14.setChecked(True)
			self.doublesb_3.setValue(h_great_unit)
			self.doublesb_3.setEnabled(True)
		
		if h_small_unit==-1:
			self.radiobutton_11.setChecked(True)
		elif h_small_unit!=None:
			self.radiobutton_15.setChecked(True)
			self.doublesb_4.setValue(h_small_unit)
			self.doublesb_4.setEnabled(True)
			
		
		if v_scale=='lineal':
			self.radiobutton_16.setChecked(True)
		elif v_scale=='log10':
			self.radiobutton_17.setChecked(True)
		elif v_scale=='ln':
			self.radiobutton_18.setChecked(True)
			
		if v_min==-1:
			self.radiobutton_19.setChecked(True)
		elif v_min!=None:
			self.radiobutton_23.setChecked(True)
			self.doublesb_5.setValue(v_min)
			self.doublesb_5.setEnabled(True)
			
		if v_max==-1:
			self.radiobutton_20.setChecked(True)
		elif v_max!=None:
			self.radiobutton_24.setChecked(True)
			self.doublesb_6.setValue(v_max)
			self.doublesb_6.setEnabled(True)
				
		if v_great_unit==-1:
			self.radiobutton_21.setChecked(True)
		elif v_great_unit!=None:
			self.radiobutton_25.setChecked(True)
			self.doublesb_7.setValue(v_great_unit)
			self.doublesb_7.setEnabled(True)
		
		if v_small_unit==-1:
			self.radiobutton_22.setChecked(True)
		elif v_small_unit!=None:
			self.radiobutton_26.setChecked(True)
			self.doublesb_8.setValue(v_small_unit)
			self.doublesb_8.setEnabled(True)

		
	def radio1(self):
		if self.radiobutton_12.isChecked():
			self.doublesb_1.setEnabled(True)
		else:
			self.doublesb_1.setEnabled(False)
			
	def radio2(self):
		if self.radiobutton_13.isChecked():
			self.doublesb_2.setEnabled(True)
		else:
			self.doublesb_2.setEnabled(False)
			
	def radio3(self):
		if self.radiobutton_14.isChecked():
			self.doublesb_3.setEnabled(True)
		else:
			self.doublesb_3.setEnabled(False)
			
	def radio4(self):
		if self.radiobutton_15.isChecked():
			self.doublesb_4.setEnabled(True)
		else:
			self.doublesb_4.setEnabled(False)
			
	def radio5(self):
		if self.radiobutton_23.isChecked():
			self.doublesb_5.setEnabled(True)
		else:
			self.doublesb_5.setEnabled(False)
			
	def radio6(self):
		if self.radiobutton_24.isChecked():
			self.doublesb_6.setEnabled(True)
		else:
			self.doublesb_6.setEnabled(False)
			
	def radio7(self):
		if self.radiobutton_25.isChecked():
			self.doublesb_7.setEnabled(True)
		else:
			self.doublesb_7.setEnabled(False)
			
	def radio8(self):
		if self.radiobutton_26.isChecked():
			self.doublesb_8.setEnabled(True)
		else:
			self.doublesb_8.setEnabled(False)
		
	def fill_data(self):
		if self.radiobutton.isChecked():		
			curve_to_show=1
		elif self.radiobutton_1.isChecked():		
			curve_to_show=2
		elif self.radiobutton_2.isChecked():		
			curve_to_show=3
			
	
		if self.radiobutton_3.isChecked():		
			show_tl=0
		elif self.radiobutton_4.isChecked():		
			show_tl=1
			

		if self.radiobutton_5.isChecked():		
			h_scale='lineal'
		elif self.radiobutton_6.isChecked():		
			h_scale='log10'
		elif self.radiobutton_7.isChecked():		
			h_scale='ln'
			
		if self.radiobutton_8.isChecked():		
			h_min=-1
		elif self.radiobutton_12.isChecked():		
			h_min=self.doublesb_1.value()
			
		if self.radiobutton_9.isChecked():		
			h_max=-1
		elif self.radiobutton_13.isChecked():		
			h_max=self.doublesb_2.value()
			
		if self.radiobutton_10.isChecked():		
			h_great_unit=-1
		elif self.radiobutton_14.isChecked():		
			h_great_unit=self.doublesb_3.value()
			
		if self.radiobutton_11.isChecked():		
			h_small_unit=-1
		elif self.radiobutton_15.isChecked():		
			h_small_unit=self.doublesb_4.value()
			
		
		if self.radiobutton_16.isChecked():		
			v_scale='lineal'
		elif self.radiobutton_17.isChecked():		
			v_scale='log10'
		elif self.radiobutton_18.isChecked():		
			v_scale='ln'
			
		if self.radiobutton_19.isChecked():		
			v_min=-1
		elif self.radiobutton_23.isChecked():		
			v_min=self.doublesb_5.value()
			
		if self.radiobutton_20.isChecked():		
			v_max=-1
		elif self.radiobutton_24.isChecked():		
			v_max=self.doublesb_6.value()
			
		if self.radiobutton_21.isChecked():		
			v_great_unit=-1
		elif self.radiobutton_25.isChecked():		
			v_great_unit=self.doublesb_7.value()
			
		if self.radiobutton_22.isChecked():		
			v_small_unit=-1
		elif self.radiobutton_26.isChecked():		
			v_small_unit=self.doublesb_8.value()
			
			
		return [curve_to_show,show_tl,h_scale,h_min,h_max,h_great_unit,h_small_unit,v_scale,v_min,v_max,v_great_unit,v_small_unit]	
			
			
			
			
			

	
