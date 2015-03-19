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

from Lienzo import *

import threading
from gensec_base import *

from Dialogs.setup import Setup
from Dialogs.profile import Profile 
from Dialogs.association import Association
from Dialogs.apply_to import Apply_To
from XMLDriver import createRLF

import math

class INDEX:
	def __init__(self,row,column):
		self.r=row
		self.c=column
	def row(self):
		return self.r
	def column(self):
		return self.c

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
			self.consecutives=self.genrep_config[19]
			self.parameters=self.genrep_config[20]
		else:
			self.curve_to_show=[1]
			self.show_tl=0
			self.h_scale='linear'
			self.h_min=-1
			self.h_max=-1
			self.h_great_unit=20
			self.h_small_unit=5
			self.unit=0
			self.v_scale='linear'
			self.v_min=-1
			self.v_max=-1
			self.v_great_unit=5000
			self.v_small_unit=500
			self.signal=True
			self.background=True
			self.s_low=0
			self.s_high=10
			self.b_low=-10
			self.b_high=0
			self.consecutives=True
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
			"Illumination Source",
			"Illumination Power",
			"Illumination Temperature",
		)
		
		self.NMuestras=0
		UI_GenSec_Base.__init__(self,'GenRep','pixmaps/genrep.ico',dir)
				
		self.treeWidget.itemSelectionChanged.connect(self.groupActive)
		self.header=self.treeWidget.header()			
		self.header.setClickable(True)	
		self.form1.resizeEvent = self.onResize
		self.actionAcerda_de.triggered.connect(partial(about,self.form1,'GenRep',QtGui.QApplication.translate("MainWindow", 'Report Generator', None, QtGui.QApplication.UnicodeUTF8),QtGui.QApplication.translate("MainWindow", 'Description', None, QtGui.QApplication.UnicodeUTF8),'1.0.0',"pixmaps/genrep.ico"))
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
		self.groupsColors={}
		self.values_sig={}
		self.values_back={}
		self.actual_in_graph=''	
		
		self.establecerFondo()
		self.create_graphic(X,Y)
		
	
	@cursorAction()
	def save(self,temp=False):
		"""Guarda la informacion en forma de xml"""
		self.closeAllDialogs()
		if self.directorioArchivo=='':
			return self.saveAs()
		else:
			if (type(self.directorioArchivo)==QtCore.QString and (self.directorioArchivo.endsWith('.rlf') or self.directorioArchivo.endsWith('.xml'))) or (type(self.directorioArchivo)==str and (self.directorioArchivo.endswith('.rlf') or self.directorioArchivo.endswith('.xml'))):
				self.createXML()
				self.myREP.save(str(self.directorioArchivo),True)
				#self.thereAreCanges=False
				self.form1.statusBar().showMessage(QtGui.QApplication.translate('MainWindow',"The document has been saved"))
				
			# faltan el slf, pdfs
	
	
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
				QtGui.QApplication.translate('MainWindow','File')+' RLF (*.rlf);; '+QtGui.QApplication.translate('MainWindow','File')+'XLS (*.xls);; '+QtGui.QApplication.translate('MainWindow','File')+'XML (*.xml);; '+QtGui.QApplication.translate('MainWindow','File')+'PDF (*.pdf)',
				'0',
				QtGui.QFileDialog.DontUseNativeDialog,
			)
		else:
			self.directorioArchivo=dir
		if self.directorioArchivo:
			if (type(self.directorioArchivo)==QtCore.QString and not (self.directorioArchivo.endsWith('.xls') or self.directorioArchivo.endsWith('.rlf') or self.directorioArchivo.endsWith('.xml') or self.directorioArchivo.endsWith('.pdf'))) or (type(self.directorioArchivo)==str and not (self.directorioArchivo.endswith('.xls') or self.directorioArchivo.endswith('.rlf') or self.directorioArchivo.endswith('.xml') or self.directorioArchivo.endswith('.pdf'))):
				self.directorioArchivo+='.rlf'
			
			if (type(self.directorioArchivo)==QtCore.QString and (self.directorioArchivo.endsWith('.rlf') or self.directorioArchivo.endsWith('.xml'))) or (type(self.directorioArchivo)==str and (self.directorioArchivo.endswith('.rlf') or self.directorioArchivo.endswith('.xml'))):
				self.createXML()
				self.myREP.save(str(self.directorioArchivo),True)
				#self.thereAreCanges=False
				self.form1.statusBar().showMessage(QtGui.QApplication.translate('MainWindow',"The document has been saved"))
				
			# faltan el slf, pdf
			return True
		else:
			self.directorioArchivo=''
		return False
		
	
	def createXML(self):
		"""Genera una estructura xml a partir de los datos entrados por el usuario"""
		self.myREP=None
		tabla=self.getallData()		
		self.myREP=createRLF.REP(nmuestras=self.NMuestras,name=self.nombre,owner=self.propietario,n2flow=self.nitrogeno,doserate=self.dosis,extdoserate=self.dosisE,protocol=self.protocolo,status=self.STATUS,reader_id=self.id_lector,datecrea=self.datecrea)
		
		for item in tabla:
				ran=item[0]				
				samples=ran.split(',')
				for sample in samples:
					if len(sample)==1:
						samples_id=sample
					elif len(sample)>1:
						val=sample.split('-')
						samples_id=range(int(val[0]),int(val[-1])+1)
					for sample_id in samples_id:						
						Sample_ID=self.myREP.createSample(sample_id)
						po_id=1
						for command in item[1]:
							cant=command[1].keys()
							if cant!=[]:
								curves=[]
								for curve in command[1]:
									curv=int(curve.split(',')[2])
									curves.append(self.myREP.createCurve(curv,command[1][curve][2], command[1][curve][0][0], command[1][curve][0][1], command[1][curve][3], command[1][curve][1][0],command[1][curve][1][1]))
								
								data={}
								pos=cant[0][:-2]
								for group in self.inGroup:
									if pos in group:
										for cm in (y for y in group if y != pos):
											info=self.processData[cm]
											
											if info['id']==0:
												if 2 in self.parameters:
													data["External_irradiation"]=self.getData(info,"External Irradiation Time",False)
												if 3 in self.parameters:
													data["External_dose"]=self.getData(info,"External Dose",False)
												if 13 in self.parameters:
													data["Time_external_irradiation"]=self.getData(info,"Time of External irradiation",False)
													
											if info['id']==1:
												if 0 in self.parameters:
													data["Beta_irradiation_time"]=self.getData(info,"Beta Irradiation Time",False)
												if 1 in self.parameters:
													data["Beta_dose"]=self.getData(info,"Beta Dose",False)
												if 12 in self.parameters:
													data["Time_beta_irradiation"]=self.getData(info,"Time of Beta irradiation",False)											
												
											if info['id']==7:
												if 4 in self.parameters:
													data["Preheating_temperature"]=self.getData(info,"Preheating Temperature",False)
												if 6 in self.parameters:
													data["Preheating_rate"]=self.getData(info,"Preheating Rate",False)	

											if info['id']==8:
												if 15 in self.parameters:
													data["Illumination_source"]=self.getData(info,"Illumination Source",False)
												if 16 in self.parameters:
													data["Illumination_power"]=self.getData(info,"Illumination Power",False)	
												if 17 in self.parameters:
													data["Illumination_temperature"]=self.getData(info,"Illumination Temperature",False)		
										break
			
								info=self.processData[pos]
								if info['id']==3 or info['id']==4 or info['id']==5:
									if 8 in self.parameters:
										data["Light_source"]=self.getData(info,"Light Sour",False)
									if 9 in self.parameters:
										data["Optical_power"]=self.getData(info,"Optical Power",False)		
								
								if info['id']==6:
									if 10 in self.parameters:
										data["Electric_stimulation"]=self.getData(info,"Electric Stimulation",False)
									if 11 in self.parameters:
										data["Electric_frequency"]=self.getData(info,"Electric Frequency",False)
								
								if 5 in self.parameters:
									data["Measuring_temperature"]=self.getData(info,"Measuring Temperature",False)
								if 7 in self.parameters:
									data["Heating_rate"]=self.getData(info,"Heating Rate",False)
								if 14 in self.parameters:
									data["Time_external_irradiation"]=self.getData(info,"Time of Measurement",False)
										
								if info['id']==2:
									p='TL'
								if info['id']==3:
									p='OSL'
								if info['id']==4:
									p='POSL'
								if info['id']==5:
									p='LMOSL'
								if info['id']==6:
									p='ESL'									
								
								self.myREP.createProcessOrder(Sample_ID,po_id,p,info['date_type'],curves,data)
								po_id +=1
							
		
	def getallData(self):
		muestras=[]
		for i in range(self.treeWidget.topLevelItemCount()):
			item = self.treeWidget.topLevelItem( i )
			if item.text(1):
				muestra=[str(item.text(1)),[]]
				for column in range(self.comandos+1)[2:]:
					dato=item.text(column)
					if dato!='':				
						info=self.processData[str(i)+','+str(column)]						
						if info['id'] > 1 and info['id'] < 7:
							curves={}
							for j in self.curve_to_show:
								if info['Curva'+str(j)] !='':
									
									sig_range=[None,None]
									back_range=[None,None]
									
									X,Y=self.getX_Y(i,column,str(j))
									
									if self.values_sig.has_key(str(i)+','+str(column)):									
										sig=self.values_sig[str(i)+','+str(column)]
										back=self.values_back[str(i)+','+str(column)]
									else:
										sig=[X[int(self.s_low)],X[int(self.s_high)]]
										if self.b_high==0:
											max=len(X)-1
										else:
											max=int(self.b_high)
										back=[X[int(self.b_low)],X[max]]
									
									sig_range[0]=int(X.index(sig[0]))
									sig_range[1]=int(X.index(sig[1])+1)
									back_range[0]=int(X.index(back[0]))
									back_range[1]=int(X.index(back[1])+1)
										
									sig_values=Y[sig_range[0]:sig_range[1]]
									back_values=Y[back_range[0]:back_range[1]]

									sig_count=0
									back_count=0
									
									for k in sig_values:
										sig_count+=k
									for k in back_values:
										back_count+=k
										
									curves[str(i)+','+str(column)+','+str(j)]=[sig,back,sig_count,back_count]
							muestra[1].append([info,curves])
				muestras.append(muestra)
		return muestras					


	def changeTheme(self,them):
		"""cambia el idioma por defecto de la aplicacion"""
		self.theme=them
		COL1,COL2,COL3,COL4,COL5,COL6,COL7,COL8=LOAD(them)		
		self.form1.setStyleSheet(BASE(COL1,COL2,COL3,COL4,COL5,COL6,COL7,COL8,False))
		
		COL1,COL2,COL3,COL4,COL5,COL6,COL7,COL8=LOAD(self.theme)	
		self.fondo=[COL2,COL3]
		self.fondo_graph=[COL1,COL2]
		self.font_color=COL8
		self.create_graphic(self.canvas.allGraphic_X,self.canvas.allGraphic_Y)
		self.establecerFondo()
		self.down_area_visible=True
	
	def establecerFondo(self):
		columns=range(self.comandos+1)
		rows=range(self.treeWidget.topLevelItemCount())
		color=''
		colorear=''
		for row in rows:
			dejar=self.dejar(row,[])
			delegate = BackgroundColorDelegate(self.treeWidget,columns,colorear,dejar,color,self.fondo) 
			self.treeWidget.setItemDelegateForRow(row,delegate)
	
	
	def change_graphic(self,item):
		headerName= str(item.text(0))
		if headerName in ['1','2','3']:
			parent=item.parent().text(0)			
			item = self.treeWidget.topLevelItem(self.selected_row[0])
			for column in range(self.comandos+1)[2:]:				
				if self.header.model().headerData(column,QtCore.Qt.Horizontal).toString()==parent:					
					X,Y=self.getX_Y(self.selected_row[0],column,headerName)					
					self.actual_in_graph=str(self.selected_row[0])+','+str(column)
					self.create_graphic(X,Y)
					
					
	def getX_Y(self,r,c,headerName):
		info=self.processData[str(r)+','+str(c)]					
		sum=int(info['datapoints1']+info['datapoints2']+info['datapoints3'])
		Y=[float(i) for i in info['Curva'+headerName].split(';')[:sum]]
		if info['id']==2 and self.show_tl:
			X=[float("{0:.4f}".format(i)) for i in info['Curva3'].split(';')[:sum]]
		else:
			X=range(1,sum+1)
		if self.unit:
			X=[ (i*info['timePerCanel']) for i in X]
		if len(X)>0 and X[0]==0 and (self.h_scale=='log' or self.h_scale=='ln'):
			del X[0]
			new= X[-1]+1
			X.append(new)
		X=[float('%.4f'%i ) for i in X]
		return X,Y
		
			
	def save_sig_back_values(self,pos):
		self.values_sig[pos]=(float(self.spin_values[self.xmin1_sb.value()]),float(self.spin_values[self.xmax1_sb.value()]))
		self.values_back[pos]=(float(self.spin_values[self.xmin2_sb.value()]),float(self.spin_values[self.xmax2_sb.value()]))
		
	
	def Apply_To(self):
		send=[]
		for i in self.parameters:
			send.append(self.enum_parameters	[i])
		self.apply_to_win=Apply_To(send,self.form1)
		self.apply_to_win.pushButton_2.clicked.connect(self.Apply_To_ready)
		self.apply_to_win.pushButton_3.clicked.connect(self.Apply_To_All)
		
		
	def Apply_To_ready(self):
		self.criterias_to=self.apply_to_win.fill_data()
		for i in range(self.treeWidget.topLevelItemCount()):
			item = self.treeWidget.topLevelItem( i )
			if item.text(1):
				muestra=str(item.text(1))					
				first=[]
				if self.criterias_to[0][0]!='':	
					for column in range(self.comandos+1)[2:]:
						if item.text(column):
							criteria=self.criterias_to[0]
							info=self.processData[str(i)+','+str(column)]
							data=self.getData(info,criteria[0],muestra)
							if data!='error':
								if criteria[1]=='Same':
									first.append (INDEX(i,column))
								elif criteria[1]=='Different':
									if str(data)!=str(criteria[2]):
										first.append (INDEX(i,column))
								elif criteria[1]=='Value':
									value=str(criteria[2])										
									if '*' in value:
										data=str(data)
										while ('*' in value):
											p=value.find('*')
											if data[:p]!=value[:p]:
												break
											value=value[p+1:]
											data=data[p+1:]		
										if data==value:
											first.append (INDEX(i,column))											
									else:
										if type(data)==float:
											try:
												value=float(value)
											except:
												value='error'
										if str(data)==str(value):
											first.append (INDEX(i,column))
				if len(self.criterias_to)>1!='':
					second={}
					if len(first)>1:
						for i in first:							
							criteria=self.criterias_to[1]
							info=self.processData[str(i.row())+','+str(i.column())]
							data=self.getData(info,criteria[0],muestra)
							if data!='error':
								if criteria[1]=='Same':
									second.append (INDEX(i.row(),i.column()))
								elif criteria[1]=='Different':
									if str(data)!=str(criteria[2]):
										second.append (INDEX(i.row(),i.column()))
								elif criteria[1]=='Value':
									value=str(criteria[2])										
									if '*' in value:
										data=str(data)
										while ('*' in value):
											p=value.find('*')
											if data[:p]!=value[:p]:
												break
											value=value[p+1:]
											data=data[p+1:]		
										if data==value:
											second.append (INDEX(i.row(),i.column()))										
									else:
										if type(data)==float:
											try:
												value=float(value)
											except:
												value='error'
										if str(data)==str(value):
											second.append (INDEX(i.row(),i.column()))
										
					if len(self.criterias_to)>2!='':		
						tercero={}
						if len(second)>1:
							for i in second:							
								criteria=self.criterias_to[2]
								info=self.processData[str(i.row())+','+str(i.column())]
								data=self.getData(info,criteria[0],muestra)
								if data!='error':
									if criteria[1]=='Same':
										tercero.append (INDEX(i.row(),i.column()))
									elif criteria[1]=='Different':
										if str(data)!=str(criteria[2]):
											tercero.append (INDEX(i.row(),i.column()))
									elif criteria[1]=='Value':
										value=str(criteria[2])										
										if '*' in value:
											data=str(data)
											while ('*' in value):
												p=value.find('*')
												if data[:p]!=value[:p]:
													break
												value=value[p+1:]
												data=data[p+1:]		
											if data==value:
												tercero.append (INDEX(i.row(),i.column()))										
										else:
											if type(data)==float:
												try:
													value=float(value)
												except:
													value='error'
											if str(data)==str(value):
												tercero.append (INDEX(i.row(),i.column()))
						if len(self.criterias_to)>3!='':		
							cuarto={}
							if len(tercero)>1:
								for i in tercero:							
									criteria=self.criterias_to[3]
									info=self.processData[str(i.row())+','+str(i.column())]
									data=self.getData(info,criteria[0],muestra)	
									if data!='error':
										if criteria[1]=='Same':
											cuarto.append (INDEX(i.row(),i.column()))
										elif criteria[1]=='Different':
											if str(data)!=str(criteria[2]):
												cuarto.append (INDEX(i.row(),i.column()))
										elif criteria[1]=='Value':
											value=str(criteria[2])										
											if '*' in value:
												data=str(data)
												while ('*' in value):
													p=value.find('*')
													if data[:p]!=value[:p]:
														break
													value=value[p+1:]
													data=data[p+1:]		
												if data==value:
													cuarto.append (INDEX(i.row(),i.column()))										
											else:
												if type(data)==float:
													try:
														value=float(value)
													except:
														value='error'
												if str(data)==str(value):
													cuarto.append (INDEX(i.row(),i.column()))
							for k in cuarto:
								self.save_sig_back_values(str(k.row())+','+str(k.column()))
						else:
							for k in tercero:
								self.save_sig_back_values(str(k.row())+','+str(k.column()))
					else:
						for k in second:
							self.save_sig_back_values(str(k.row())+','+str(k.column()))
				else:
					for k in first:
						self.save_sig_back_values(str(k.row())+','+str(k.column()))
		
		
		self.apply_to_win.form1.close()
	
	
	def Apply_To_All(self):
		for i in range(self.treeWidget.topLevelItemCount()):
			item = self.treeWidget.topLevelItem( i )
			for column in range(self.comandos+1)[2:]:
				dato=item.text(column)
				if dato!='':
					info=self.processData[str(i)+','+str(column)]
					if info['id'] > 1 and info['id'] < 7:
						for j in self.curve_to_show:
							if info['Curva'+str(j)] !='':	
								self.save_sig_back_values(str(i)+','+str(column))
		try:
			self.apply_to_win.form1.close()
		except:
			pass
								
	
	def associationCriteria(self):
		send=[]
		for i in self.parameters:
			send.append(self.enum_parameters	[i])
		self.association=Association(send,self.consecutives,self.form1)
		self.association.pushButton_2.clicked.connect(self.association_ready)	
		
		
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
		X=[]
		Y=[]
		self.groupsColors={}
		self.values_sig={}
		self.values_back={}
		self.actual_in_graph=''
		
		self.create_graphic(X,Y)
		self.clear_lateral_panel()
		
		self.selected_row=[False,False]
		self.colores_in_row={}
		for group in self.inGroup:		
			self.colorearGrupo([group[0]],False,[])
		self.inGroup=[]
		self.directorioArchivo=''
		
	@cursorAction()
	def create_graphic(self,X,Y):
		self.pan=False
		self.zoom=False
		
		w=int(self.W/64)
		
		if self.actual_in_graph=='' or not self.values_sig.has_key(self.actual_in_graph):
			sl=self.s_low
			sh=self.s_high
			bl=self.b_low
			bh=self.b_high
			default=True
		else:
			sl=self.values_sig[self.actual_in_graph][0]
			sh=self.values_sig[self.actual_in_graph][1]
			bl=self.values_back[self.actual_in_graph][0]
			bh=self.values_back[self.actual_in_graph][1]
			default=False
		
		self.canvas = Lienzo(X,Y,w,sl,sh,bl,bh,default,self.signal,self.background,self.h_min,self.h_max,self.h_great_unit,self.h_small_unit,self.v_min,self.v_max,self.v_great_unit,self.v_small_unit,self.fondo_graph,self.font_color,self.verticalLayoutWidget)
		try:
			if self.v_scale=='log':
				self.canvas.allGraphic.set_yscale('log', basey=10)
				if self.canvas.active_sig:
					self.canvas.Signal.set_yscale('log', basey=10)
				if self.canvas.active_back:
					self.canvas.Background.set_yscale('log', basey=10)
			elif self.v_scale=='ln':
				self.canvas.allGraphic.set_yscale('log', basey=math.e)
				if self.canvas.active_sig:
					self.canvas.Signal.set_yscale('log', basey=math.e)
				if self.canvas.active_back:
					self.canvas.Background.set_yscale('log', basey=math.e)
		except:
			pass
		try:
			if self.h_scale=='log':
				self.canvas.allGraphic.set_xscale('log', basey=10)
				if self.canvas.active_sig:
					self.canvas.Signal.set_xscale('log', basey=10)
				if self.canvas.active_back:
					self.canvas.Background.set_xscale('log', basey=10)
			elif self.h_scale=='ln':
				self.canvas.allGraphic.set_xscale('log', basey=math.e)
				if self.canvas.active_sig:
					self.canvas.Signal.set_xscale('log', basey=math.e)
				if self.canvas.active_back:
					self.canvas.Background.set_xscale('log', basey=math.e)
		except:
			pass
		
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
							event.inaxes.patch.set_facecolor(self.fondo_graph[0])
							event.canvas.draw()
							self.canvas.activeSignal=False
					elif event.inaxes.get_title()=='Background(BG)' and not self.canvas.activeSignal:
						if not self.canvas.activeBackground:
							self.form1.statusBar().showMessage(QtGui.QApplication.translate('MainWindow',"Background area is selected"),3000)
							event.inaxes.patch.set_facecolor('#6C9DEC')
							event.canvas.draw()
							self.canvas.activeBackground=True
						else:
							event.inaxes.patch.set_facecolor(self.fondo_graph[0])
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
		self.canvas.fig.set_facecolor(self.fondo_graph[0])
		
		self.spin_values=['%.4f'%i for i in self.canvas.allGraphic_X]
		
		xmin1_label=QtGui.QLabel('low')		
		xmin1_label.setStyleSheet('color:green')
		self.xmin1_sb = ValuesSpinBox(self.spin_values)		
		self.xmin1_sb.setStatusTip(QtGui.QApplication.translate("MainWindow", 'Low channel to signal'))	
		
		xmax1_label=QtGui.QLabel('high')
		xmax1_label.setStyleSheet('color:green')
		self.xmax1_sb =ValuesSpinBox(self.spin_values)	
		self.xmax1_sb.setStatusTip(QtGui.QApplication.translate("MainWindow", 'High channel to signal'))
		
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

		self.xmin2_sb = ValuesSpinBox(self.spin_values)	
		self.xmin2_sb.setStatusTip(QtGui.QApplication.translate("MainWindow", 'Low channel to Background'))
		
		xmax2_label=QtGui.QLabel('high')
		xmax2_label.setStyleSheet('color:#1A297D')
		self.xmax2_sb =ValuesSpinBox(self.spin_values)	
		self.xmax2_sb.setStatusTip(QtGui.QApplication.translate("MainWindow", 'High channel to Background'))
		
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
		apply_all.clicked.connect(self.Apply_To_All)
		
		self.verticalLayout.addWidget(ToolBarr,2,0,6,1)
		self.verticalLayout.addWidget(self.canvas,0,0,10,60)		
		
		
		self.sig_verticalLayout.addWidget(xmin1_label,0,0,1,1)
		self.sig_verticalLayout.addWidget(self.xmin1_sb,1,0,1,1)		
		self.sig_verticalLayout.addWidget(sign_count_label,0,2,1,2)
		self.sig_verticalLayout.addWidget(sign_count_line,1,2,1,2)		
		self.sig_verticalLayout.addWidget(xmax1_label,0,5,1,1)
		self.sig_verticalLayout.addWidget(self.xmax1_sb,1,5,1,1)
		self.sig_verticalLayout.setColumnMinimumWidth(3,80)		
		self.verticalLayout.addWidget(self.sig_widget,11,0,2,15)
			
		self.verticalLayout.addWidget(apply_to,12,19,1,7)
		self.verticalLayout.addWidget(apply_all,12,34,1,7)
		
		self.back_verticalLayout.addWidget(xmin2_label,0,0,1,1)
		self.back_verticalLayout.addWidget(self.xmin2_sb,1,0,1,1)
		self.back_verticalLayout.addWidget(back_count_label,0,2,1,2)
		self.back_verticalLayout.addWidget(back_count_line,1,2,1,2)	
		self.back_verticalLayout.addWidget(xmax2_label,0,5,1,1)
		self.back_verticalLayout.addWidget(self.xmax2_sb,1,5,1,1)
		self.back_verticalLayout.setColumnMinimumWidth(3,80)
		self.verticalLayout.addWidget(self.back_widget,11,45,2,15)
		
		
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
			x1=self.spin_values.index('%.4f'%x1)
			x2=self.spin_values.index('%.4f'%x2)
			self.xmin1_sb.setValue(x1)
			self.xmax1_sb.setValue(x2)			
			count_signal()			

		def fill_x_2(x1,x2):
			x1=self.spin_values.index('%.4f'%x1)
			x2=self.spin_values.index('%.4f'%x2)
			self.xmin2_sb.setValue(x1)
			self.xmax2_sb.setValue(x2)
			count_background()
			self.flag=True
		
		def x1_sb_change(buttom):
			if not self.canvas.activeSignal:
				if self.xmax1_sb.value() >=self.xmin1_sb.value():
					pass
					self.canvas.activeSignal=True
					self.canvas.onselect(float(self.spin_values[self.xmin1_sb.value()]),float(self.spin_values[self.xmax1_sb.value()]),True)
			self.save_sig_back_values(self.actual_in_graph)

			
		def x2_sb_change(buttom):
			if not self.canvas.activeBackground:				
				if self.xmax2_sb.value() >=self.xmin2_sb.value():
					self.canvas.activeBackground=True
					self.canvas.onselect(float(self.spin_values[self.xmin2_sb.value()]),float(self.spin_values[self.xmax2_sb.value()]),True)
			self.save_sig_back_values(self.actual_in_graph)
			
				
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
			

			self.xmin1_sb.valueChanged.connect(partial(x1_sb_change,1))
			self.xmax1_sb.valueChanged.connect(partial(x1_sb_change,2))
			self.xmin2_sb.valueChanged.connect(partial(x2_sb_change,1))
			self.xmax2_sb.valueChanged.connect(partial(x2_sb_change,2))	
			self.canvas.signal_change.connect(fill_x_1)
			self.canvas.background_change.connect(fill_x_2)
			
			if self.signal:
				fill_x_1(self.canvas.Signal_X[0],self.canvas.Signal_X[-1])
			if self.background:
				fill_x_2(self.canvas.Background_X[0],self.canvas.Background_X[-1])
			
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
		self.treeWidget_2.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		self.treeWidget_2.headerItem().setText(0, QtGui.QApplication.translate('MainWindow',"Columns"))
		
		self.mainWidget=QtGui.QWidget()
		self.form1.setCentralWidget(self.mainWidget)
		
		#Panel de abajo
		self.down_area= QtGui.QWidget()
		self.down_area_layout=QtGui.QGridLayout(self.down_area)
		self.active_bar=QtGui.QLabel()
		self.active_bar.mouseDoubleClickEvent=self.show_hidden_down_area
		self.active_bar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.active_bar.setStatusTip(QtGui.QApplication.translate("MainWindow", 'Show/Hidde graphic'))
		self.active_bar.setStyleSheet('background:#E8E8E8')
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
		delegate = BackgroundColorDelegate(self.treeWidget,columns,colorear,dejar,color,self.fondo) 
		self.treeWidget.setItemDelegateForRow(row,delegate)
		
	
	def dejar(self,row,toGroup):
		if row!=None:
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
	
	
	def getData(self,info,data,muestra):
			try:
				if data=="Sample ID":
					return muestra
				elif data=="Process Order":
					return float(info['process_order_id'])
				elif data=="Data Type":
					return info['date_type']
				elif data=="Beta Irradiation Time" and info['id']==1:
					return float(info['time'])
				elif data=="Beta Dose"  and info['id']==1:
					return float(info['time'])*float(self.dosis)
				elif data=="External Irradiation Time"  and info['id']==0:
					return float(info['time'])
				elif data=="External Dose"  and info['id']==0:
					return float(info['time'])*float(self.dosisE)
				elif data=="Preheating Temperature" and info['id']==7:
					return float(info['final_temp'])
				elif data=="Measuring Temperature" and (info['id']==2  or info['id']==3  or info['id']==4  or info['id']==5  or info['id']==6):
					return float(info['final_temp'])
				elif data=="Preheating Rate" and info['id']==7:
					return float(info['heating_rate'])
				elif data=="Heating Rate" and (info['id']==2  or info['id']==3  or info['id']==4  or info['id']==5  or info['id']==6):
					return float(info['heating_rate'])
				elif data=="Light Source":
					return str(info['light_source'])
				elif data=="Optical Power":
					return float(info['start_optical_power'])
				elif data=="Electric Stimulation":
					return float(info['excV'])
				elif data=="Electric Frequency":
					return float(info['excF'])
				elif data=="Time of Beta irradiation" and info['id']==1:
					return str(info['Tiempo2'])
				elif data=="Time of External irradiation" and info['id']==0:
					return str(info['Tiempo2'])
				elif data=="Time of Measurement" and (info['id']==2  or info['id']==3  or info['id']==4  or info['id']==5  or info['id']==6):
					return str(info['Tiempo1'])
				elif data=="Illumination Source" and info['id']==8:
					return str(info['light_source'])
				elif data=="Illumination Power" and info['id']==8:
					return str(info['start_optical_power'])
				elif data=="Illumination Temperature" and info['id']==8:
					return str(info['final_temp'])
				else:
					return 'error'
			except:
				return 'error'
				
	def association_ready(self):
		self.criterias,self.consecutives=self.association.fill_data()
		print self.criterias
		print self.consecutives
		
		for i in range(self.treeWidget.topLevelItemCount()):
			item = self.treeWidget.topLevelItem( i )
			if item.text(1):
				muestra=str(item.text(1))					
				first={}
				if self.criterias[0][0]!='':	
					for column in range(self.comandos+1)[2:]:
						if item.text(column):
							criteria=self.criterias[0]
							info=self.processData[str(i)+','+str(column)]
							data=self.getData(info,criteria[0],muestra)
							if data!='error':
								if criteria[1]=='Same':
									first.setdefault(data, []).append (INDEX(i,column))
								elif criteria[1]=='Different':
									if str(data)!=str(criteria[2]):
										first.setdefault(data, []).append (INDEX(i,column))
								elif criteria[1]=='Value':
									value=str(criteria[2])										
									if '*' in value:
										data=str(data)
										while ('*' in value):
											p=value.find('*')
											if data[:p]!=value[:p]:
												break
											value=value[p+1:]
											data=data[p+1:]		
										if data==value:
											first.setdefault(str(criteria[2]), []).append (INDEX(i,column))											
									else:
										if type(data)==float:
											try:
												value=float(value)
											except:
												value='error'
										print data
										print value
										print str(data)==str(value)
										print "*****************************"
										if str(data)==str(value):
											first.setdefault(data, []).append (INDEX(i,column))
		
				
				if len(self.criterias)>1!='':					
					for list in first.values():
						second={}
						if len(list)>1:
							for i in list:							
								criteria=self.criterias[1]
								info=self.processData[str(i.row())+','+str(i.column())]
								data=self.getData(info,criteria[0],muestra)
								if data!='error':
									if criteria[1]=='Same':
										second.setdefault(data, []).append (INDEX(i.row(),i.column()))
									elif criteria[1]=='Different':
										if str(data)!=str(criteria[2]):
											second.setdefault(data, []).append (INDEX(i.row(),i.column()))
									elif criteria[1]=='Value':
										value=str(criteria[2])										
										if '*' in value:
											data=str(data)
											while ('*' in value):
												p=value.find('*')
												if data[:p]!=value[:p]:
													break
												value=value[p+1:]
												data=data[p+1:]		
											if data==value:
												second.setdefault(str(criteria[2]), []).append (INDEX(i.row(),i.column()))										
										else:
											if type(data)==float:
												try:
													value=float(value)
												except:
													value='error'
											if str(data)==str(value):
												second.setdefault(data, []).append (INDEX(i.row(),i.column()))
											
						if len(self.criterias)>2!='':		
							for list in second.values():
								tercero={}
								if len(list)>1:
									for i in list:							
										criteria=self.criterias[2]
										info=self.processData[str(i.row())+','+str(i.column())]
										data=self.getData(info,criteria[0],muestra)
										if data!='error':
											if criteria[1]=='Same':
												tercero.setdefault(data, []).append (INDEX(i.row(),i.column()))
											elif criteria[1]=='Different':
												if str(data)!=str(criteria[2]):
													tercero.setdefault(data, []).append (INDEX(i.row(),i.column()))
											elif criteria[1]=='Value':
												value=str(criteria[2])										
												if '*' in value:
													data=str(data)
													while ('*' in value):
														p=value.find('*')
														if data[:p]!=value[:p]:
															break
														value=value[p+1:]
														data=data[p+1:]		
													if data==value:
														tercero.setdefault(str(criteria[2]), []).append (INDEX(i.row(),i.column()))										
												else:
													if type(data)==float:
														try:
															value=float(value)
														except:
															value='error'
													if str(data)==str(value):
														tercero.setdefault(data, []).append (INDEX(i.row(),i.column()))
													
								if len(self.criterias)>3!='':		
									for list in tercero.values():
										cuarto={}
										if len(list)>1:
											for i in list:							
												criteria=self.criterias[3]
												info=self.processData[str(i.row())+','+str(i.column())]
												data=self.getData(info,criteria[0],muestra)	
												if data!='error':
													if criteria[1]=='Same':
														cuarto.setdefault(data, []).append (INDEX(i.row(),i.column()))
													elif criteria[1]=='Different':
														if str(data)!=str(criteria[2]):
															cuarto.setdefault(data, []).append (INDEX(i.row(),i.column()))
													elif criteria[1]=='Value':
														value=str(criteria[2])										
														if '*' in value:
															data=str(data)
															while ('*' in value):
																p=value.find('*')
																if data[:p]!=value[:p]:
																	break
																value=value[p+1:]
																data=data[p+1:]		
															if data==value:
																cuarto.setdefault(str(criteria[2]), []).append (INDEX(i.row(),i.column()))										
														else:
															if type(data)==float:
																try:
																	value=float(value)
																except:
																	value='error'
															if str(data)==str(value):
																cuarto.setdefault(data, []).append (INDEX(i.row(),i.column()))
										for list in cuarto.values():
											if len(list)>1:
												self.group(list)
								else:
									for list in tercero.values():
										if len(list)>1:
											self.group(list)
						else:
							for list in second.values():
								if len(list)>1:
									self.group(list)
				else:
					for list in first.values():
						if len(list)>1:
							self.group(list)
								
						
		self.association.form1.close()
	
	def group(self,selected=False):
		toGroup=[]
		borrar=[]
		row=None
		if not selected:
			selected=self.treeWidget.selectedIndexes()
		
		for item in selected:
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
			if self.pertenecen_consecutivos() or not self.consecutives :
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
	
	def show_hidden_down_area(self,event):
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


	def onCloseEvent(self,event):
		self.closeAllDialogs()
		self.config.saveGeneral(self.fuente,self.size,self.fileLocation,self.opacity,self.lang,self.theme)		
		self.config.saveGenRep(self.curve_to_show,self.show_tl,self.h_scale,self.h_min,self.h_max,self.h_great_unit,self.h_small_unit,self.unit,self.v_scale,self.v_min,self.v_max,self.v_great_unit,self.v_small_unit,self.signal,self.background,self.s_low,self.s_high,self.b_low,self.b_high,self.consecutives,self.parameters)
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
		"""Selecciona un conjunto de filas, recibe por parametro un string de la forma: row,row,row...."""					
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
					#self.selected_row[1].setStyleSheet(HEADER_TOOLBUTTON_STYLE)
					pass
				self.selected_row[1]=self.treeWidget.itemWidget(item,0)
				#self.selected_row[1].setStyleSheet(HEADER_TOOLBUTTON_STYLE2)
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
		if type(self.selected_row[0])==int:
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
						
						item_2.setExpanded (True)
						
						if not item_2.childCount()>0:
							item_2.setHidden(True)
						


class BackgroundColorDelegate(QtGui.QStyledItemDelegate):
	def __init__(self, parent,columns,colorear,dejar,color,fondo):
		super(BackgroundColorDelegate, self).__init__(parent)
		self.columns=columns
		self.colorear=colorear
		self.dejar=dejar
		self.color=color
		self.fondo=fondo

	def paint(self, painter, option, index):
		if index.column() in self.columns and self.colorear:
			painter.fillRect(option.rect, self.color)
			super(BackgroundColorDelegate, self).paint(painter, option, index)
		elif index.column() in self.dejar:
			painter.fillRect(option.rect, self.dejar[index.column()])
			super(BackgroundColorDelegate, self).paint(painter, option, index)
		elif index.row() %2==0:
			painter.fillRect(option.rect, QtGui.QColor(self.fondo[0]),)
			super(BackgroundColorDelegate, self).paint(painter, option, index)
		else:
			painter.fillRect(option.rect, QtGui.QColor(self.fondo[1]),)
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
			
			
class ValuesSpinBox(QtGui.QSpinBox):
    def __init__(self, values, parent=None):
        super(ValuesSpinBox, self).__init__(parent)
        if values==[]:
			values=['0,0000']
        self.setStrings(values)

    def strings(self):
        return self._strings

    def setStrings(self, strings):
        self._strings = tuple(strings)
        self._values = dict(zip(strings, range(len(strings))))
        self.setRange(0, len(strings) - 1)

    def textFromValue(self, value):
        return self._strings[value]

    def valueFromText(self, text):
        return self._values[text]