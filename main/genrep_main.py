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


import os
import re
from Lienzo import *

import threading
from gensec_base import *
import time
import datetime

from Dialogs.operationsWid import operationsWid 
from Dialogs.fontSelect import fontS
from Dialogs.setup import Setup
from Dialogs.profile import Profile 
from Dialogs.priview import priview
from Dialogs.association import Association
from Dialogs.apply_to import Apply_To
from Dialogs.process import eslWin,irraWin,ilumWin,lmosWin,oslWin,pauseWin,poslWin,pre_heatWin, tlWin
from GenSecLib import createXML,loadXML
import math

class UI_GenRep(UI_GenSec_Base):	
	def __init__(self,dir=False,parent=None):		
		self.config=config()
		self.genrep_config=self.config.loadGenRep()
		if self.genrep_config:
			self.curve_to_show=self.genrep_config[0]
			self.show_tl=self.genrep_config[1]
			self.h_scale=self.genrep_config[2]
			self.h_min=self.genrep_config[3]
			self.h_max=self.genrep_config[4]
			self.h_great_unit=self.genrep_config[5]
			self.h_small_unit=self.genrep_config[6]
			self.unit=self.genrep_config[7]
			self.v_scale=self.genrep_config[8]
			self.v_min=self.genrep_config[9]
			self.v_max=self.genrep_config[10]
			self.v_great_unit=self.genrep_config[11]
			self.v_small_unit=self.genrep_config[12]
			self.signal=self.genrep_config[13]
			self.background=self.genrep_config[14]
			self.s_low=self.genrep_config[15]
			self.s_high=self.genrep_config[16]
			self.b_low=self.genrep_config[17]
			self.b_high=self.genrep_config[18]
			self.parameters=self.genrep_config[19]
		else:
			self.curve_to_show=[1]
			self.show_tl=0
			self.h_scale='lineal'
			self.h_min=-1
			self.h_max=-1
			self.h_great_unit=-1
			self.h_small_unit=-1
			self.unit=0
			self.v_scale='lineal'
			self.v_min=-1
			self.v_max=-1
			self.v_great_unit=-1
			self.v_small_unit=-1
			self.signal=True
			self.background=True
			self.s_low=0
			self.s_high=0
			self.b_low=0
			self.b_high=0
			self.parameters=[]
			
		self.enum_parameters=(
			"Beta Irradiation Time", 
			"Beta Dose",
			"External Irradiation Time", 
			"External Dose", 
			"Preheating Temperature",
			"Measuring Temperature",
			"Preheating Rate",
			"Heating Rate",
			"Light Source",
			"Optical Power",
			"Electric Stimulation",
			"Electric Frequency",
			"Time of Beta irradiation",
			"Time of External irradiation",
			"Time of Measurement",
		)
		
		UI_GenSec_Base.__init__(self,'GenRep','pixmaps/genrep.png',dir)
				
		self.treeWidget.itemSelectionChanged.connect(self.groupActive)
		self.header=self.treeWidget.header()			
		self.header.setClickable(True)
		self.header.setStyleSheet(HEADER)		
		self.form1.resizeEvent = self.onResize
		self.actionAcerda_de.triggered.connect(partial(about,self.form1,'GenRep',QtGui.QApplication.translate("MainWindow", 'Report Generator', None, QtGui.QApplication.UnicodeUTF8),QtGui.QApplication.translate("MainWindow", 'Description', None, QtGui.QApplication.UnicodeUTF8),'1.0.0',"pixmaps/genrep.png"))
		self.action_setup.triggered.connect(self.data_setup)
		self.action_profile.triggered.connect(self.data_profile)
		self.action_group.triggered.connect(self.group)
		self.action_ungroup.triggered.connect(self.ungroup)
		self.action_ungroup_all.triggered.connect(self.ungroupall)
		self.action_association.triggered.connect(self.associationCriteria)			

		self.treeWidget_2.itemClicked.connect(self.change_graphic)
		
		self.form1.statusBar().showMessage(QtGui.QApplication.translate('MainWindow',"Ready"),2000)
		self.form1.setCursor(QtCore.Qt.ArrowCursor)
		self.treeWidget.customContextMenuRequested.connect(self.popup)
		
		X=[]
		Y=[]
		self.create_graphic(X,Y)
		self.groupsColors={}
	
	def change_graphic(self,item):
		headerName= str(item.text(0))
		if headerName in ['1','2','3']:
			parent=item.parent().text(0)			
			item = self.treeWidget.topLevelItem(self.selected_row[0])
			for column in range(self.comandos+1)[2:]:				
				if self.header.model().headerData(column,QtCore.Qt.Horizontal).toString()==parent:					
					info=self.processData[str(self.selected_row[0])+','+str(column)]					
					sum=int(info['datapoints1']+info['datapoints2']+info['datapoints3'])
					Y=[float(i) for i in info['Curva'+headerName].split(';')[:sum]]
					if info['id']==2 and self.show_tl:
						X=[float(i) for i in info['Curva3'].split(';')[:sum]]
					else:
						X=range(sum)
					if self.unit:
						X=[ (i*info['timePerCanel']) for i in X]
					
					self.create_graphic(X,Y)
		
			
	def Apply_To(self):
		send=[]
		for i in self.parameters:
			send.append(self.enum_parameters	[i])
		self.apply_to_win=Apply_To(send,self.form1)
		self.apply_to_win.pushButton_2.clicked.connect(self.Apply_To_ready)
		
		
	def Apply_To_ready(self):
		self.criterias_to=self.apply_to_win.fill_data()
		print self.criterias_to
		self.apply_to_win.form1.close()
	
	
	def associationCriteria(self):
		send=[]
		for i in self.parameters:
			send.append(self.enum_parameters	[i])
		self.association=Association(send,self.form1)
		self.association.pushButton_2.clicked.connect(self.association_ready)	
		
	def association_ready(self):
		self.criterias=self.association.fill_data()
		print self.criterias
		self.association.form1.close()
	
	
	def  data_setup(self):
		self.setup=Setup(self.curve_to_show,self.show_tl,self.h_scale,self.h_min,self.h_max,self.h_great_unit,self.h_small_unit,self.unit,self.v_scale,self.v_min,self.v_max,self.v_great_unit,self.v_small_unit,self.signal,self.background,self.s_low,self.s_high,self.b_low,self.b_high,self.form1)
		self.setup.pushButton.clicked.connect(self.setup_ready)		
	

	def  data_profile(self):
		self.profile=Profile(self.parameters,self.form1)
		self.profile.pushButton_2.clicked.connect(self.profile_ready)		

	def profile_ready(self):
		self.parameters=self.profile.fill_data()
		self.profile.form1.close()		
		
		
	def setup_ready(self):
		setup_data=self.setup.fill_data()
		self.setup.form1.close()
		
		self.curve_to_show=setup_data[0]
		self.show_tl=setup_data[1]
		self.h_scale=setup_data[2]
		self.h_min=setup_data[3]
		self.h_max=setup_data[4]
		self.h_great_unit=setup_data[5]
		self.h_small_unit=setup_data[6]
		self.unit=setup_data[7]
		self.v_scale=setup_data[8]
		self.v_min=setup_data[9]
		self.v_max=setup_data[10]
		self.v_great_unit=setup_data[11]
		self.v_small_unit=setup_data[12]
		self.signal=setup_data[13]
		self.background=setup_data[14]
		self.s_low=setup_data[15]
		self.s_high=setup_data[16]
		self.b_low=setup_data[17]
		self.b_high=setup_data[18]
		
		self.clear_lateral_panel()
		self.fill_lateral_panel()
		self.create_graphic(self.canvas.allGraphic_X,self.canvas.allGraphic_Y)
					
	def afterOpen(self):
		self.create_graphic([],[])
		self.clear_lateral_panel()
		
		if self.selected_row[1]:
			self.selected_row[1].setStyleSheet(HEADER_TOOLBUTTON_STYLE)
		self.selected_row=[False,False]
		self.colores_in_row={}
		for group in self.inGroup:		
			self.colorearGrupo([group[0]],False,[])
		self.inGroup=[]
		
		
	@cursorAction()
	def create_graphic(self,X,Y):
		self.pan=False
		self.zoom=False
		
		w=int(self.W/64)
		sl=self.s_low
		sh=self.s_high
		bl=self.b_low
		bh=self.b_high
		self.canvas = Lienzo(X,Y,w,sl,sh,bl,bh,self.signal,self.background,self.verticalLayoutWidget)
		
								
		def onClick(event):
			if event.button==1 and (not self.pan) and (not self.zoom):
				try:
					if event.inaxes.get_title()=='Signal(SG)' and not self.canvas.activeBackground:						
						if not self.canvas.activeSignal:
							self.form1.statusBar().showMessage(QtGui.QApplication.translate('MainWindow',"Signal area is selected"),3000)
							event.inaxes.patch.set_facecolor('#6C9DEC')
							event.canvas.draw()
							self.canvas.activeSignal=True
						else:
							event.inaxes.patch.set_facecolor('#ffffff')
							event.canvas.draw()
							self.canvas.activeSignal=False
					elif event.inaxes.get_title()=='Background(BG)' and not self.canvas.activeSignal:
						if not self.canvas.activeBackground:
							self.form1.statusBar().showMessage(QtGui.QApplication.translate('MainWindow',"Background area is selected"),3000)
							event.inaxes.patch.set_facecolor('#6C9DEC')
							event.canvas.draw()
							self.canvas.activeBackground=True
						else:
							event.inaxes.patch.set_facecolor('#ffffff')
							event.canvas.draw()
							self.canvas.activeBackground=False					
				except:
					pass
				
		def enter_axes(event):
			if event.inaxes.get_title()=='Signal' or event.inaxes.get_title()=='Background' :
				self.form1.statusBar().showMessage(QtGui.QApplication.translate('MainWindow',"Slect area to change"))
				self.form1.setCursor(QtCore.Qt.PointingHandCursor)
				
		def leave_axes(event):
			if event.inaxes.get_title()=='Signal' or event.inaxes.get_title()=='Background' :
				self.form1.statusBar().showMessage(' ')
				self.form1.setCursor(QtCore.Qt.ArrowCursor)
		
		ToolBarr = NavigationToolbar(self.canvas, self.verticalLayoutWidget)
		self.verticalLayoutWidget.setStyleSheet(TOOLBUTTON_STYLE)
		
		def pan_change(event):
			if self.pan:
				self.pan=False
			else:
				self.pan=True
				self.zoom=False
				
		def zoom_change(event):
			if self.zoom:
				self.zoom=False
			else:
				self.zoom=True
				self.pan=False
				
		def home_press(event):
			self.canvas.activeSignal=True
			self.canvas.activeBackground=False
			if self.signal and self.canvas.allGraphic_X!=[]:
				try:
					self.canvas.onselect(min(self.canvas.Signal_X),max(self.canvas.Signal_X))
				except:
					self.canvas.onselect(self.canvas.Signal_X,self.canvas.Signal_X)
			self.canvas.activeBackground=True
			if self.background and self.canvas.allGraphic_X!=[]:
				try:
					self.canvas.onselect(min(self.canvas.Background_X),max(self.canvas.Background_X))
				except:
					self.canvas.onselect(self.canvas.Background_X,self.canvas.Background_X)
				
		
		ToolBarr.setOrientation(QtCore.Qt.Vertical)
		ToolBarr.setMaximumWidth (40)
		
		for act in ToolBarr.actions():
			toolTip=str(act.toolTip())
			if toolTip=='Configure subplots' or toolTip=='Edit curves line and axes parameters':
				ToolBarr.removeAction(act)
			elif toolTip=='Reset original view':
				act.triggered.connect(home_press)
				act.setToolTip(QtGui.QApplication.translate("MainWindow", 'Home'))
				act.setStatusTip(QtGui.QApplication.translate("MainWindow", 'Reset Original View'))
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap("pixmaps/icons/home.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				act.setIcon(icon)				
			elif toolTip=='Back to previous view' or toolTip=='Back to  previous view':
				act.setToolTip(QtGui.QApplication.translate("MainWindow", 'Back'))
				act.setStatusTip(QtGui.QApplication.translate("MainWindow", 'Back to previous view'))
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap("pixmaps/icons/back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				act.setIcon(icon)
			elif toolTip=='Forward to next view':
				act.setToolTip(QtGui.QApplication.translate("MainWindow", 'Forward'))
				act.setStatusTip(QtGui.QApplication.translate("MainWindow", 'Forward to next view'))
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap("pixmaps/icons/next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				act.setIcon(icon)
			elif toolTip=='Pan axes with left mouse, zoom with right':
				act.triggered.connect(pan_change)
				act.setToolTip(QtGui.QApplication.translate("MainWindow", 'Drag'))
				act.setStatusTip(QtGui.QApplication.translate("MainWindow", 'Drag with left mouse, zoom with right'))
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap("pixmaps/icons/transform.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				#act.setIcon(icon)
			elif toolTip=='Zoom to rectangle':
				act.triggered.connect(zoom_change)
				act.setToolTip(QtGui.QApplication.translate("MainWindow", 'Zoom'))
				act.setStatusTip(QtGui.QApplication.translate("MainWindow", 'Zoom the rectangle'))
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap("pixmaps/icons/zoom.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				act.setIcon(icon)
			elif toolTip=='Save the figure':
				act.setToolTip(QtGui.QApplication.translate("MainWindow", 'Save'))
				act.setStatusTip(QtGui.QApplication.translate("MainWindow", 'Save the figure as image'))		
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap("pixmaps/icons/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				act.setIcon(icon)
		self.canvas.fig.set_facecolor('#f0f0f0')
		ToolBarr.setStyleSheet('background:#f0f0f0;')
		
		xmin1_label=QtGui.QLabel('low')		
		xmin1_label.setStyleSheet('color:green')
		xmin1_sb = QtGui.QDoubleSpinBox()
		xmin1_sb.setStatusTip(QtGui.QApplication.translate("MainWindow", 'Low channel to signal'))	
		
		xmax1_label=QtGui.QLabel('high')
		xmax1_label.setStyleSheet('color:green')
		xmax1_sb = QtGui.QDoubleSpinBox()
		xmax1_sb.setStatusTip(QtGui.QApplication.translate("MainWindow", 'High channel to signal'))
		
		sign_count_label=QtGui.QLabel('signal')
		sign_count_label.setStyleSheet('color:green')
		sign_count_line = QtGui.QLineEdit()
		sign_count_line.setReadOnly (True)
		sign_count_line.setStatusTip(QtGui.QApplication.translate("MainWindow", 'Count of signal area'))
		
		if not self.signal:
			self.sig_widget.setVisible(False)
		else:
			self.sig_widget.setVisible(True)
			
		xmin2_label=QtGui.QLabel('low')
		xmin2_label.setStyleSheet('color:#1A297D')
		xmin2_sb = QtGui.QDoubleSpinBox()
		xmin2_sb.setStatusTip(QtGui.QApplication.translate("MainWindow", 'Low channel to Background'))
		
		xmax2_label=QtGui.QLabel('high')
		xmax2_label.setStyleSheet('color:#1A297D')
		xmax2_sb = QtGui.QDoubleSpinBox()
		xmax2_sb.setStatusTip(QtGui.QApplication.translate("MainWindow", 'High channel to Background'))
		
		back_count_label=QtGui.QLabel('background')
		back_count_label.setStyleSheet('color:#1A297D')
		back_count_line = QtGui.QLineEdit()
		back_count_line.setReadOnly (True)
		back_count_line.setStatusTip(QtGui.QApplication.translate("MainWindow", 'Count of background area'))
		
		if not self.background:
			self.back_widget.setVisible(False)
		else:
			self.back_widget.setVisible(True)
		
		apply_to=QtGui.QPushButton()
		apply_to.setText(QtGui.QApplication.translate("MainWindow", 'Apply this to'))
		apply_to.clicked.connect(self.Apply_To)
		
		apply_all=QtGui.QPushButton()
		apply_all.setText(QtGui.QApplication.translate("MainWindow", 'Apply to all'))
		
		self.verticalLayout.addWidget(ToolBarr,2,0,8,1)
		self.verticalLayout.addWidget(self.canvas,0,0,10,60)		
		
		self.sig_verticalLayout.addWidget(xmin1_label,0,0,1,1)
		self.sig_verticalLayout.addWidget(xmin1_sb,1,0,1,1)		
		self.sig_verticalLayout.addWidget(sign_count_label,0,2,1,2)
		self.sig_verticalLayout.addWidget(sign_count_line,1,2,1,2)		
		self.sig_verticalLayout.addWidget(xmax1_label,0,5,1,1)
		self.sig_verticalLayout.addWidget(xmax1_sb,1,5,1,1)		
		self.verticalLayout.addWidget(self.sig_widget,11,6,2,4)
		
		self.verticalLayout.addWidget(apply_to,12,25,1,1)
		self.verticalLayout.addWidget(apply_all,12,30,1,1)
		
		self.back_verticalLayout.addWidget(xmin2_label,0,0,1,1)
		self.back_verticalLayout.addWidget(xmin2_sb,1,0,1,1)
		self.back_verticalLayout.addWidget(back_count_label,0,2,1,2)
		self.back_verticalLayout.addWidget(back_count_line,1,2,1,2)	
		self.back_verticalLayout.addWidget(xmax2_label,0,5,1,1)
		self.back_verticalLayout.addWidget(xmax2_sb,1,5,1,1)
		self.verticalLayout.addWidget(self.back_widget,11,50,2,4)
		
		def count_signal():
			count=0
			for i in self.canvas.Signal_Y:
				count+=i
			sign_count_line.setText(str(int(count)))
			
		def count_background():
			count=0
			for i in self.canvas.Background_Y:
				count+=i
			back_count_line.setText(str(int(count)))
		
		def fill_x_1(x1,x2):
			xmin1_sb.setValue(x1)
			xmax1_sb.setValue(x2)			
			count_signal()
		
		def fill_x_2(x1,x2):
			xmin2_sb.setValue(x1)
			xmax2_sb.setValue(x2)
			count_background()	
		
		def x1_sb_change(buttom):
			if not self.canvas.activeSignal:				
				if xmax1_sb.value() >=xmin1_sb.value():
					self.canvas.activeSignal=True
					self.canvas.onselect(xmin1_sb.value(),xmax1_sb.value()+1)

			
		def x2_sb_change(buttom):
			if not self.canvas.activeBackground:				
				if xmax2_sb.value() >=xmin2_sb.value():
					self.canvas.activeBackground=True
					self.canvas.onselect(xmin2_sb.value(),xmax2_sb.value()+1)
				
		if self.canvas.allGraphic_X!=[] and self.canvas.allGraphic_Y!=[]:
			self.canvas.mousePressEvent=SpanSelector(
								self.canvas.allGraphic,
								self.canvas.onselect,
								'horizontal',
								useblit=True,
								rectprops=dict(alpha=0.5, facecolor='#c0c0c0') 
								)
			
			self.canvas.mpl_connect('button_press_event', onClick)
			self.canvas.mpl_connect('axes_enter_event', enter_axes)
			self.canvas.mpl_connect('axes_leave_event', leave_axes)
			
			xmin1_sb.setMinimum(min(X))
			xmin1_sb.setMaximum(max(X))
			xmax1_sb.setMinimum(min(X))
			xmax1_sb.setMaximum(max(X))
			xmin2_sb.setMinimum(min(X))
			xmin2_sb.setMaximum(max(X))
			xmax2_sb.setMinimum(min(X))
			xmax2_sb.setMaximum(max(X))
			
			xmin1_sb.valueChanged.connect(partial(x1_sb_change,1))
			xmax1_sb.valueChanged.connect(partial(x1_sb_change,2))
			xmin2_sb.valueChanged.connect(partial(x2_sb_change,1))
			xmax2_sb.valueChanged.connect(partial(x2_sb_change,2))	
			self.canvas.signal_change.connect(fill_x_1)
			self.canvas.background_change.connect(fill_x_2)
			
			if self.signal:
				fill_x_1(self.canvas.Signal_X[0],self.canvas.Signal_X[-1]+1)
			if self.background:
				fill_x_2(self.canvas.Background_X[0],self.canvas.Background_X[-1]+1)
			
	def fillActions(self):
		#Para la grafica
		self.verticalLayoutWidget = QtGui.QWidget()		
		self.verticalLayout = QtGui.QGridLayout(self.verticalLayoutWidget)
		self.verticalLayout.setContentsMargins(5, 0, 0, 0)
		
		self.sig_widget=QtGui.QWidget()		
		self.sig_verticalLayout = QtGui.QGridLayout(self.sig_widget)
		self.sig_verticalLayout.setContentsMargins(0, 0, 0, 0)
		
		self.back_widget=QtGui.QWidget()
		self.back_verticalLayout = QtGui.QGridLayout(self.back_widget)
		self.back_verticalLayout.setContentsMargins(0, 0, 0, 0)		
		
		#isquierda de la grafica
		self.treeWidget_2 = QtGui.QTreeWidget()
		font = QtGui.QFont()
		font.setFamily("Novason")
		font.setPointSize(12)
		font.setBold(False)
		font.setItalic(False)
		font.setUnderline(False)
		font.setWeight(53)
		self.treeWidget_2.setFont(font)
		self.treeWidget_2.setFocusPolicy(QtCore.Qt.ClickFocus)
		self.treeWidget_2.setFrameShape(QtGui.QFrame.StyledPanel)
		self.treeWidget_2.setFrameShadow(QtGui.QFrame.Sunken)
		self.treeWidget_2.setTabKeyNavigation(True)
		self.treeWidget_2.setStyleSheet(TREEW2_STYLE)
		self.treeWidget_2.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		self.treeWidget_2.headerItem().setText(0, QtGui.QApplication.translate('MainWindow',"Columns"))
		self.treeWidget_2.header().setStyleSheet(HEADER)	
		
		self.mainWidget=QtGui.QWidget()
		self.form1.setCentralWidget(self.mainWidget)
		
		#Panel de abajo
		self.down_area= QtGui.QWidget()
		#self.down_area.setStyleSheet('background:red;')
		self.down_area_layout=QtGui.QGridLayout(self.down_area)
		self.active_bar=QtGui.QLabel()
		self.active_bar.mouseDoubleClickEvent=self.chow_hidden_down_area
		self.active_bar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.active_bar.setStatusTip(QtGui.QApplication.translate("MainWindow", 'Show/Hidde graphic'))
		self.active_bar.setStyleSheet('background:qlineargradient( x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #d3d3d3, stop: 0.1 #d3d3d3,stop: 0.49 #ffffff, stop: 0.5 #ffffff, stop: 0.9 #f0f0f0,stop: 1 #f0f0f0)')
		self.down_area_layout.setContentsMargins(0, 0, 0, 0)
		self.down_area_layout.addWidget(self.active_bar,0,0,1,4)
		self.down_area_layout.addWidget(self.verticalLayoutWidget,1,0,10,3)
		self.down_area_layout.addWidget(self.treeWidget_2,1,3,10,1)
		self.down_area_layout.setColumnMinimumWidth(3,120)
		
		self.layout=QtGui.QGridLayout(self.mainWidget)
		self.layout.setRowMinimumHeight(1,150)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.layout.addWidget(self.treeWidget, 1, 0, 1, 3)
		self.layout.addWidget(self.down_area,2,0,1,3)
		self.layout.setRowMinimumHeight(2,390)
		
		self.m_anim = Animation(self.down_area, 'pos')
		self.m_anim.setEasingCurve(QtCore.QEasingCurve.Linear)
		self.m_anim.setDuration(700)
		self.m_anim.setLoopCount(1)
		self.m_anim.finished.connect(self.detenido)
		
		self.down_area_visible=True
		
		self.fill_aux()
		
	def fill_aux(self):
		self.actionEjecutar_GenRep.setVisible(False)
		
		self.actionNuevo.setVisible(False)
		self.actionPegar.setVisible(False)
		self.actionCortar.setVisible(False)
		
		#Seleccionar Fila-----------------------------------------------------------------
		self.menuEditar.addSeparator()
		self.actionSeleccionar_Fila = QtGui.QAction(self.form1)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("pixmaps/icons/select_row.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.actionSeleccionar_Fila.setIconVisibleInMenu(True)
		self.actionSeleccionar_Fila.setIcon(icon)
		self.actionSeleccionar_Fila.setShortcut("Alt+S")
		self.actionSeleccionar_Fila.setStatusTip(QtGui.QApplication.translate("MainWindow", "Select one row of the table", None, QtGui.QApplication.UnicodeUTF8))
		self.menuEditar.addAction(self.actionSeleccionar_Fila)
		self.actionSeleccionar_Fila.setText(QtGui.QApplication.translate("MainWindow", "&Select Row", None, QtGui.QApplication.UnicodeUTF8))
		
		#SetUp-------------------------------------------------------------------
		self.action_setup = QtGui.QAction(self.form1)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("pixmaps/icons/setup.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.action_setup.setIconVisibleInMenu(True)
		self.action_setup.setIcon(icon)
		self.action_setup.setShortcut("Ctrl+T")
		self.action_setup.setStatusTip(QtGui.QApplication.translate("MainWindow", "Defines how they are to be displayed the results", None, QtGui.QApplication.UnicodeUTF8))
		self.action_setup.setText(QtGui.QApplication.translate("MainWindow", "Set&Up", None, QtGui.QApplication.UnicodeUTF8))
		self.menuOpciones.insertAction(self.menuOpciones_de_GenSec.menuAction(),self.action_setup)
		
		#Perfil--------------------------------------------------------------------
		self.action_profile = QtGui.QAction(self.form1)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("pixmaps/icons/profile.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.action_profile.setIconVisibleInMenu(True)
		self.action_profile.setIcon(icon)
		self.action_profile.setShortcut("Ctrl+E")
		self.action_profile.setStatusTip(QtGui.QApplication.translate("MainWindow", "Define the parameters to report", None, QtGui.QApplication.UnicodeUTF8))
		self.action_profile.setText(QtGui.QApplication.translate("MainWindow", "Pro&file", None, QtGui.QApplication.UnicodeUTF8))
		self.menuEditar.insertAction(self.actionSeleccionar_Fila,self.action_profile)
		
		#Asociacion-------------------------------------------------------------------
		self.action_association = QtGui.QAction(self.form1)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("pixmaps/icons/association.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.action_association.setIconVisibleInMenu(True)
		self.action_association.setIcon(icon)
		self.action_association.setShortcut("Ctrl+K")
		self.action_association.setStatusTip(QtGui.QApplication.translate("MainWindow", "Defines how they are to be displayed the results", None, QtGui.QApplication.UnicodeUTF8))
		self.action_association.setText(QtGui.QApplication.translate("MainWindow", "&Association by criteria", None, QtGui.QApplication.UnicodeUTF8))
		self.menuOpciones.insertAction(self.actionEjecutar_GenSec, self.action_association)
		self.menuOpciones.insertSeparator(self.actionEjecutar_GenSec)
		
		#Desagrupar todas-------------------------------------------------------------------
		self.action_ungroup_all = QtGui.QAction(self.form1)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("pixmaps/icons/ungroup_all.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.action_ungroup_all.setIconVisibleInMenu(True)
		self.action_ungroup_all.setIcon(icon)
		self.action_ungroup_all.setShortcut("Ctrl+U")
		self.action_ungroup_all.setStatusTip(QtGui.QApplication.translate("MainWindow", "Ungroup all the associated processes", None, QtGui.QApplication.UnicodeUTF8))
		self.action_ungroup_all.setText(QtGui.QApplication.translate("MainWindow", "&Ungroup All", None, QtGui.QApplication.UnicodeUTF8))
		self.menuOpciones.insertAction(self.action_association, self.action_ungroup_all)
		
		#Agrupar--------------------------------------------------------------------
		self.action_group = QtGui.QAction(self.form1)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("pixmaps/icons/group.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.action_group.setIconVisibleInMenu(True)
		self.action_group.setIcon(icon)
		self.action_group.setStatusTip(QtGui.QApplication.translate("MainWindow", "Define the associated processes to a measurement", None, QtGui.QApplication.UnicodeUTF8))
		self.action_group.setText(QtGui.QApplication.translate("MainWindow", "Group", None, QtGui.QApplication.UnicodeUTF8))
		self.action_group.setEnabled(False)
		
		#Desagrupar--------------------------------------------------------------------
		self.action_ungroup = QtGui.QAction(self.form1)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("pixmaps/icons/ungroup.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.action_ungroup.setIconVisibleInMenu(True)
		self.action_ungroup.setIcon(icon)
		self.action_ungroup.setStatusTip(QtGui.QApplication.translate("MainWindow", "Ungroup the associated processes", None, QtGui.QApplication.UnicodeUTF8))
		self.action_ungroup.setText(QtGui.QApplication.translate("MainWindow", "Ungroup", None, QtGui.QApplication.UnicodeUTF8))
		self.action_ungroup.setEnabled(False)
		
		#Reporte--------------------------------------------------------------------
		self.action_report= QtGui.QAction(self.form1)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("pixmaps/icons/report.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.action_report.setIconVisibleInMenu(True)
		self.action_report.setIcon(icon)
		self.action_report.setStatusTip(QtGui.QApplication.translate("MainWindow", "Make a report", None, QtGui.QApplication.UnicodeUTF8))
		self.action_report.setText(QtGui.QApplication.translate("MainWindow", "Report", None, QtGui.QApplication.UnicodeUTF8))
		
		self.Tools_ToolBar.setVisible(True)
		self.Tools_ToolBar.addAction(self.action_profile)
		self.Tools_ToolBar.addAction(self.action_setup)
		self.Tools_ToolBar.addAction(self.action_group)
		self.Tools_ToolBar.addAction(self.action_ungroup)
		self.Tools_ToolBar.addAction(self.action_report)
	
	
	def getGroupColor(self,row):
		try:
			existen=self.colores_in_row[row]
		except:
			existen=[]
			
		colors=(
			QtGui.QColor(255, 188, 0, 50),
			QtGui.QColor(0, 255,218, 50),
			QtGui.QColor(0, 203, 255, 50),
			QtGui.QColor(147, 132, 245, 50),
			QtGui.QColor(245, 132, 181, 50),
		)
		
		for color in colors:
			if not color in existen:
				self.colores_in_row.setdefault(row, []).append (color)
				return color
		
		self.colores_in_row.setdefault(row, []).append (existen[-5])
		return existen[-5]
	
	def colorearGrupo(self,group,colorear,dejar):
		columns=[]
		row=-1		
		color= self.getGroupColor(row)		
		for g in group:
			self.groupsColors[g]=color
			data=g.split(',')
			row=int(data[0])
			columns.append(int(data[1]))		
		delegate = BackgroundColorDelegate(self.treeWidget,columns,colorear,dejar,color) 
		self.treeWidget.setItemDelegateForRow(row,delegate)

	
	def dejar(self,row,toGroup):
		list={}
		item = self.treeWidget.topLevelItem(row)
		for column in range(self.treeWidget.columnCount()):
			if not (str(row)+','+str(column)) in toGroup:
				for group in range(len(self.inGroup)):
					if (str(row)+','+str(column)) in self.inGroup[group]:
						g=str(row)+','+str(column)
						list[column]=self.groupsColors[g]
		return list
		
		
	def deleteinGroup(self,borrar):
		for grupo in borrar:
			try:
				del self.inGroup[grupo]					
			except:
				pass
		self.action_ungroup.setEnabled(False)
	
	
	def group(self):
		toGroup=[]
		borrar=[]
		row=None
		for item in self.treeWidget.selectedIndexes():
			i = self.treeWidget.topLevelItem(item.row())
			if i.text(item.column())=='':
				self.error(QtGui.QApplication.translate('MainWindow','Command ')+str(item.column()-1)+QtGui.QApplication.translate('MainWindow',' is empty'))
				return False
			self.ungroup()
			row=item.row()
			toGroup.append(str(row)+','+str(item.column()))
		
		self.deleteinGroup(borrar)	
		self.inGroup.append(toGroup)
		dejar=self.dejar(row,toGroup)
		self.colorearGrupo(toGroup,True,dejar)
		self.action_ungroup.setEnabled(True)
		
	
	def ungroup(self):
		toUngroup=[]
		borrar=[]
		row=None
		for item in self.treeWidget.selectedIndexes():
			for group in range(len(self.inGroup)):
				if (str(item.row())+','+str(item.column())) in self.inGroup[group]:
					if not group in borrar:
						borrar.insert(0,group)
			row=item.row()
			toUngroup.append(str(item.row())+','+str(item.column()))
		
		self.deleteinGroup(borrar)	
		dejar=self.dejar(row,toUngroup)
		self.colorearGrupo(toUngroup,False,dejar)
		
	
	@seguro(QtGui.QApplication.translate('MainWindow','Are you sure you want to continue, you will lose all associations?'))		
	def ungroupall(self):
		for group in self.inGroup:		
			self.colorearGrupo([group[0]],False,[])
		self.inGroup=[]
		self.colores_in_row={}
		
		
	def groupActive(self):
			"""activa el boton merge cuando es posible usarlo, lo desactiva cuando no"""
			if self.pertenecen_consecutivos():
				self.action_group.setEnabled(True)				
			else:
				self.action_group.setEnabled(False)
			
			self.action_ungroup.setEnabled(False)
			for item in self.treeWidget.selectedIndexes():
				for group in range(len(self.inGroup)):
					for poss in self.inGroup[group]:
						if str(item.row())+','+str(item.column())==poss:
							self.action_ungroup.setEnabled(True)
	
	
	def onResize(self,event):
		if not self.down_area_visible:
			self.m_anim.setStartValue(QtCore.QPointF(0,self.mainWidget.height()))
			self.m_anim.setEndValue(QtCore.QPointF(0, self.mainWidget.height()-20))
			self.m_anim.start()
			
	def detenido(self):
		if self.down_area_visible:
			self.layout.addWidget(self.treeWidget, 1, 0,1, -1)
			self.layout.setContentsMargins(0, 0, 0, 0)
			self.verticalLayoutWidget.setEnabled(True)
	
	def chow_hidden_down_area(self,event):
		self.verticalLayoutWidget.setEnabled(False)
		if self.down_area_visible:
			self.layout.addWidget(self.treeWidget, 1, 0,4, -1)
			self.layout.setContentsMargins(0, 0, 0, 20)
			self.m_anim.setStartValue(QtCore.QPointF(0,self.mainWidget.height()-self.down_area.height()))
			self.m_anim.setEndValue(QtCore.QPointF(0, self.mainWidget.height()-20))
			self.down_area_visible=False
		else:
			self.m_anim.setEndValue(QtCore.QPointF(0, self.mainWidget.height()-self.down_area.height()))
			self.m_anim.setStartValue(QtCore.QPointF(0, self.mainWidget.height()-20))
			self.down_area_visible=True			
		self.m_anim.start()
	
			
	def popup(self,pos):
		menu = QtGui.QMenu()
		menu.addAction(self.actionCopiar)
		if self.action_group.isEnabled():
			menu.addAction(self.action_group)
		if self.action_ungroup.isEnabled():
			menu.addAction(self.action_ungroup)
		action = menu.exec_(self.treeWidget.mapToGlobal(pos))
		
	@cursorAction()
	def save(self,temp=False):
		"""Guarda la informacion en forma de xml"""
		self.closeAllDialogs()
		if self.directorioArchivo=='':
			return self.saveAs()
		else:
			#guardarlo en la dir self.directorioArchivo
			pass
	
	
	@cursorAction()
	def saveAs(self,dir=False):
		"""Ventana para guardar un documanto"""
		self.closeAllDialogs()
		dialog=QtGui.QFileDialog(self.form1)
		if not dir:
			self.directorioArchivo=dialog.getSaveFileName(
				self.form1,
				QtGui.QApplication.translate('MainWindow',"Save"),
				self.fileLocation,
				QtGui.QApplication.translate('MainWindow','File')+' XLS (*.xls);; '+QtGui.QApplication.translate('MainWindow','File')+'RLS (*.rls);; '+QtGui.QApplication.translate('MainWindow','File')+'PDF (*.pdf)',
			)
		else:
			self.directorioArchivo=dir
		if self.directorioArchivo:
			if not (self.directorioArchivo.endswith('.xls') or self.directorioArchivo.endswith('.xml') or self.directorioArchivo.endswith('.pdf')):
				self.directorioArchivo+='.xls'
			return True
		else:
			self.directorioArchivo=''
		return False


	def onCloseEvent(self,event):
		self.closeAllDialogs()
		self.config.saveGeneral(self.fuente,self.size,self.fileLocation,self.opacity,self.lang)		
		self.config.saveGenRep(self.curve_to_show,self.show_tl,self.h_scale,self.h_min,self.h_max,self.h_great_unit,self.h_small_unit,self.unit,self.v_scale,self.v_min,self.v_max,self.v_great_unit,self.v_small_unit,self.signal,self.background,self.s_low,self.s_high,self.b_low,self.b_high,self.parameters)
		event.accept()
	
	
	def copy(self):
		"""Copia el texto de la casilla seleccionada en el clipboard"""
		self.form1.statusBar().showMessage("")
		if self.treeWidget.selectedIndexes():
			text=''
			item=self.treeWidget.selectedIndexes()[0]
			text+=self.treeWidget.topLevelItem(item.row()).text(item.column())
			for item in self.treeWidget.selectedIndexes()[1:]:
				aux=self.treeWidget.topLevelItem(item.row()).text(item.column())
				if aux:
					text+=', '+aux
			clipboard=QtGui.QApplication.clipboard()
			clipboard.setText(text)

	
	def imprimir(self):
		"""Imprime toda la informacion de la aplicacion"""
		printer =QtGui.QPrinter(QtGui.QPrinter.HighResolution)
		if os.sys.platform=='linux' or os.sys.platform=='linux2':
			printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
			printer.setOutputFileName(str(self.fileLocation)+'/gensec.pdf')
		dialog = QtGui.QPrintDialog(printer,self.form1)
		dialog.addEnabledOption(QtGui.QAbstractPrintDialog.PrintSelection)
		dialog.setWindowTitle('Print Table')
		
		if dialog.exec_() == QtGui.QDialog.Accepted:
			document=QtGui.QTextDocument()
			document.setHtml(QtCore.QString.fromUtf8(self.buildHtml()))
			document.print_(printer)
			self.form1.statusBar().showMessage(QtGui.QApplication.translate('MainWindow',"The document has been printed"))
		dialog.show()	
			
			
	def buildHtml(self):			
		"""Construye una tabla html con estructura igual a la del gensec, con la informacion de esta"""
		hora='<table><tr><td> GenRep : '+str(datetime.datetime.fromtimestamp(time.time()))+'</td></tr></td></tr><tr><td> </td></tr></table>'
		html=''
		cant_filas=0
		for i in range(self.treeWidget.topLevelItemCount()):
			item = self.treeWidget.topLevelItem( i )
			cant_filas+=1
			colum=0
			html+='<tr>'
			for column in range(self.treeWidget.columnCount()):
				if not self.treeWidget.isColumnHidden(column):
					color= item.textColor(column).name()
					font= self.treeWidget.font().family()
					size= str(self.treeWidget.font().pointSize())
					dato=item.text(column)
					html+='<td style="font-family:'+font+'; font-size:'+size+'; color:'+color+';">     '+dato+'     </td>'
			html+='</tr>'
		html+="</table></body></html>"
		
		header='<table border="2"><tr>'
		for column in range(self.treeWidget.columnCount()):
			if not self.treeWidget.isColumnHidden(column):
				columna=self.header.model().headerData(column,QtCore.Qt.Horizontal).toString()
				header+='<td>     '+str(columna)+'     </td>'			
		header+='</tr>'
		
		html=hora+header+html
		return html
		
	
	def addGroup(self):
		"""Adiciona una fila para otra muestra"""
		self.closeAllDialogs()
		self.form1.statusBar().showMessage("")
		item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
		item_0.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
		self.toolButtonHeader = QtGui.QToolButton()
		self.toolButtonHeader.setText(QtGui.QApplication.translate("MainWindow", str(self.grupos+1), None, QtGui.QApplication.UnicodeUTF8))
		font = QtGui.QFont()
		font.setFamily(("Novason"))
		font.setPointSize(12)
		font.setBold(False)
		font.setItalic(False)
		font.setUnderline(False)
		font.setWeight(53)
		font.setStrikeOut(False)
		font.setKerning(False)
		font.setStyleStrategy(QtGui.QFont.PreferDefault)
		self.toolButtonHeader.setFont(font)
		self.toolButtonHeader.setObjectName(("toolButton"))
		self.toolButtonHeader.setStyleSheet(HEADER_TOOLBUTTON_STYLE)
		self.treeWidget.setItemWidget(item_0, 0,self.toolButtonHeader)
		self.toolButtonHeader.clicked.connect(partial(self.selectRow,True,self.grupos+1))
		vs=self.treeWidget.verticalScrollBar()
		vs.setValue(vs.maximum())
		self.grupos+=1
		
	
	def addComand(self):
		"""Adiciona una columna para comandos"""
		self.closeAllDialogs()
		self.treeWidget.headerItem().setText(self.comandos+1, (QtGui.QApplication.translate('MainWindow',"Command ")+str(self.comandos)))
		hs=self.treeWidget.horizontalScrollBar()
		hs.setValue(hs.maximum())			
		self.comandos+=1
		
			
	def change(self):
		"""Cambia el tipo de letra y el tamanno de los elementos de la tabla"""
		self.fuente=self.fontS.fontComboBox.currentFont().toString().split(',')[0]
		self.size=self.fontS.spinBox.value()
		self.fontS.form1.close()
		font = QtGui.QFont()
		font.setFamily(self.fuente)
		font.setPointSize(self.size)
		font.setBold(False)
		font.setItalic(False)
		font.setUnderline(False)
		font.setWeight(53)
		font.setStrikeOut(False)
		font.setKerning(False)
		font.setStyleStrategy(QtGui.QFont.PreferDefault)
		self.treeWidget.setFont(font)
		self.form1.statusBar().showMessage(QtGui.QApplication.translate('MainWindow',"The font has been changed"))
		
	
	def setValue(self,row,column,valor):
		"""Introduce un valor en determinado campo, column, tiene que ser mayor que 0"""
		item=self.treeWidget.topLevelItem( row )
		if not item.text(column):
			item.setTextColor(column,QtGui.QColor('#000000'))
		item.setText(column,valor)
			
	
	def selectRow(self, ok=False, row=False):
		"""Selecciona un conjunto de filas, recibe por parametro un estrin de la forma: row,row,row...."""					
		if not ok:
			row, ok = QtGui.QInputDialog.getInteger(self.form1, QtGui.QApplication.translate('MainWindow','Row Number'), QtGui.QApplication.translate('MainWindow','Row')+':',0,1)			
		if ok:				
			for i in self.treeWidget.selectedIndexes():
				item = self.treeWidget.topLevelItem(i.row())
				item.setSelected(False)				
			row=int(row)-1
			try:
				item = self.treeWidget.topLevelItem(row)
				item.setSelected(True)
				if self.selected_row[1]:
					self.selected_row[1].setStyleSheet(HEADER_TOOLBUTTON_STYLE)
				self.selected_row[1]=self.treeWidget.itemWidget(item,0)
				self.selected_row[1].setStyleSheet(HEADER_TOOLBUTTON_STYLE2)
				self.selected_row[0]=row
				self.clear_lateral_panel()
				self.fill_lateral_panel()
			except:
				pass
					
					
	def clear_lateral_panel(self):
		for i in range(self.treeWidget_2.topLevelItemCount()):
			item = self.treeWidget_2.topLevelItem(i)
			dato=item.text(0)
			if dato!='':
				item.setHidden(True)
	
	
	def fill_lateral_panel(self):
		item = self.treeWidget.topLevelItem(self.selected_row[0])
		for column in range(self.comandos+1)[2:]:
			dato=item.text(column)
			if dato!='':
				info=self.processData[str(self.selected_row[0])+','+str(column)]
				if info['id'] > 1 and info['id'] < 7:
					#Comprobar k curvas son las k necesito self.curve_to_show
					header=self.header.model().headerData(column,QtCore.Qt.Horizontal).toString()						
					item_2 = QtGui.QTreeWidgetItem(self.treeWidget_2)
					item_2.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
					item_2.setText(0,header)
					for i in self.curve_to_show:
						if info['Curva'+str(i)] !='':	
							item_2.addChild(QtGui.QTreeWidgetItem(str(i)))
							
					if item_2.childCount ()>0:
						self.treeWidget_2.setItemWidget(item_2, 0,QtGui.QWidget())



class BackgroundColorDelegate(QtGui.QStyledItemDelegate):
	def __init__(self, parent,columns,colorear,dejar,color):
		super(BackgroundColorDelegate, self).__init__(parent)
		self.columns=columns
		self.colorear=colorear
		self.dejar=dejar
		self.color=color

	def paint(self, painter, option, index):
		if index.column() in self.columns and self.colorear:
			painter.fillRect(option.rect, self.color)
			super(BackgroundColorDelegate, self).paint(painter, option, index)
		elif index.column() in self.dejar:
			painter.fillRect(option.rect, self.dejar[index.column()])
			super(BackgroundColorDelegate, self).paint(painter, option, index)
		else:			
			super(BackgroundColorDelegate, self).paint(painter, option, index)
	

class Animation(QtCore.QPropertyAnimation):
	LinearPath, CirclePath = range(2)

	def __init__(self, target, prop):
		super(Animation, self).__init__(target, prop)

		self.setPathType(Animation.LinearPath)

	def setPathType(self, pathType):
		self.m_pathType = pathType
		self.m_path = QtGui.QPainterPath()

	def updateCurrentTime(self, currentTime):
		if self.m_pathType == Animation.CirclePath:
			if self.m_path.isEmpty():
				end = self.endValue()
				start = self.startValue()
				self.m_path.moveTo(start)
				self.m_path.addEllipse(QtCore.QRectF(start, end))

			dura = self.duration()
			if dura == 0:
				progress = 1.0
			else:
				progress = (((currentTime - 1) % dura) + 1) / float(dura)

			easedProgress = self.easingCurve().valueForProgress(progress)
			if easedProgress > 1.0:
				easedProgress -= 1.0
			elif easedProgress < 0:
				easedProgress += 1.0

			pt = self.m_path.pointAtPercent(easedProgress)
			self.updateCurrentValue(pt)
			self.valueChanged.emit(pt)
		else:
			super(Animation, self).updateCurrentTime(currentTime)