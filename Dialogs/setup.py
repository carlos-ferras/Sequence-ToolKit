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
from UI import setup

class Setup(setup.Ui_Form):
	"""Ventana para seleccionar fuente"""
	def __init__(self,curve_to_show,show_tl,h_scale,h_min,h_max,h_great_unit,h_small_unit,unit,v_scale,v_min,v_max,v_great_unit,v_small_unit,signal,background,s_low,s_high,b_low,b_high,parent=None):
		self.form1 =QtGui.QMainWindow(parent)
		self.setupUi(self.form1)
		
		self.fill(curve_to_show,show_tl,h_scale,h_min,h_max,h_great_unit,h_small_unit,unit,v_scale,v_min,v_max,v_great_unit,v_small_unit,signal,background,s_low,s_high,b_low,b_high)
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
		
		self.doublesb_12.valueChanged.connect(self.hback_change)
		self.doublesb_11.valueChanged.connect(self.lback_change)
		
		self.doublesb_10.valueChanged.connect(self.hsig_change)
		self.doublesb_9.valueChanged.connect(self.lsig_change)
		
	def hsig_change(self):
		if self.doublesb_10.value()<self.doublesb_9.value():
			self.doublesb_10.setValue(self.doublesb_10.value()+1)
	
	def lsig_change(self):
		if self.doublesb_10.value()<self.doublesb_9.value():
			self.doublesb_9.setValue(self.doublesb_9.value()-1)	
	
	def hback_change(self):
		if self.doublesb_12.value()<self.doublesb_11.value():
			self.doublesb_12.setValue(self.doublesb_12.value()+1)
	
	def lback_change(self):
		if self.doublesb_12.value()<self.doublesb_11.value():
			self.doublesb_11.setValue(self.doublesb_11.value()-1)
	
	def fill(self,curve_to_show,show_tl,h_scale,h_min,h_max,h_great_unit,h_small_unit,unit,v_scale,v_min,v_max,v_great_unit,v_small_unit,signal,background,s_low,s_high,b_low,b_high):
		if  1 in curve_to_show:
			self.checkbox.setChecked(True)
		if 2 in curve_to_show:
			self.checkbox_1.setChecked(True)
		if 3 in curve_to_show:
			self.checkbox_2.setChecked(True)
			
			
		if show_tl==0:
			self.radiobutton_3.setChecked(True)
		elif show_tl==1:
			self.radiobutton_4.setChecked(True)
			
			
		if h_scale=='linear':
			self.radiobutton_5.setChecked(True)
		elif h_scale=='log':
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
			
		self.combobox.setCurrentIndex(unit)
			
		if v_scale=='log':
			self.radiobutton_17.setChecked(True)
		elif v_scale=='ln':
			self.radiobutton_18.setChecked(True)
		else:
			self.radiobutton_16.setChecked(True)
		
			
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
			
		self.checkbox_3.setChecked(signal)
		self.checkbox_4.setChecked(background)
		self.doublesb_9.setValue(s_low)
		self.doublesb_10.setValue(s_high)
		self.doublesb_11.setValue(b_low)
		self.doublesb_12.setValue(b_high)

		
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
		curve_to_show=[]
		if self.checkbox.isChecked():		
			curve_to_show.append(1)
		if self.checkbox_1.isChecked():		
			curve_to_show.append(2)
		if self.checkbox_2.isChecked():		
			curve_to_show.append(3)
			
	
		if self.radiobutton_3.isChecked():		
			show_tl=0
		elif self.radiobutton_4.isChecked():		
			show_tl=1
			

		if self.radiobutton_5.isChecked():		
			h_scale='linear'
		elif self.radiobutton_6.isChecked():		
			h_scale='log'
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
		
		unit=self.combobox.currentIndex()
				
		if self.radiobutton_18.isChecked():		
			v_scale='ln'		
		elif self.radiobutton_17.isChecked():		
			v_scale='log'
		else:	
			v_scale='linear'
			
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
			
			
		signal=int(self.checkbox_3.isChecked())
		background=int(self.checkbox_4.isChecked())
		s_low=self.doublesb_9.value()
		s_high=self.doublesb_10.value()
		b_low=self.doublesb_11.value()
		b_high=self.doublesb_12.value()
			
			
		return [curve_to_show,show_tl,h_scale,h_min,h_max,h_great_unit,h_small_unit,unit,v_scale,v_min,v_max,v_great_unit,v_small_unit,signal,background,s_low,s_high,b_low,b_high]
			
			
			
			
			

	
