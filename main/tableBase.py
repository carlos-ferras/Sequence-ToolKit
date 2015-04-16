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

import threading
from base import *
import time
import datetime

from dialogs.gensec.operations import classOperations
from dialogs.gensec.priview import classPriview
from dialogs.gensec.process import eslWin,irraWin,ilumWin,lmosWin,oslWin,pauseWin,poslWin,preHeatWin, tlWin

from xmlDriver import loadSLF

class classTableBase(classBase): 
		def __init__(self,title,appIcon,dir=False, parent=None):
			self.Title=str(title)
			if dir:
				title=title+' *'+dir
			else:
				title=title+' *Untitled'
			classBase.__init__(self,title,appIcon)
			self.form1.setCursor(QtCore.Qt.WaitCursor)
			self.fill()
				
			self.comandos=8
			self.grupos=0
			
			self.form1.closeEvent=self.onCloseEvent
			self.header=self.treeWidget.header()
			self.header.setClickable(True)
			
			self.actionSeleccionar_Fila.triggered.connect(self.selectRow)
			
			widget=QtGui.QDesktopWidget()
			mainScreenSize = widget.availableGeometry(widget.primaryScreen())
			H= mainScreenSize.height()-78
			if self.size>11:
				cant=int(H/((self.size*2)))+1
				if self.size<16:
					cant-=2
				elif self.size>47:
					pass
				else:
					cant-=1
			else:
				cant=27
				#cant=int(H/24)
			for group in range(cant):
				self.addGroup()
			
			self.nombre=''
			self.propietario=''
			self.nitrogeno=0
			self.dosis=0
			self.dosisE=0
			self.datecrea=''
			self.protocolo=''
			self.id_lector=QtGui.QApplication.translate('MainWindow','Unknown')
			
			self.processData={}
			self.externalIrradiation=[]
			self.externalIrradiationDefined=[]
			self.inMerge=[]	
			
			self.selected_row=[False,False]
			self.inGroup=[]
			self.colores_in_row={}
			
			if dir:
				self.directorioArchivo=dir
				self.open(True)
	
		
		def fill(self):
			self.treeWidget = QtGui.QTreeWidget()
			self.treeWidget.setAlternatingRowColors(True)
			self.treeWidget.setIndentation(0)
			font = QtGui.QFont()
			font.setFamily("Novason")
			font.setPointSize(12)
			font.setBold(False)
			font.setItalic(False)
			font.setUnderline(False)
			font.setWeight(53)
			font.setStrikeOut(False)
			font.setKerning(False)
			font.setStyleStrategy(QtGui.QFont.PreferDefault)
			self.treeWidget.setFont(font)
			self.treeWidget.setFocusPolicy(QtCore.Qt.ClickFocus)
			self.treeWidget.setAcceptDrops(False)
			self.treeWidget.setFrameShape(QtGui.QFrame.StyledPanel)
			self.treeWidget.setFrameShadow(QtGui.QFrame.Sunken)
			self.treeWidget.setMidLineWidth(0)
			self.treeWidget.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.EditKeyPressed)
			self.treeWidget.setTabKeyNavigation(True)
			self.treeWidget.setProperty("showDropIndicator", False)
			self.treeWidget.setDragDropOverwriteMode(False)
			self.treeWidget.setDragDropMode(QtGui.QAbstractItemView.NoDragDrop)
			self.treeWidget.setDefaultDropAction(QtCore.Qt.MoveAction)				
			self.treeWidget.setAlternatingRowColors(True)
			self.treeWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
			self.treeWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
			self.treeWidget.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
			self.treeWidget.setUniformRowHeights(True)
			self.treeWidget.setAnimated(False)
			self.treeWidget.setAllColumnsShowFocus(False)
			self.treeWidget.setHeaderHidden(False)
			self.treeWidget.setExpandsOnDoubleClick(True)
			self.treeWidget.setObjectName("treeWidget")
			self.treeWidget.headerItem().setText(0, QtGui.QApplication.translate('MainWindow',"Group", None, QtGui.QApplication.UnicodeUTF8))
			self.treeWidget.headerItem().setText(1, QtGui.QApplication.translate('MainWindow',"Sample", None, QtGui.QApplication.UnicodeUTF8))
			H=self.W%117
			num=self.W-H
			coe=0
			if H<55:
				num=num-55
				H+=55
				coe+=1
			cant=int(num/117)-1
			for i in range(cant):
				self.treeWidget.headerItem().setText(i+2, QtGui.QApplication.translate('MainWindow',"Command ")+str(i+1))
			for i in range(2,cant+2):
				self.treeWidget.headerItem().setToolTip(i,QtGui.QApplication.translate('MainWindow','Add Command'))
			self.treeWidget.header().setMovable(False)		
			self.treeWidget.header().setDefaultSectionSize(117)
			self.treeWidget.header().setHighlightSections(True)
			self.treeWidget.header().setMinimumSectionSize(H)		
			self.treeWidget.setColumnWidth(0,H)
			self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
			
			self.fillActions()
		
		def fillActions(self):
			pass		
			
		
		def setIcon(self,status,row,column):
			"""Pone un icono en un item"""
			self.treeWidget.topLevelItem(row).setIcon(column,QtGui.QIcon('pixmaps/icons/status_'+str(status)+'.png'))
				
				
		def quitIcon(self,row,column):
			"""Quita el icono de un item"""
			icon = QtGui.QIcon()
			self.treeWidget.topLevelItem(row).setIcon(column,QtGui.QIcon(icon))
		
		
		def popup(self,pos):
			"""Menu al dar click derecho"""
			pass
			
		@cursorAction()
		def save(self,temp=False):
			"""Guarda la informacion en forma de xml"""
			pass
		
		def cleanGeneralData(self):
			"""Reinicia alos datos generales a vacios"""
			self.nombre=''
			self.propietario=''
			self.nitrogeno=0
			self.dosis=0
			self.dosisE=0
			self.datecrea=''
			self.protocolo=''
			self.id_lector=QtGui.QApplication.translate('MainWindow','Unknown')
			self.directorioArchivo=''
			self.form1.setWindowTitle(self.Title+' *Untitled')

		
		@cursorAction()
		def open(self,dir=False):
			"""Ventana para abrir un documento existente"""
			self.closeAllDialogs()
			if not dir:
				ret=self.question()
				if not ret:
					return False
				elif ret==1 :
					pass
				else:
					if self.save():
						pass
					else:
						return False				
				self.cleanGeneralData()
				self.directorioArchivo=QtGui.QFileDialog.getOpenFileName(
					self.form1,
					QtGui.QApplication.translate('MainWindow',"Open") +" SLF",
					self.fileLocation,
					QtGui.QApplication.translate('MainWindow','File')+' SLF (*.slf)',
					'0',
					QtGui.QFileDialog.DontUseNativeDialog,
				)				
			if self.directorioArchivo:
				try:
					myLoader=loadSLF.classLoader(self.directorioArchivo)
					list=myLoader.exportExtructure()				
					if str(list[1][0][1])!='None':
						self.nombre=list[1][0][1]
					self.STATUS=list[1][1][1]
					self.datecrea=str(list[1][2][1])
					Datemod=list[1][3][1]
					self.propietario=str(list[1][4][1])
					self.NMuestras=list[1][5][1]
					self.id_lector=str(list[1][6][1])
					self.nitrogeno=int(list[1][7][1])
					self.dosis=float(list[1][8][1])
					self.dosisE=float(list[1][9][1])
					if str(list[1][10][1])!='None':
						self.protocolo=str(list[1][9][1])
					self.limpiar()
				except:					
					self.limpiar()
					self.cleanGeneralData()
					self.thereAreCanges=True
					self.error(QtGui.QApplication.translate('MainWindow','Invalid file'))
					return False
				try:					
					tabla=[]
					for seq in list[1][11:]:						
						for sample in seq[1]:							
							tupla=['',[]]
							for process_order in sample[1]:
								#status
								st=process_order[1][0][1]
								#type
								process_order[1][1][1]
								#process_order number
								process_order[2][0][0]
								process_order_id=int(process_order[2][1][0])
								merge=[]
								for process_id in process_order[1][2:]:
									command={}
									command['status']=str(st)
									#param
									for param in process_id[1][0][1]:
										#nombre del parametro
										parametro=str(param[0]).split('\'')[1]
										#valor
										valor=param[1]
										if valor!=None:
											if parametro=='T1':
												parametro='final_temp'
											elif parametro=='dT1':
												parametro='stabilization'
											elif parametro=='tT1':
												parametro='time_final_temp'
											elif parametro=='ExcV':
												parametro='excV'
											elif parametro=='ExcF':
												parametro='excF'
												
											if parametro=='stabilization' or parametro=='excV' or parametro=='excF' or parametro=='final_temp' or parametro=='time_final_temp' or parametro=='heating_rate' or parametro=='time':	
												valor=float(valor)
											elif parametro=='datapoints1' or parametro=='datapoints2' or parametro=='datapoints3' or parametro=='start_optical_power' or parametro=='end_optical_power' or parametro=='number_of_scans' or parametro=='save_temp':	
												valor=int(valor)
											command[parametro]=valor
											
											command['time_unid']='s'

									#inf
									command['date_type']=str(process_id[1][1][1][0][1])
									command['comments']=str(process_id[1][1][1][1][1])
									
									#data
									command['Curva1']=process_id[1][2][1][0][1] if str(process_id[1][2][1][0][1])!='None' else ''
									command['Curva2']=process_id[1][2][1][1][1] if str(process_id[1][2][1][1][1])!='None' else ''
									command['Curva3']=process_id[1][2][1][2][1] if str(process_id[1][2][1][2][1])!='None' else ''
									command['Tiempo1']=process_id[1][2][1][3][1] if str(process_id[1][2][1][3][1])!='None' else ''
									command['Tiempo2']=process_id[1][2][1][4][1] if str(process_id[1][2][1][4][1])!='None' else ''
									
									#process_id id
									process_id[2][0][1]
									command['id']=int(process_id[2][1][1])
									#process_id columna
									process_id[2][0][0]
									command['column']=int(process_id[2][1][0])
									
									command['process_order_id']=process_order_id
									
									if command['id']==1:
										command['source']='Beta'
									if command['id']==0:
										command['source']='External'
									if command['id']==3 or command['id']==4:
										command['channels']=command['datapoints1']+command['datapoints2']+command['datapoints3']
										try:
											command['timePerCanel']=command['time']/command['channels']
										except:
											command['timePerCanel']=0
									if command['id']==4:
										try:
											command['number_scan']=(command['time_final_temp']-command['stabilization'])/command['time']
										except:
											command['number_scan']=0
									if command['id']==5:
										try:
											command['timePerCanel']=command['time']/command['datapoints2']
										except:
											command['timePerCanel']=0
									if command['id']==6:
										#Estos parametros no se de donde salen en el xml
										command['record_ruring']=0
										command['light_co_simult']=0
										try:
											command['timePerCanel']=command['time']/command['datapoints2']
										except:
											command['timePerCanel']=0
									if command['id']==7:
										pass
									
									merge.append(command)	
								tupla[1].append(merge)
							#sample #sample
							sample[2][0][0]
							s=sample[2][1][0]
							
							tupla[0]=s
							tabla.append(tupla)
				except:
					self.error(QtGui.QApplication.translate('MainWindow','The file could not be opened correctly, were recovered only general data.'))
					self.thereAreCanges=True
					return False
				r=0
				ultimaFila=self.treeWidget.topLevelItemCount()-1
				before='#000000'
				affter='#000000'
				for fila in tabla:
					if r>ultimaFila:
						self.addGroup()
					self.setValue(r,1,fila[0])
					for merge in fila[1]:	
						if len(merge)>1:
							process_order_id=0
							inMerge=[]
							color=self.getColor(before,affter)
							before=str(affter)
							affter=str(color)
						for comando in merge:
							if (not self.existe(int(fila[0]))) or (comando['id']==0):
								c=comando['column']
							else:
								c=-1
								i=self.existe(int(fila[0]))-1
								item = self.treeWidget.topLevelItem( i )
								for column in range(self.comandos+1)[2:]:						
									dato=item.text(column)
									if dato=='' and not(column in self.externalIrradiation):
										if len(filter(lambda n: n<int(comando['column'] ), self.externalIrradiation))>0:
											if column>max(filter(lambda n: n<int(comando['column'] ), self.externalIrradiation)):
												c=column
												break
												print c
										else:
											c=column
											break
								if c==-1:
									c=self.comandos+1
							if c>self.comandos:
								self.addComand()
							id=comando['id']
							del comando['column']					
							st=comando['status']							
							if id==0 and r==0:
								self.setValue(r,c,'External Irradiation,'+str(comando['time']*self.dosisE)+' Gy')
								self.externalIrradiation.append(c)
								self.externalIrradiationDefined.append(r)
							elif id==1:
								self.setValue(r,c,'Beta Irradiation,'+str(comando['time'])+' s')
							elif id==2:
								self.setValue(r,c,'TL,'+str(comando['final_temp'])+QtCore.QString.fromUtf8(' °C, ')+str(comando['heating_rate'])+QtCore.QString.fromUtf8(' °C/s'))
							elif id==3:
								self.setValue(r,c,'OSL,'+str(comando['light_source'])+', '+str(comando['start_optical_power'])+' %')
							elif id==4:
								self.setValue(r,c,'POSL,'+str(comando['light_source'])+', '+str(comando['start_optical_power'])+' %')
							elif id==5:
								self.setValue(r,c,'LMOSL,'+str(comando['light_source'])+', '+str(comando['end_optical_power'])+' %')
							elif id==6:
								self.setValue(r,c,'ESL,'+str(comando['excF'])+' KHz, '+str(comando['excV'])+' V')
							elif id==7:
								self.setValue(r,c,'Pre-Heat,'+str(comando['final_temp'])+QtCore.QString.fromUtf8(' °C, ')+str(comando['heating_rate'])+QtCore.QString.fromUtf8(' °C/s'))
							elif id==8:
								self.setValue(r,c,'Ilumination,'+str(comando['light_source'])+', '+str(comando['start_optical_power'])+' %')
							elif id==9:
								self.setValue(r,c,'Pause,'+str(comando['time'])+' s')
							
							if id!=0 or (id==0 and r==0):
								self.processData[str(r)+','+str(c)]=comando	
								self.setIcon(st,r,c)
							
							if len(merge)>1:
								inMerge.append(str(r)+','+str(c))
								parentItem = self.treeWidget.topLevelItem(r)								
								parentItem.setTextColor(c,QtGui.QColor(color))	
								if not process_order_id:
									process_order_id=self.processData[str(r)+','+str(c)]['process_order_id']
								else:
									self.processData[str(r)+','+str(c)]['process_order_id']=process_order_id
								
						if len(merge)>1:
							self.inMerge.append(inMerge)
					r+=1
				
				self.thereAreCanges=False
				self.form1.statusBar().showMessage(QtGui.QApplication.translate('MainWindow',"The document has been opened"))
				self.form1.setWindowTitle(self.Title+' *'+self.directorioArchivo)     
			else:
				self.directorioArchivo=''				
			self.afterOpen()
			
		def afterOpen(self):
			pass
		
		def getColor(self,before,affter):
			"""Devulve un color diferente a los pasados por parametro"""
			if (before==self.col3 and affter==self.col1) or (before==self.col1 and affter==self.col3) :
				return self.col2
			elif (before==self.col3 and affter==self.col2) or (before==self.col2 and affter==self.col3) :
				return self.col1
			elif (before==self.col1 and affter==self.col2) or (before==self.col2 and affter==self.col1):
				return self.col3
			elif (before==self.col3 or before==self.col1) or (affter==self.col3 or affter==self.col1):
				return self.col2
			else:
				return self.col1
		
		@cursorAction()
		def saveAs(self,dir=False):
			"""Ventana para guardar un documanto"""
			pass
			
		
		def ordenar(self):
			"""Ordena por columna las casillas seleccionadas"""
			aux=[]
			aux[:]=self.treeWidget.selectedIndexes()[:]
			for i in range(len(aux)):
				for j in range(len(aux))[i:]:
					if aux[i]>aux[j]:
						temp=aux[i]
						aux[i]=aux[j]
						aux[j]=temp
			return aux
			
		
		def pertenecen_consecutivos(self):
			"""retorna true si las casillas seleccionadas son de la misma fila y estan de manera consecutiva"""
			list=self.ordenar()
			if len(list)==1:
				return False
			try:
				column=list[0].column()
				if column<2:
					return False
			except:
				return False
			row=list[0].row()
			for item in list[1:]:
				if (item.column()!=(column+1)) or (item.row()!=row):
					return False
				column=item.column()
			return True

					
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
			
			
		def selectRow(self):
			"""Selecciona un conjunto de filas, recibe por parametro un estrin de la forma: row,row,row...."""					
			row, ok = QtGui.QInputDialog.getInteger(self.form1, QtGui.QApplication.translate('MainWindow','Row Number'), QtGui.QApplication.translate('MainWindow','Row')+':',0,1)		
			if ok:
				rows=str(row).split(',')
				for rw in rows:
					if str(rw).isdigit():
						row=int(rw)-1
						try:
							item = self.treeWidget.topLevelItem(row)
							item.setSelected(True)
						except:
							pass
			
		
		def generar(self):
			"""Devuelve una estructura de lista donde cada
			elemento es una lista que representa una muestra,
			en la primera pocision tiene la muestra y en la segunda una lista con todos los comandos"""
			pass	
		
		
		def createXML(self):
			"""Genera una estructura xml a partir de los datos entrados por el usuario"""
			pass
		
		
		def buildHtml(self):
			"""Construye una tabla html con estructura igual a la del gensec, con la informacion de esta"""
			pass
		
		
		@cursorAction()
		def imprimir(self,temp=False):
			"""Imprime toda la informacion de la aplicacion"""
			pass	

		
		@cursorAction()		
		def limpiar(self):
			"""Borra toda la informacion en la tabla"""
			for i in range(self.treeWidget.topLevelItemCount()):
				item = self.treeWidget.topLevelItem( i )
				for column in range(self.comandos+1)[1:]:						
						item.setText(column,'')
						item.setTextColor(column,QtGui.QColor('#000000'))
						self.quitIcon(i,column)
			self.inMerge=[]
			self.processData={}
			self.externalIrradiation=[]
			self.externalIrradiationDefined=[]
			
		
		def setValue(self,row,column,valor):
			"""Introduce un valor en determinado campo, column, tiene que ser mayor que 0"""
			if column<1:
				raise ValueError(QtGui.QApplication.translate('MainWindow','The column parameter must be a number greater than 0'))
			item=self.treeWidget.topLevelItem( row )
			if not item.text(column):
				item.setTextColor(column,QtGui.QColor('#000000'))
			item.setText(column,valor)
			if valor=='':
				self.quitIcon(row,column)
			self.thereAreCanges=True
			
		
		def getSamplesList(self,sample):
			allSamples=[]
			partes=str(sample).split(',')
			for parte in partes:
				numeros=parte.split('-')
				if len(numeros)>1:
					rango=range(int(numeros[0]),int(numeros[-1])+1)
					for n in rango:
						allSamples.append(n)
				else:
					allSamples.append(int(numeros[0]))
			return allSamples
					
					
		def existe(self,n):
			for i in range(self.treeWidget.topLevelItemCount()):
				item = self.treeWidget.topLevelItem( i )
				if item.text(1):
					if n in self.getSamplesList(item.text(1)):
						return i+1
			return False
		
		
		def headerAction(self, logicalIndex):
			"""Es quien controla que no se ejecute el metodo addComand desde 
			el primer header"""
			self.form1.statusBar().showMessage("")
			if logicalIndex>1:
				self.addComand()
			
