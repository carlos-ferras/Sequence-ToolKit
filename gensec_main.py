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

import os
import re
from PyQt4 import QtCore  
from PyQt4 import QtGui 
import threading
from functools import partial
from UI.style import *
from UI import MainWindows_gensec as mainWindows
import time
import datetime

from Dialogs.operationsWid import operationsWid 
from Dialogs.fontSelect import fontS 
from Dialogs.priview import priview
from Dialogs.about_gensec import about
from Dialogs.process import eslWin,irraWin,ilumWin,lmosWin,oslWin,pauseWin,poslWin,pre_heatWin, tlWin
from GenSecLib import createXML,loadXML

class UI_GenSec(mainWindows.Ui_MainWindow): 
		def __init__(self,config,dir=False, parent=None):
			self.form1 =QtGui.QMainWindow()
			self.setupUi(self.form1)		
			
			self.form1.show()
			self.form1.setCursor(QtCore.Qt.WaitCursor)
				
			self.comandos=8
			self.grupos=0
			
			self.form1.closeEvent=self.onCloseEvent
			self.header=self.treeWidget.header()			
			self.header.setClickable(True)
			self.header.sectionClicked.connect(self.headerAction)
			self.header.setStyleSheet(HEADER)
			self.treeWidget.itemDoubleClicked.connect(self.itemAction)
			self.treeWidget.itemSelectionChanged.connect(self.mergeActive)
			
			self.actionGurdar.triggered.connect(self.save)
			self.actionGurdar_como.triggered.connect(self.saveAs)
			self.actionAbrir.triggered.connect(self.open)
			self.actionNuevo.triggered.connect(self.new)
			self.actionLimpiar.triggered.connect(self.limpiar)
			self.actionDfgfh.triggered.connect(self.salir)			
			self.actionImprimir.triggered.connect(self.imprimir)
			self.actionDsdsda.triggered.connect(self.previusly)
			self.actionAdicionar_Fila.triggered.connect(self.addGroup)
			self.actionAdicionar_Columna.triggered.connect(self.addComand)
			self.actionBorrar.triggered.connect(self.delete)
			self.actionSeleccionar_Fila.triggered.connect(self.selectRow)
			self.actionFuente.triggered.connect(self.font)
			self.actionPegar.triggered.connect(self.paste)
			self.actionCopiar.triggered.connect(self.copy)
			self.actionCortar.triggered.connect(self.cut)
			self.actionAcerda_de.triggered.connect(partial(about,self.form1))
			self.actionNombre.triggered.connect(self.Nombre)
			self.actionPropietario.triggered.connect(self.Propietario)
			self.actionUso_de_Nitr_geno.triggered.connect(self.Nitrogeno)
			self.actionT_sa_de_Dosis.triggered.connect(self.Dosis)
			self.actionTasa_de_Dosis_Externa.triggered.connect(self.DosisExterna)
			self.actionProtocolo.triggered.connect(self.Protocolo)
			self.actionReaderId.triggered.connect(self.ReaderId)
			self.actionEjecutar_Comando.triggered.connect(self.runCommand)
			self.actionAyuda.triggered.connect(self.help)
			self.actionDir_defecto.triggered.connect(self.defaultLocation)
			self.actionOpacity.triggered.connect(self.setOpacity)	
			self.actionColor1.triggered.connect(partial(self.changeColor,1))
			self.actionColor2.triggered.connect(partial(self.changeColor,2))
			self.actionColor3.triggered.connect(partial(self.changeColor,3))
			self.toolButton_6.triggered.connect(self.merge)
			self.toolButton_7.triggered.connect(self.cancelMerge)
			self.actionEjecutar_Analyzer.triggered.connect(self.runAnalyzer)
			
			lang= QtGui.QAction(self.form1)
			lang.setObjectName("lang")
			self.menuLanguage.addAction(lang)
			lang.setText(QtGui.QApplication.translate("MainWindow", 'locale', None, QtGui.QApplication.UnicodeUTF8))
			lang.triggered.connect(partial(self.changeLang, 'locale'))
			lang.setStatusTip(QtGui.QApplication.translate("MainWindow", "Change the language to default language on your PC", None, QtGui.QApplication.UnicodeUTF8))
			lang= QtGui.QAction(self.form1)
			lang.setObjectName("lang")
			self.menuLanguage.addAction(lang)
			lang.setText('en')
			lang.triggered.connect(partial(self.changeLang, 'en'))
			lang.setStatusTip(QtGui.QApplication.translate("MainWindow", "Change the language to ", None, QtGui.QApplication.UnicodeUTF8)+'" en "')
			for filePath in os.listdir('Locale'):
			    fileName  = os.path.basename(filePath)
			    fileMatch = re.match("gensec_([a-z]{2,}).qm", fileName)
			    if fileMatch:
					lang= QtGui.QAction(self.form1)
					lang.setObjectName("lang")
					self.menuLanguage.addAction(lang)
					lang.setText(QtCore.QString.fromUtf8(fileMatch.group(1)))
					lang.triggered.connect(partial(self.changeLang, QtCore.QString.fromUtf8(fileMatch.group(1))))
					lang.setStatusTip(QtGui.QApplication.translate("MainWindow", "Change the language to ", None, QtGui.QApplication.UnicodeUTF8)+ '" '+QtCore.QString.fromUtf8(fileMatch.group(1))+' "')
			
			self.config=config
			conf=self.config.load()
			if conf:
				self.fuente=conf[0]
				self.size=conf[1]
				self.fileLocation=conf[2]
				if self.fileLocation=='None':
					self.fileLocation=''
				self.opacity=float(conf[3])
				self.col1=conf[4]
				self.col2=conf[5]
				self.col3=conf[6]
				self.lang=conf[7]
				self.processDefaults=conf[8]
				
				font = QtGui.QFont()
				font.setFamily(self.fuente)
				font.setPointSize(self.size)
				self.treeWidget.setFont(font)
				
				self.form1.setWindowOpacity(self.opacity)
			else:
				self.fuente='Novason'
				self.size=12
				self.fileLocation=''
				self.opacity=1				
				self.col1='#6695df'
				self.col2='#4e72aa'
				self.col3='#8665df'				
				self.lang=''
				self.processDefaults=[False,False,False,False,False,False,False,[False,False],False]

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
			
			self.changeColors()	
			
			self.directorioArchivo=''
			
			self.nombre=''
			self.propietario=''
			self.nitrogeno=0
			self.dosis=0
			self.dosisE=0
			self.datecrea=''
			self.protocolo=''
			self.id_lector=QtGui.QApplication.translate('MainWindow','Unknown')
			
			self.processData={}			
			self.clipboard=[]
			self.processClipboard=''
			self.externalIrradiation=[]
			self.externalIrradiationDefined=[]
			self.inMerge=[]			
			
			if dir:
				self.directorioArchivo=dir
				self.open(True)
				
			self.thereAreCanges=False
			
			self.form1.showMaximized()
			self.form1.statusBar().showMessage(QtGui.QApplication.translate('MainWindow',"Ready"))
			self.form1.setCursor(QtCore.Qt.ArrowCursor)		
			self.treeWidget.customContextMenuRequested.connect(self.popup)			
			self.actionReset.triggered.connect(self.reset)
			self.assistant= QtCore.QProcess()
			self.process_order_by_sample={}
		
		
		def cursorAction():
			def decorador(fun):
				def interna(*arg):
					arg[0].form1.setCursor(QtCore.Qt.WaitCursor)
					fun(arg[0])
					arg[0].form1.setCursor(QtCore.Qt.ArrowCursor)
				return interna
			return decorador
			
			
		def seguro(msg):
			def decorador(fun):
				def interna(*arg):
					ret = QtGui.QMessageBox.warning(arg[0].form1,QtGui.QApplication.translate('MainWindow','Attention!'),msg,QtGui.QMessageBox.No,QtGui.QMessageBox.Yes)
					if ret==QtGui.QMessageBox.Yes:
						fun(arg[0])
				return interna
			return decorador
			

		def runCommand(self):
			pass
			
		
		@cursorAction()
		@seguro(QtGui.QApplication.translate('MainWindow','Continue with reset?'))		
		def reset(self):
			"""Restaura todos los valores de status a pend, asi como las etiquetas data las pone en vacio, tambien el nombre, fecha de creado y id del lector de la secuencia"""
			self.nombre=''
			self.datecrea=''
			self.id_lector=QtGui.QApplication.translate('MainWindow','Unknown')			
			for data in self.processData.keys():
				self.processData[str(data)]['status']='pend'
				self.processData[str(data)]['Curva1']=''
				self.processData[str(data)]['Curva2']=''
				self.processData[str(data)]['Curva3']=''
				self.processData[str(data)]['Tiempo1']=''
				self.processData[str(data)]['Tiempo2']=''
				pos=data.split(',')
				self.setIcon('pend',int(pos[0]),int(pos[1]))					
			self.thereAreCanges=True
		
		
		def setIcon(self,status,row,column):
			"""Pone un icono en un item"""
			self.treeWidget.topLevelItem(row).setIcon(column,QtGui.QIcon('pixmaps/icons/status_'+str(status)+'.png'))
				
				
		def quitIcon(self,row,column):
			"""Quita el icono de un item"""
			icon = QtGui.QIcon()
			self.treeWidget.topLevelItem(row).setIcon(column,QtGui.QIcon(icon))
		
		
		def popup(self,pos):
			"""Menu al dar click derecho"""
			self.closeAllDialogs()
			x= pos.x()+3
			y= pos.y()
			pos=QtCore.QPoint(x,y)
			menu = QtGui.QMenu()
			menu.addAction(self.actionCopiar)
			menu.addAction(self.actionCortar)
			menu.addAction(self.actionPegar)
			menu.addSeparator()
			
			if self.toolButton_6.isEnabled():
				action = QtGui.QAction(self.form1)
				action.setIconVisibleInMenu(True)
				action.setIcon(self.toolButton_6.icon())
				action.setText(self.toolButton_6.toolTip())
				action.setStatusTip(self.toolButton_6.statusTip())
				action.triggered.connect(self.merge)
				menu.addAction(action)
			if self.toolButton_7.isEnabled():
				action = QtGui.QAction(self.form1)
				action.setIconVisibleInMenu(True)
				action.setIcon(self.toolButton_7.icon())
				action.setText(self.toolButton_7.toolTip())
				action.setStatusTip(self.toolButton_7.statusTip())
				action.triggered.connect(self.cancelMerge)
				menu.addAction(action)

			action = menu.exec_(self.treeWidget.mapToGlobal(pos))			
					

		def runAnalyzer(self):
			"""Ejecuta GenVis"""
			self.closeAllDialogs()
			try:
				QtCore.QProcess.startDetached('python genvis.py')
			except:
				self.error(QtGui.QApplication.translate('MainWindow','Unable to launch GenVis'))
				
				
		def help(self):
			"""Corre la ayuda de la aplicacion"""
			self.closeAllDialogs()			
			if (self.assistant.state() != QtCore.QProcess.Running):
				#app = QLibraryInfo.location(QLibraryInfo.BinariesPath) + QDir.separator()
				app ="assistant ";
				args="-collectionFile documentation/asistente.qhc -enableRemoteControl"
				self.assistant.start(str(app)+str(args))
				
			
		def changeLang(self,lang):
			"""cambia el idioma por defecto de la aplicacion"""
			self.lang=lang
			QtGui.QMessageBox.about(self.form1, "GenSec", QtGui.QApplication.translate('MainWindow','To save the changes you must restart'))
			
			
		def cancelMerge(self):
			"""rompe los grupos formados por las casillas que estan seleccionadas"""
			borrar=[]
			for item in self.treeWidget.selectedIndexes():
				for group in range(len(self.inMerge)):
					for poss in self.inMerge[group]:
						if str(item.row())+','+str(item.column())==poss:
							self.clearGroupMerge(group)							
							if not group in borrar: 
								borrar.insert(0,group)
			self.deleteInMerge(borrar)
			self.toolButton_6.setEnabled(True)
			self.toolButton_7.setEnabled(False)
			self.thereAreCanges=True
		
		
		def changeColor(self,color):
			"""Abre una ventana para cambiar el color que pertenece al numero pasado por parametro"""
			self.closeAllDialogs()
			if color==1:
				QColor=QtGui.QColorDialog.getColor(QtGui.QColor(self.col1),self.form1,"color 1",)
				if QColor.name()!='#000000' and QColor.name()!='#ffffff':
					self.col1=QColor.name()
				else:
					self.error(QtGui.QApplication.translate('MainWindow','Invalid color, the color must be different to black and white'))
			elif color==2:
				QColor=QtGui.QColorDialog.getColor(QtGui.QColor(self.col2),self.form1,"color 1",)
				if QColor.name()!='#000000' and QColor.name()!='#ffffff':
					self.col2=QColor.name()
				else:
					self.error(QtGui.QApplication.translate('MainWindow','Invalid color, the color must be different to black and white'))
			elif color==3:
				QColor=QtGui.QColorDialog.getColor(QtGui.QColor(self.col3),self.form1,"color 1",)
				if QColor.name()!='#000000' and QColor.name()!='#ffffff':	
					self.col3=QColor.name()
				else:
					self.error(QtGui.QApplication.translate('MainWindow','Invalid color, the color must be different to black and white'))
			self.changeColors()
			
			
		def changeColors(self):
			"""Ajusta los colores de los iconos a los colores actuales"""
			icon = QtGui.QIcon()
			pm=QtGui.QPixmap(50,50)
			pm.fill(QtGui.QColor(self.col1))
			icon.addPixmap(pm, QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.actionColor1.setIconVisibleInMenu(True)
			self.actionColor1.setIcon(icon)
			
			pm=QtGui.QPixmap(50,50)
			pm.fill(QtGui.QColor(self.col2))
			icon.addPixmap(pm, QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.actionColor2.setIconVisibleInMenu(True)
			self.actionColor2.setIcon(icon)
			
			pm=QtGui.QPixmap(50,50)
			pm.fill(QtGui.QColor(self.col3))
			icon.addPixmap(pm, QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.actionColor3.setIconVisibleInMenu(True)
			self.actionColor3.setIcon(icon)		
			
			
		def setOpacity(self):
			"""Abre una ventana para cambiar la opacidad de la ventana"""
			self.closeAllDialogs()
			dialog=QtGui.QDialog(self.form1)
			dialog.setGeometry(QtCore.QRect(0, 0, 170, 70));	
			
			horizontalSlider=QtGui.QSlider(dialog)
			horizontalSlider.setGeometry(QtCore.QRect(5,5, 160, 20));
			horizontalSlider.setOrientation(QtCore.Qt.Horizontal);
			horizontalSlider.setMinimum(80)
			horizontalSlider.setValue(self.opacity*100)
			
			def opacity():
				"""Cambia la opacidad de la ventana"""
				self.opacity=horizontalSlider.value()/100.0
				self.form1.setWindowOpacity(self.opacity)
				dialog.close()
				
			def cancel():
				"""Pone la opacidad como estaba anteriormente a la vista previa"""
				self.form1.setWindowOpacity(self.opacity)
				dialog.close()
				
			def preview():
				"""Vista previa de la opacidad que esta modificando el usuario"""
				o=horizontalSlider.value()/100.0
				self.form1.setWindowOpacity(o)
				
			def hide(event):
				"""Ajusta la opacidad de la ventana"""
				self.form1.setWindowOpacity(self.opacity)
			
			button=QtGui.QPushButton(QtGui.QApplication.translate('MainWindow','Aply'),dialog)
			button.setGeometry(QtCore.QRect(108,30, 60, 25));
			button.clicked.connect(opacity)
			
			button2=QtGui.QPushButton(QtGui.QApplication.translate('MainWindow','Cancel'),dialog)
			button2.setGeometry(QtCore.QRect(40,30, 60, 25));
			button2.clicked.connect(cancel)
			
			horizontalSlider.valueChanged.connect(preview)
			horizontalSlider.hideEvent =hide
			
			dialog.exec_()	
			
			
		def defaultLocation(self):
			"""Para escoger el directorio por defecto donde se van a guardar los archivos, y de donde seran cargados"""
			self.closeAllDialogs()
			self.fileLocation=QtGui.QFileDialog.getExistingDirectory (self.form1,'', self.fileLocation)
			if not self.fileLocation:
				self.fileLocation=''
			
			
		def onCloseEvent(self,event):
			"""Se ejecuta al cerrar la aplicacion, pregunta si desa guardar los cambios"""
			ret=self.question()
			if not ret:
				event.ignore()
			elif ret==1 :
				self.closeAllDialogs()
				self.config.save(self.fuente,self.size,self.fileLocation,self.opacity,self.lang,self.col1,self.col2,self.col3,self.processDefaults)
				event.accept()
			else:
				if self.save():
					self.closeAllDialogs()
					self.config.save(self.fuente,self.size,self.fileLocation,self.opacity,self.lang,self.col1,self.col2,self.col3,self.processDefaults)
					event.accept()
				else:
					event.ignore()
		
		
		def question(self):
			"""Ventana para preguntar si se desean guardar los cambios"""
			if self.thereAreCanges==True:
				msgBox = QtGui.QMessageBox(self.form1)
				msgBox.setWindowTitle('GenSec')
				msgBox.setText(QtGui.QApplication.translate('MainWindow','Save changes?'))
				msgBox.addButton(QtGui.QPushButton(QtGui.QApplication.translate('MainWindow','Cancel')), QtGui.QMessageBox.DestructiveRole)
				msgBox.addButton(QtGui.QPushButton(QtGui.QApplication.translate('MainWindow','No')), QtGui.QMessageBox.NoRole)
				msgBox.addButton(QtGui.QPushButton(QtGui.QApplication.translate('MainWindow','Yes')), QtGui.QMessageBox.YesRole)
				ret = msgBox.exec_()
				return ret
			else:
				return 1
		
		
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
		
		
		def new(self):
			"""Borra toda la informacion actual para comenzar desde cero"""
			self.closeAllDialogs()
			ret=self.question()
			if not ret:
				pass
			elif ret==1 :
				self.limpiar()
				self.cleanGeneralData()
			else:
				if self.save():
					self.limpiar()
					self.cleanGeneralData()
			self.form1.statusBar().showMessage(QtGui.QApplication.translate('MainWindow',"Ready"))
		
		
		@cursorAction()
		def save(self):
			"""Guarda la informacion en forma de xml"""
			self.closeAllDialogs()
			if self.directorioArchivo=='':
				return self.saveAs()
			else:
				self.createXML()
				self.thereAreCanges=False
				self.form1.statusBar().showMessage(QtGui.QApplication.translate('MainWindow',"The document has been saved"))
				return self.mySEQ.save(str(self.directorioArchivo),True)
		
		
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
					QtGui.QApplication.translate('MainWindow','File')+' SLF (*.slf)' 
				)				
				
			if self.directorioArchivo:
				try:
					myLoader=loadXML.Loader(self.directorioArchivo)
					list=myLoader.exportExtructure()				
					
					if str(list[1][0][1])!='None':
						self.nombre=list[1][0][1]
					STATUS=list[1][1][1]
					self.datecrea=str(list[1][2][1])
					Datemod=list[1][3][1]
					self.propietario=str(list[1][4][1])
					NMuestras=list[1][5][1]
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
											elif parametro=='datapoints1' or parametro=='datapoints2' or parametro=='datapoints3' or parametro=='start_optical_power' or parametro=='end_optical_power' or parametro=='number_of_scans':	
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
				f=0
				ultimaFila=self.treeWidget.topLevelItemCount()-1

				before='#000000'
				affter='#000000'
				
				for fila in tabla:
					if f>ultimaFila:
						self.addGroup()
					self.setValue(f,1,fila[0])
					for merge in fila[1]:	
						if len(merge)>1:
							process_order_id=0
							inMerge=[]
							color=self.getColor(before,affter)
							before=str(affter)
							affter=str(color)
						
						for comando in merge:
							c=comando['column']
							if c>self.comandos:
								self.addComand()
							id=comando['id']						
							del comando['column']					
							
							st=comando['status']
							self.setIcon(st,f,c)
							
							if id==0 and f==0:
								self.setValue(f,c,'External Irradiation,'+str(comando['time']*self.dosisE)+' Gy')
								self.externalIrradiation.append(c)
								self.externalIrradiationDefined.append(f)
							elif id==1:
								self.setValue(f,c,'Beta Irradiation,'+str(comando['time'])+' s')
							elif id==2:
								self.setValue(f,c,'TL,'+str(comando['final_temp'])+QtCore.QString.fromUtf8(' °C, ')+str(comando['heating_rate'])+QtCore.QString.fromUtf8(' °C/s'))
							elif id==3:
								self.setValue(f,c,'OSL,'+str(comando['light_source'])+', '+str(comando['start_optical_power'])+' %')
							elif id==4:
								self.setValue(f,c,'POSL,'+str(comando['light_source'])+', '+str(comando['start_optical_power'])+' %')
							elif id==5:
								self.setValue(f,c,'LMOSL,'+str(comando['light_source'])+', '+str(comando['end_optical_power'])+' %')
							elif id==6:
								self.setValue(f,c,'ESL,'+str(comando['excF'])+' KHz, '+str(comando['excV'])+' V')
							elif id==7:
								self.setValue(f,c,'Pre-Heat,'+str(comando['final_temp'])+QtCore.QString.fromUtf8(' °C, ')+str(comando['heating_rate'])+QtCore.QString.fromUtf8(' °C/s'))
							elif id==8:
								self.setValue(f,c,'Ilumination,'+str(comando['light_source'])+', '+str(comando['start_optical_power'])+' %')
							elif id==9:
								self.setValue(f,c,'Pause,'+str(comando['time'])+' s')
							
							if id!=0 or (id==0 and f==0):
								self.processData[str(f)+','+str(c)]=comando					
							
							if len(merge)>1:								
								inMerge.append(str(f)+','+str(c))
								parentItem = self.treeWidget.topLevelItem(f)								
								parentItem.setTextColor(c,QtGui.QColor(color))	
								
								if not process_order_id:
									process_order_id=self.processData[str(f)+','+str(c)]['process_order_id']
								else:
									self.processData[str(f)+','+str(c)]['process_order_id']=process_order_id
								
						if len(merge)>1:
							self.inMerge.append(inMerge)
					f+=1
				
				self.thereAreCanges=False
				self.form1.statusBar().showMessage(QtGui.QApplication.translate('MainWindow',"The document has been opened"))
			else:
				self.directorioArchivo=''		
		
		
		@cursorAction()
		def saveAs(self):
			"""Ventana para guardar un documanto"""
			self.closeAllDialogs()
			dialog=QtGui.QFileDialog(self.form1)
			self.directorioArchivo=dialog.getSaveFileName(
				self.form1,
				QtGui.QApplication.translate('MainWindow',"Save"),
				self.fileLocation,
				QtGui.QApplication.translate('MainWindow','File')+' SLF (*.slf);; '+QtGui.QApplication.translate('MainWindow','File')+'XML (*.xml)',
			)	
			if self.directorioArchivo:
				self.createXML()
				self.mySEQ.save(str(self.directorioArchivo),True)
				self.thereAreCanges=False
				self.form1.statusBar().showMessage(QtGui.QApplication.translate('MainWindow',"The document has been saved"))
				return True
			else:
				self.directorioArchivo=''
			return False
			
		
		def deleteInMerge(self,borrar):
			"""Borra un grupo de procesos unidos de la memoria de la aplicacion, se usa luego de la funcion clearGroupMerge"""
			for grupo in borrar:
				try:
					del self.inMerge[grupo]					
				except:
					pass
			self.thereAreCanges=True
					
		
		def clearGroupMerge(self,group):
			"""Desagrupa procesos que se encontraban dentro de un mismo process order"""
			for poss in self.inMerge[group]:
				row=int(poss.split(',')[0])
				column=int(poss.split(',')[1])
				parentItem = self.treeWidget.topLevelItem(row)
				parentItem.setTextColor(column,QtGui.QColor('#000000'))
				try:
					self.processData[poss]['process_order_id']=column-1
					self.processData[poss]['status']='pend'
					self.setIcon('pend',row,column)
				except:
					pass
			self.thereAreCanges=True
			
		
		def merge(self):
			"""Une dos procesos en un mismo process order"""
			for item in self.treeWidget.selectedIndexes():
				try:
					temp=self.processData[str(item.row())+','+str(item.column())]
					id=temp["id"]
					if id in [0,1,9]:
						if id in [0,1]:
							process='Irradiation'
						else:
							process='Pause'
						self.error(QtGui.QApplication.translate('MainWindow','Unable to perform the operation, the process ')+process+QtGui.QApplication.translate('MainWindow',' does not support merging'))
						return False
					else:
						pass
				except:
					self.error(QtGui.QApplication.translate('MainWindow','Command ')+str(item.column()-1)+QtGui.QApplication.translate('MainWindow',' is empty'))
					return False
					
			process_order_id=0
			inMerge=[]
			borrar=[]
			first=True
			color=self.col1
			
			for item in self.treeWidget.selectedIndexes():
				for group in range(len(self.inMerge)):
					for poss in self.inMerge[group]:
						if str(item.row())+','+str(item.column())==poss:
							self.clearGroupMerge(group)							
							if not group in borrar: 
								borrar.insert(0,group)
			self.deleteInMerge(borrar)
			
			for item in self.treeWidget.selectedIndexes():					
				inMerge.append(str(item.row())+','+str(item.column()))
				parentItem = self.treeWidget.topLevelItem(item.row())
				
				if first:
					before='#000000'
					affter='#000000'
					try:
						before=str(parentItem.textColor(item.column()-1).name())
					except:
						pass
					try:
						affter=str(parentItem.textColor(item.column()+len(self.treeWidget.selectedIndexes())).name())					
					except:
						pass
					color=self.getColor(before,affter)
					first=False
				
				parentItem.setTextColor(item.column(),QtGui.QColor(color))				
				
				if not process_order_id:
					process_order_id=self.processData[str(item.row())+','+str(item.column())]['process_order_id']
				else:
					self.processData[str(item.row())+','+str(item.column())]['process_order_id']=process_order_id
					
				self.processData[str(item.row())+','+str(item.column())]['status']='pend'
				self.setIcon('pend',item.row(),item.column())
				
			self.inMerge.append(inMerge)
			self.toolButton_7.setEnabled(True)
			self.thereAreCanges=True
			
		
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
		
		
		def mergeActive(self):
			"""activa el boton merge cuando es posible usarlo, lo desactiva cuando no"""
			if self.pertenecen_consecutivos():
				self.toolButton_6.setEnabled(True)				
			else:
				self.toolButton_6.setEnabled(False)
			
			self.toolButton_7.setEnabled(False)
			for item in self.treeWidget.selectedIndexes():
				for group in range(len(self.inMerge)):
					for poss in self.inMerge[group]:
						if str(item.row())+','+str(item.column())==poss:
							self.toolButton_7.setEnabled(True)
			
			
		def esl(self,campos,row,column):			
			self.closeAllDialogs()
			self.eslWin=eslWin.eslWin(self.form1,campos)
			self.eslWin.pushButton.clicked.connect(partial(self.Data,self.eslWin,row,column))
			
			
		def ilumination(self,campos,row,column):			
			self.closeAllDialogs()
			self.ilumWin=ilumWin.ilumWin(self.form1,campos)
			self.ilumWin.pushButton.clicked.connect(partial(self.Data,self.ilumWin,row,column))			
			
			
		def irradiation(self,campos,row,column,source=False):
			#Si source es true la fuente es externa
			self.closeAllDialogs()
			self.irraWin=irraWin.irraWin(self.form1,source,campos,self.dosis,self.dosisE)
			self.irraWin.pushButton.clicked.connect(partial(self.Data,self.irraWin,row,column))			
			
			
		def lmos(self,campos,row,column):
			self.closeAllDialogs()
			self.lmosWin=lmosWin.lmosWin(self.form1,campos)
			self.lmosWin.pushButton.clicked.connect(partial(self.Data,self.lmosWin,row,column))			
			
			
		def osl(self,campos,row,column):
			self.closeAllDialogs()
			self.oslWin=oslWin.oslWin(self.form1,campos)
			self.oslWin.pushButton.clicked.connect(partial(self.Data,self.oslWin,row,column))			
			
			
		def pause(self,campos,row,column):
			self.closeAllDialogs()
			self.pauseWin=pauseWin.pauseWin(self.form1,campos)
			self.pauseWin.pushButton.clicked.connect(partial(self.Data,self.pauseWin,row,column))			
			
			
		def posl(self,campos,row,column):
			self.closeAllDialogs()
			self.poslWin=poslWin.poslWin(self.form1,campos)
			self.poslWin.pushButton.clicked.connect(partial(self.Data,self.poslWin,row,column))			
			
			
		def preHealt(self,campos,row,column):
			self.closeAllDialogs()
			self.pre_heatWin=pre_heatWin.pre_heatWin(self.form1,campos)
			self.pre_heatWin.pushButton.clicked.connect(partial(self.Data,self.pre_heatWin,row,column))			
			
			
		def tl(self,campos,row,column):
			self.closeAllDialogs()
			self.tlWin=tlWin.tlWin(self.form1,campos)
			self.tlWin.pushButton.clicked.connect(partial(self.Data,self.tlWin,row,column))			
		
		
		def Data(self,process,row,column):
			"""Guarda los datos de los comandos"""
			data,all=process.data()
			if column in self.externalIrradiation:
				if all['id']==1:
					index=self.externalIrradiation.index(column)
					if self.externalIrradiationDefined[index]==row:
						self.delete()
				else:
					self.error(QtGui.QApplication.translate('MainWindow','This column is locked'))
					process.form1.close()
					return False
			if all['id']==0:
				for i in range(self.treeWidget.topLevelItemCount()):
					if i==row:
						continue
					item = self.treeWidget.topLevelItem( i )
					if item.text(column):
						self.error(QtGui.QApplication.translate('MainWindow','The irradiation process with external source must be set to an empty column.'))
						process.form1.close()
						return False
				self.externalIrradiation.append(column)
				self.externalIrradiationDefined.append(row)				
			self.setValue(row,column,data)
			self.setIcon('pend',row,column)
			all['process_order_id']=column-1
			all['status']='pend'
			all['Curva1']=''
			all['Curva2']=''
			all['Curva3']=''
			all['Tiempo1']=''
			all['Tiempo2']=''
			self.processData[str(row)+','+str(column)]=all
			
			if all['id']==2:
				self.processDefaults[0]=all
			elif all['id']==3:
				self.processDefaults[1]=all
			elif all['id']==4:
				self.processDefaults[2]=all
			elif all['id']==5:
				self.processDefaults[3]=all
			elif all['id']==6:
				self.processDefaults[4]=all
			elif all['id']==7:
				self.processDefaults[5]=all
			elif all['id']==8:
				self.processDefaults[6]=all
			elif all['id']==1 or all['id']==0:
				if all['id']==1:
					source=False
				else:
					source=True
				self.processDefaults[7]=[source,all]
			elif all['id']==9:
				self.processDefaults[8]=all			
			
			process.form1.close()
			self.thereAreCanges=True
			
		def Nombre(self):
			self.closeAllDialogs()
			nombre, ok = QtGui.QInputDialog.getText(self.form1,QtGui.QApplication.translate('MainWindow','Name'),QtGui.QApplication.translate('MainWindow','Name')+':',QtGui.QLineEdit.Normal,self.nombre)
			if ok:
				if str(nombre).isalpha() or str(nombre)=='':
					try:
						self.nombre=str(nombre)
						self.thereAreCanges=True
					except:
						pass
				else:
					self.error(QtGui.QApplication.translate('MainWindow','The Name field should contain only text'))
					
						
		def Propietario(self):
			self.closeAllDialogs()
			propietario, ok = QtGui.QInputDialog.getText(self.form1, QtGui.QApplication.translate('MainWindow','Owner'), QtGui.QApplication.translate('MainWindow','Owner')+':',QtGui.QLineEdit.Normal,self.propietario)
			if ok:
				if str(propietario).isalpha() or str(propietario)=='':
					try:
						self.propietario=str(propietario)
						self.thereAreCanges=True
					except:
						pass
				else:
					self.error(QtGui.QApplication.translate('MainWindow','The Owner field should contain only text'))
					
						
		def Nitrogeno(self):
			self.closeAllDialogs()
			nitrogeno, ok = QtGui.QInputDialog.getInteger(self.form1, QtGui.QApplication.translate('MainWindow','Nitrogen'), QtGui.QApplication.translate('MainWindow','Nitrogen Use')+':',self.nitrogeno,0,1)			
			if ok:
				try:
					self.nitrogeno=nitrogeno
					self.thereAreCanges=True
				except:
					pass
					
						
		def Dosis(self):
			self.closeAllDialogs()
			dosis, ok = QtGui.QInputDialog.getDouble(self.form1, QtGui.QApplication.translate('MainWindow','Dose Rate'),QtGui.QApplication.translate('MainWindow', 'Dose Rate (Gy/s)')+':',self.dosis,0,999999999,2)			
			if ok:
				try:
					self.dosis=dosis
					self.thereAreCanges=True
				except:
					pass
					
						
		def DosisExterna(self):
			self.closeAllDialogs()
			self.dosisE, ok = QtGui.QInputDialog.getDouble(self.form1, QtGui.QApplication.translate('MainWindow','External Dose Rate'), QtGui.QApplication.translate('MainWindow','External Dose Rate (Gy/s)')+':',self.dosisE,0,999999999,2)			
			if ok:
				try:
					self.dosisE=dosisE
					self.thereAreCanges=True
				except:
					pass
					
						
		def Protocolo(self):
			self.closeAllDialogs()
			protocolo, ok = QtGui.QInputDialog.getText(self.form1, QtGui.QApplication.translate('MainWindow','Protocol'), QtGui.QApplication.translate('MainWindow','Protocol')+':',QtGui.QLineEdit.Normal,self.protocolo)			
			if ok:
				if (str(protocolo).isalpha() and len(str(protocolo))==16) or str(protocolo)=='':
					try:
						self.protocolo=str(protocolo)
						self.thereAreCanges=True
					except:
						pass
				else:
					self.error(QtGui.QApplication.translate('MainWindow','The Protocol field must be a string of 16 characters'))
						
						
		def ReaderId(self):
			"""Muestra en solo lectura el id del lector"""
			self.closeAllDialogs()
			msgBox = QtGui.QMessageBox(self.form1)
			msgBox.setText(QtGui.QApplication.translate('MainWindow','Reader ID')+':                      \n\n'+str(self.id_lector))
			msgBox.addButton(QtGui.QPushButton(QtGui.QApplication.translate('MainWindow','Accept')), QtGui.QMessageBox.YesRole)
			ret = msgBox.exec_()
		
		
		@cursorAction()
		def paste(self):
			"""Pega en todas las casillas seleccionadas el texto k esta en el clipboard"""
			self.form1.statusBar().showMessage("")
			borrar=[]
			if len(self.treeWidget.selectedIndexes())>0:
				item=self.treeWidget.selectedIndexes()[0]
				if item.column():
					if item.column()>1:
						if len(self.clipboard)>0:
							c=item.column()
							f=item.row()
							for element in self.clipboard:
								element[2]['status']='pend'
								c_actual=element[0][1]+c
								f_actual=element[0][0]+f	
								
								ultimaFila=self.treeWidget.topLevelItemCount()-1
								if f_actual>ultimaFila:
									for k in range(f_actual-ultimaFila):
										self.addGroup()								
								if c_actual>self.comandos:
									for k in range(c_actual-self.comandos):
										self.addComand()							
								
								if c_actual in self.externalIrradiation:
									self.error(QtGui.QApplication.translate('MainWindow','Column wiht command')+str(c_actual-1)+QtGui.QApplication.translate('MainWindow',' is locked'))
								else:
									if element[2]['id']==0:
										for i in range(self.treeWidget.topLevelItemCount()):
											if i==f_actual:
												continue
											item2 = self.treeWidget.topLevelItem( i )
											if item2.text(c_actual):
												self.error(QtGui.QApplication.translate('MainWindow','The irradiation process with external source must be set to an empty column.'))
												return False
										self.externalIrradiation.append(c_actual)
										self.externalIrradiationDefined.append(f_actual)
									self.setValue(f_actual,c_actual,element[1])
									self.setIcon(element[2]['status'],f_actual,c_actual)
									self.processData[str(f_actual)+','+str(c_actual)]={}
									
									for key in element[2]:							
										self.processData[str(f_actual)+','+str(c_actual)][key]=element[2][key]
									self.processData[str(f_actual)+','+str(c_actual)]['process_order_id']=c_actual-1
									
									for group in range(len(self.inMerge)):
										for poss in self.inMerge[group]:
											if str(f_actual)+','+str(c_actual)==poss:
												self.clearGroupMerge(group)
												if not group in borrar: 
													borrar.insert(0,group)
					elif item.column()==1:
						self.setValue(item.row(),item.column(),self.processClipboard)
				self.deleteInMerge(borrar)
				self.thereAreCanges=True				
		
		
		def menores(self):
			c=-1
			f=-1
			for item in self.treeWidget.selectedIndexes():
				if c==-1 or c>item.column():
					c=item.column()
				if f==-1 or f>item.row():
					f=item.row()
			return f,c
		
		
		@cursorAction()
		def copy(self):
			"""Copia el texto de la casilla seleccionada en el clipboard"""
			self.form1.statusBar().showMessage("")
			if len(self.treeWidget.selectedIndexes())>0:
				self.clipboard=[]
				for item in self.treeWidget.selectedIndexes():
					if item.column():
						if item.column()>1:
							try:
								menor_f,menor_c=self.menores()
								f=item.row()-menor_f
								c=item.column()-menor_c
								text=self.treeWidget.topLevelItem(item.row()).text(item.column())
								clipboard=[False,False,False]
								clipboard[0]=(f,c)
								clipboard[1]=text								
								clipboard[2]=self.processData[str(item.row())+','+str(item.column())]
								self.clipboard.append(clipboard)
							except:
								pass
						elif item.column()==1:
							self.processClipboard=self.treeWidget.topLevelItem(item.row()).text(item.column())
		
		
		@cursorAction()
		def cut(self):
			"""Corta el texto en la casilla seleccionada en el clipboard"""
			self.form1.statusBar().showMessage("")
			borrar=[]
			if len(self.treeWidget.selectedIndexes())>0:
				self.clipboard=[]
				for item in self.treeWidget.selectedIndexes():
					if item.column():
						if item.column()>1:
							try:
								menor_f,menor_c=self.menores()
								f=item.row()-menor_f
								c=item.column()-menor_c								
								text=self.treeWidget.topLevelItem(item.row()).text(item.column())
								clipboard=[False,False,False]
								clipboard[0]=(f,c)
								clipboard[1]=text
								clipboard[2]=self.processData[str(item.row())+','+str(item.column())]				
								self.clipboard.append(clipboard)														
								for group in range(len(self.inMerge)):
									for poss in self.inMerge[group]:
										if str(item.row())+','+str(item.column())==poss:
											self.clearGroupMerge(group)
											if not group in borrar: 
												borrar.insert(0,group)
								self.deleteInMerge(borrar)
							except:
								pass
						elif item.column()==1:
							self.processClipboard=self.treeWidget.topLevelItem(item.row()).text(item.column())
							self.setValue(item.row(),item.column(),'')
				self.delete()
				self.thereAreCanges=True
				
				
		def font(self):
			"""Crea la ventana para escoger tipo y tamanno de fuente"""
			self.closeAllDialogs()
			try:
				self.fontS.form1.close()
			except:
				pass
			self.fontS=fontS(self.form1,self.fuente,self.size)
			self.fontS.pushButton.clicked.connect(self.change)
			
			
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
			row, ok = QtGui.QInputDialog.getText(self.form1, QtGui.QApplication.translate('MainWindow','Row Number'), QtGui.QApplication.translate('MainWindow','Row')+':')			
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
			
			
		@cursorAction()
		def delete(self):
			"""Borra la informacion en todas las filas seleccionadas"""
			self.form1.statusBar().showMessage("")
			borrar=[]
			for item in self.treeWidget.selectedIndexes():
				if item.column():
					if item.column()>1:
						try:
							del self.processData[str(item.row())+','+str(item.column())]
							self.setValue(item.row(),item.column(),'')
							if item.column() in self.externalIrradiation:
								index=self.externalIrradiation.index(item.column())
								if item.row()==self.externalIrradiationDefined[index]:								
									del self.externalIrradiation[index]
									del self.externalIrradiationDefined[index]
							for group in range(len(self.inMerge)):
								for poss in self.inMerge[group]:
									if str(item.row())+','+str(item.column())==poss:
										self.clearGroupMerge(group)
										if not group in borrar: 
											borrar.insert(0,group)	
										
						except:
							pass
					if item.column()==1:
						self.setValue(item.row(),item.column(),'')
			self.deleteInMerge(borrar)
			self.thereAreCanges=True
									
		
		def generar(self):
			"""Devuelve una estructura de lista donde cada
			elemento es una lista que representa una muestra,
			en la primera pocision tiene la muestra y en la segunda una lista con todos los comandos"""
			muestras=[]
			for i in range(self.treeWidget.topLevelItemCount()):
				item = self.treeWidget.topLevelItem( i )
				if item.text(1):
					muestra=[str(item.text(1)),[]]
					for column in range(self.comandos+1)[2:]:						
						dato=item.text(column)
						if dato!='':
							#texto del header en esa columna
							columna=self.header.model().headerData(column,QtCore.Qt.Horizontal).toString()
							#dato en la casilla
							info=self.processData[str(i)+','+str(column)]
							if info['id']==0:
								info['doserate']=info['time']*self.dosis
							elif info['id']==1:
								info['doserate']=info['time']*self.dosisE
							muestra[1].append(info)
							muestra[1][-1]['column']=column
						elif column in self.externalIrradiation:							
							index=self.externalIrradiation.index(column)							
							info=self.processData[str(self.externalIrradiationDefined[index])+','+str(column)]
							info['doserate']=info['time']*self.dosisE							
							muestra[1].append(info)
							muestra[1][-1]['column']=column							
					if muestra[1]!=[]:
						muestras.append(muestra)
			return muestras		
		
		
		def createXML(self):
			"""Genera una estructura xml a partir de los datos entrados por el usuario"""
			self.mySEQ=None
			tabla=self.generar()
			self.nmuestras=0
			for row in tabla:
				ran=row[0]
				samples=ran.split(',')
				for sample in samples:
					if len(sample)==1:
						self.nmuestras+=1
					elif len(sample)>1:
						val1=int(sample[0])
						val2=int(sample[-1])
						for val in range(val1,val2+1):
							self.nmuestras+=1
			
			self.mySEQ=createXML.SEQ(nmuestras=self.nmuestras,name=self.nombre,owner=self.propietario,n2flow=self.nitrogeno,doserate=self.dosis,extdoserate=self.dosisE,protocol=self.protocolo,reader_id=self.id_lector,datecrea=self.datecrea)
			
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
						commands={}
						Sample_ID=self.mySEQ.createSample(sample_id)				
						for command in item[1]:
							st=command['status']
							group=[]
							try:
								group[:]=commands[command['process_order_id']][1][:]
							except:
								pass
							
							data={}
							data['Curva1']=str(command['Curva1'] )#arreglo
							data['Curva2']=str(command['Curva2'] )#arreglo
							data['Curva3']=str(command['Curva3'] )#arreglo
							data['Tiempo1']=str(command['Tiempo1'] )#int
							data['Tiempo2']=str(command['Tiempo2'] )#int
							
							group.append(self.mySEQ.createProcess(command['id'],command,data,command['column']))
							commands[command['process_order_id']]=[st,group[:]]
							
						for group in commands:
							try:
								last=self.process_order_by_sample[str(sample_id)]
								self.process_order_by_sample[str(sample_id)]=self.process_order_by_sample[str(sample_id)]+1
							except:
								last=1
								self.process_order_by_sample[str(sample_id)]=2
							if commands[group][1][0].getAttribute('id')=='0' or commands[group][1][0].getAttribute('id')=='1':
								typ='irrad'
							elif commands[group][1][0].getAttribute('id')=='9':
								typ='pc'
							else:
								typ='meas'
							st=commands[group][0]
							p=self.mySEQ.createProcessOrder(Sample_ID,last,type=typ,status=st,process=commands[group][1])							
			self.process_order_by_sample={}
				
		
		@cursorAction()
		def previusly(self):
			"""Abre la ventana de vista previa"""
			self.closeAllDialogs()
			try:
				self.priview.form1.close()
			except:
				pass
			self.priview=priview(self.form1)			
			self.createXML()				
			self.priview.textEdit.setText(self.mySEQ.preview())
			self.priview.toolButton.clicked.connect(self.save)
			self.priview.toolButton_2.clicked.connect(self.saveAs)
		
		
		def buildHtml(self):
			"""Construye una tabla html con estructura igual a la del gensec, con la informacion de esta"""
			hora='<table><tr><td> GenSec : '+str(datetime.datetime.fromtimestamp(time.time()))+'</td></tr></td></tr><tr><td> </td></tr></table>'
			general='<table><tr><td>'+QtGui.QApplication.translate('MainWindow','Name')+': </td><td>'+ self.nombre +'</td></tr><tr><td>'+QtGui.QApplication.translate('MainWindow','Owner')+': </td><td>'+ self.propietario +'</td></tr><tr><td>'+QtGui.QApplication.translate('MainWindow','Created')+': </td><td>'+ str(self.datecrea) +'</td></tr><tr><td>'+QtGui.QApplication.translate('MainWindow','Nitrogen Use')+': </td><td>'+ str(self.nitrogeno) +'</td></tr><tr><td>'+QtGui.QApplication.translate('MainWindow','Dose Rate')+': </td><td>'+ str(self.dosis) +'</td></tr><tr><td>'+QtGui.QApplication.translate('MainWindow','External Dose Rate')+': </td><td>'+ str(self.dosisE) +'</td></tr><tr><td>'+QtGui.QApplication.translate('MainWindow','Protocol')+': </td><td>'+ self.protocolo +'</td></tr><tr><td>'+QtGui.QApplication.translate('MainWindow','Reader ID')+': </td><td>'+ self.id_lector +'</td></tr><tr><td> </td><td> </td></tr></table>'
			html=''
			cant_filas=0
			cant_colum=0
			for i in range(self.treeWidget.topLevelItemCount()):
				item = self.treeWidget.topLevelItem( i )
				if item.text(1):
					cant_filas+=1
					colum=0
					html+='<tr>'
					html+='<td>     '+str(cant_filas)+'      </td>'
					html+='<td>     '+str(item.text(1))+'     </td>'
					for column in range(self.comandos+1)[2:]:
						color= item.textColor(column).name()
						font= self.treeWidget.font().family()
						size= str(self.treeWidget.font().pointSize())
						dato=item.text(column)
						text=''
						for c in dato:
							try:
								text+=str(c)
							except:
								text+='°'
						if text!='':
							if str(self.processData[str(i)+','+str(column)]['status'])=='exe':
								color1='red'
							elif str(self.processData[str(i)+','+str(column)]['status'])=='pend':
								color1='#dde000'
							else:
								color1='green'
							icon='<img style="background:'+color1+';" width="10" height="10" src=" "></img>'
						else:
							icon=''
						html+='<td style="font-family:'+font+';font-size:'+size+'; color:'+color+';">' +str(icon)+'     '+text+'     </td>'
						colum+=1
					html+='</tr>'
					if cant_colum<colum:
						cant_colum=colum
			html+="</table></body></html>"
			
			header='<table border="2"><tr><td>     '+QtGui.QApplication.translate('MainWindow','Group')+'     </td><td>     '+QtGui.QApplication.translate('MainWindow','Sample')+'     </td>'
			for i in range(cant_colum):
				header+='<td>     '+str(i+1)+'     </td>'
			header+='</tr>'
			html=hora+general+header+html
			return html
		
		
		@cursorAction()
		def imprimir(self):
			"""Imprime toda la informacion de la aplicacion"""
			self.closeAllDialogs()
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
			
		
		def salir(self):
			"""Cierra la ventana activa, si es La ventana principal, las cierra todas"""
			self.closeAllDialogs()
			self.form1.close()
				
		
		def closeAllDialogs(self):
			"""Cuando se ejecuta se cierran todas las ventanas de Comandos"""
			try:
				self.fontS.form1.close()
			except:
				pass
			try:
				self.priview.form1.close()
			except:
				pass
			try:
				self.oper.form1.close()
			except:
				pass
			try:
				self.eslWin.close()
			except:
				pass
			try:
				self.ilumWin.close()
			except:
				pass
			try:
				self.irraWin.close()
			except:
				pass
			try:
				self.lmosWin.close()
			except:
				pass
			try:
				self.oslWin.close()
			except:
				pass
			try:
				self.pauseWin.close()
			except:
				pass
			try:
				self.poslWin.close()
			except:
				pass
			try:
				self.pre_heatWin.close()
			except:
				pass
			try:
				self.tlWin.close()
			except:
				pass
			
		
		@cursorAction()
		@seguro(QtGui.QApplication.translate('MainWindow','Are you sure you want to delete all the information?'))	
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
			
		
		def validSample(self,sample):
			"""Retorna True si la secuencia entrada es valida para una cadena de muestras"""
			if len(sample)>1:
				if sample[0].isdigit():
                                        num=''
                                        num+=sample[0]
					for i in range(len(sample))[1:]:
						if sample[i].isdigit():
                                                        num+=sample[i]
							if i==len(sample)-1:
                                                                if int(num)>0 and int(num)<25:
                                                                        return True					
						else:
							if sample[i]=='-' or sample[i]==',':
								return self.validSample(sample[i+1:])
							else:
								return False
			else:
				if sample=='' or sample.isdigit():
					if int(sample)>0 and int(sample)<24:
						return True
			return False				
			
		
		def itemAction(self,item,column):
			"""Realiza una accion cuando se da doble click en un elemento de la tabla"""
			self.form1.statusBar().showMessage("")
			row=self.treeWidget.indexFromItem(item).row()
			dato=item.text(column)
			self.closeAllDialogs()
			if column==1:
				sample, ok = QtGui.QInputDialog.getText(self.form1,QtGui.QApplication.translate('MainWindow','Sample'),QtGui.QApplication.translate('MainWindow','Sample')+':',QtGui.QLineEdit.Normal,dato)
				if ok:
                                        try:
                                                if self.validSample(str(sample)):
                                                        
                                                        allSamples=[]
                                                        partes=str(sample).split(',')
                                                        for parte in partes:
                                                                numeros=parte.split('-')
                                                                if len(numeros)>1:
                                                                        actual=0
                                                                        for num in numeros:
                                                                                try:
                                                                                        n=int(num)
                                                                                except:
                                                                                        self.error(QtGui.QApplication.translate('MainWindow','Samples must have the structure [1-3,4,5]\nonly contains ranges and numbers separated by commas'))
                                                                                        return False
                                                                                if n<=actual:
                                                                                        self.error(QtGui.QApplication.translate('MainWindow','samples ranges must be low to high, and should not have repeated elements.'))
                                                                                        return False
                                                                                else:
                                                                                        actual=int(num)
                                                                        rango=range(int(numeros[0]),int(numeros[-1])+1)
                                                                        for n in rango:
                                                                                if not n in allSamples:
                                                                                        allSamples.append(n)
                                                                                else:
                                                                                        self.error(QtGui.QApplication.translate('MainWindow','There are repeated number in sample sequence'))
                                                                                        return False
                                                                elif str(numeros[0])!='':
                                                                        if not int(numeros[0]) in allSamples:
                                                                                allSamples.append(int(numeros[0]))
                                                                        else:
                                                                                self.error(QtGui.QApplication.translate('MainWindow','There are repeated number in the sequence of input samples'))
                                                                                return False				
                                                        self.setValue(row,column,str(sample))
                                                else:
                                                        self.error(QtGui.QApplication.translate('MainWindow','Samples must have the structure [1-3,4,5]\nonly contains ranges and numbers between 1-24 separated by commas'))
                                        except:
                                               self.error(QtGui.QApplication.translate('MainWindow','Samples must have the structure [1-3,4,5]\nonly contains ranges and numbers between 1-24 separated by commas')) 
					
			elif column>1:
				command=dato.split(',')[0]
				try:
					dato=self.processData[str(row)+','+str(column)]
				except:
					dato=False						
				if command=='Pre-Heat':
					self.preHealt(dato,row,column)
				elif command=='TL':
					self.tl(dato,row,column)
				elif command=='OSL':
					self.osl(dato,row,column)
				elif command=='POSL':
					self.posl(dato,row,column)
				elif command=='Pause':
					self.pause(dato,row,column)
				elif command=='LMOSL':
					self.lmos(dato,row,column)
				elif command=='Ilumination':
					self.ilumination(dato,row,column)
				elif command=='Beta Irradiation':
					self.irradiation(dato,row,column,False)
				elif command=='External Irradiation':
					self.irradiation(dato,row,column,True)
				elif command=='ESL':
					self.esl(dato,row,column)
				else:					
					self.oper=operationsWid(self.form1)
					self.oper.pushButton.clicked.connect(partial(self.preHealt,self.processDefaults[5],row,column))
					self.oper.pushButton_2.clicked.connect(partial(self.tl,self.processDefaults[0],row,column))
					self.oper.pushButton_3.clicked.connect(partial(self.osl,self.processDefaults[1],row,column))
					self.oper.pushButton_4.clicked.connect(partial(self.posl,self.processDefaults[2],row,column))
					self.oper.pushButton_5.clicked.connect(partial(self.pause,self.processDefaults[8],row,column))
					self.oper.pushButton_7.clicked.connect(partial(self.lmos,self.processDefaults[3],row,column))
					self.oper.pushButton_8.clicked.connect(partial(self.ilumination,self.processDefaults[6],row,column))
					self.oper.pushButton_9.clicked.connect(partial(self.irradiation,self.processDefaults[7][1],row,column,self.processDefaults[7][0]))
					self.oper.pushButton_10.clicked.connect(partial(self.esl,self.processDefaults[4],row,column))
					
				

		def headerAction(self, logicalIndex):
			"""Es quien controla que no se ejecute el metodo addComand desde 
			el primer header"""
			self.form1.statusBar().showMessage("")
			if logicalIndex>1:
				self.addComand()
			
		
		def addComand(self):
			"""Adiciona una columna para comandos"""
			self.closeAllDialogs()
			self.treeWidget.headerItem().setText(self.comandos+1, (QtGui.QApplication.translate('MainWindow',"Command ")+str(self.comandos)))
			self.treeWidget.headerItem().setToolTip(self.comandos+1,QtGui.QApplication.translate('MainWindow','Add Command'))
			hs=self.treeWidget.horizontalScrollBar()
			hs.setValue(hs.maximum())			
			self.comandos+=1
		
		
		def addGroup(self):
			"""Adiciona una fila para otra muestra"""
			self.closeAllDialogs()
			self.form1.statusBar().showMessage("")
			item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
			item_0.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
			self.toolButtonHeader = QtGui.QToolButton()
			self.toolButtonHeader.setText(QtGui.QApplication.translate("MainWindow", str(self.grupos+1), None, QtGui.QApplication.UnicodeUTF8))
			self.toolButtonHeader.setToolTip(QtGui.QApplication.translate("MainWindow",'Add Group', None, QtGui.QApplication.UnicodeUTF8))
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
			self.toolButtonHeader.clicked.connect(self.addGroup)			
			vs=self.treeWidget.verticalScrollBar()
			vs.setValue(vs.maximum())
			self.grupos+=1
			
		
		def error(self,text):
			"""Muestra una ventana de error"""
			self.closeAllDialogs()
			msgBox = QtGui.QMessageBox(self.form1)
			msgBox.setWindowTitle(QtGui.QApplication.translate('MainWindow','Error'))
			msgBox.setStyleSheet(ERROR_STYLE)
			msgBox.setText(text)
			msgBox.addButton(QtGui.QPushButton(QtGui.QApplication.translate('MainWindow','Accept')), QtGui.QMessageBox.YesRole)
			ret = msgBox.exec_()
	
	
