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
from gensec_base import *
from XMLDriver import createSLF


class UI_GenSec(UI_GenSec_Base): 
		def __init__(self,dir=False, parent=None):			
			UI_GenSec_Base.__init__(self,'GenSec','pixmaps/gensec.ico',dir)
			
			if self.gensec_config:
				self.processDefaults=self.gensec_config[3]
			else:
				self.processDefaults=[False,False,False,False,False,False,False,[False,False],False]
			
			self.treeWidget.itemDoubleClicked.connect(self.itemAction)
			self.treeWidget.itemSelectionChanged.connect(self.mergeActive)
			
			self.actionAdicionar_Fila.triggered.connect(self.addGroup)
			self.actionAdicionar_Columna.triggered.connect(self.addComand)
			self.actionLimpiar.triggered.connect(self.limpiarall)
			self.actionDsdsda.triggered.connect(self.previusly)
			self.actionOrder.triggered.connect(self.orderBySample)
			self.actionBorrar.triggered.connect(self.delete)
			self.actionAcerda_de.triggered.connect(partial(about,self.form1,'GenSec',QtGui.QApplication.translate("MainWindow", 'Sequence Generator', None, QtGui.QApplication.UnicodeUTF8),QtGui.QApplication.translate("MainWindow", 'This application generates a xml file with the data used by the LF02 automated luminescence reader to run a measuring sequence.', None, QtGui.QApplication.UnicodeUTF8),'1.0.0',"pixmaps/gensec.ico"))
			self.actionNombre.triggered.connect(self.Nombre)
			self.actionPropietario.triggered.connect(self.Propietario)
			self.actionUso_de_Nitr_geno.triggered.connect(self.Nitrogeno)
			self.actionT_sa_de_Dosis.triggered.connect(self.Dosis)
			self.actionTasa_de_Dosis_Externa.triggered.connect(self.DosisExterna)
			self.actionProtocolo.triggered.connect(self.Protocolo)
			self.actionReaderId.triggered.connect(self.ReaderId)
			self.actionColor1.triggered.connect(partial(self.changeColor,1))
			self.actionColor2.triggered.connect(partial(self.changeColor,2))
			self.actionColor3.triggered.connect(partial(self.changeColor,3))
			self.toolButton_6.triggered.connect(self.merge)
			self.toolButton_7.triggered.connect(self.cancelMerge)
			self.actionReset.triggered.connect(self.reset)
			self.header.sectionClicked.connect(self.headerAction)
			
			self.changeColors()
			
			self.form1.statusBar().showMessage(QtGui.QApplication.translate('MainWindow',"Ready"),2000)
			self.form1.setCursor(QtCore.Qt.ArrowCursor)		
			self.treeWidget.customContextMenuRequested.connect(self.popup)					
		
		def fillActions(self):
			
			self.form1.setCentralWidget(self.treeWidget)
			
			self.actionEjecutar_GenSec.setVisible(False)
			
			#Limpiar---------------------------------------------------
			self.actionLimpiar = QtGui.QAction(self.form1)
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("pixmaps/icons/clear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.actionLimpiar.setIconVisibleInMenu(True)
			self.actionLimpiar.setIcon(icon)
			self.actionLimpiar.setShortcut("Ctrl+Q")
			self.actionLimpiar.setStatusTip(QtGui.QApplication.translate("MainWindow", "Delete all the content of the table", None, QtGui.QApplication.UnicodeUTF8))
			self.menuArchivo.insertAction(self.actionImprimir,self.actionLimpiar)
			self.actionLimpiar.setText(QtGui.QApplication.translate("MainWindow", "&Clear All", None, QtGui.QApplication.UnicodeUTF8))
			#Vista Previa------------------------------------------
			self.actionDsdsda = QtGui.QAction(self.form1)
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("pixmaps/icons/preview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.actionDsdsda.setIconVisibleInMenu(True)
			self.actionDsdsda.setIcon(icon)
			self.actionDsdsda.setShortcut("Ctrl+W")
			self.actionDsdsda.setStatusTip(QtGui.QApplication.translate("MainWindow", "Open a PreView of the xml file", None, QtGui.QApplication.UnicodeUTF8))
			self.menuArchivo.insertAction(self.actionLimpiar,self.actionDsdsda)			
			self.Standar_ToolBar.insertAction(self.actionImprimir,self.actionDsdsda)
			self.actionDsdsda.setText(QtGui.QApplication.translate("MainWindow", "&Preview", None, QtGui.QApplication.UnicodeUTF8))
			
			self.menuEditar.addSeparator()
			#Adicionar Fila-----------------------------------------------------------
			self.actionAdicionar_Fila = QtGui.QAction(self.form1)
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("pixmaps/icons/add_row.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.actionAdicionar_Fila.setIconVisibleInMenu(True)
			self.actionAdicionar_Fila.setIcon(icon)
			self.actionAdicionar_Fila.setShortcut("F9")
			self.actionAdicionar_Fila.setStatusTip(QtGui.QApplication.translate("MainWindow", "Add one row at end of the table", None, QtGui.QApplication.UnicodeUTF8))
			self.menuEditar.addAction(self.actionAdicionar_Fila)
			self.actionAdicionar_Fila.setText(QtGui.QApplication.translate("MainWindow", "Add &Row", None, QtGui.QApplication.UnicodeUTF8))
			#Adicionar Columna----------------------------------------------------
			self.actionAdicionar_Columna = QtGui.QAction(self.form1)
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("pixmaps/icons/add_column.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.actionAdicionar_Columna.setIconVisibleInMenu(True)
			self.actionAdicionar_Columna.setIcon(icon)
			self.actionAdicionar_Columna.setShortcut("F10")
			self.actionAdicionar_Columna.setStatusTip(QtGui.QApplication.translate("MainWindow", "Add one column at end of the table", None, QtGui.QApplication.UnicodeUTF8))
			self.menuEditar.addAction(self.actionAdicionar_Columna)	
			self.actionAdicionar_Columna.setText(QtGui.QApplication.translate("MainWindow", "Add Colu&mn", None, QtGui.QApplication.UnicodeUTF8))
			#Seleccionar Fila-----------------------------------------------------------------
			self.actionSeleccionar_Fila = QtGui.QAction(self.form1)
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("pixmaps/icons/select_row.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.actionSeleccionar_Fila.setIconVisibleInMenu(True)
			self.actionSeleccionar_Fila.setIcon(icon)
			self.actionSeleccionar_Fila.setShortcut("Alt+S")
			self.actionSeleccionar_Fila.setStatusTip(QtGui.QApplication.translate("MainWindow", "Select one row of the table", None, QtGui.QApplication.UnicodeUTF8))
			self.menuEditar.addAction(self.actionSeleccionar_Fila)
			self.actionSeleccionar_Fila.setText(QtGui.QApplication.translate("MainWindow", "&Select Row", None, QtGui.QApplication.UnicodeUTF8))
			self.menuEditar.addSeparator()
			#Order--------------------------------------------------------
			self.actionOrder = QtGui.QAction(self.form1)
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("pixmaps/icons/order.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.actionOrder.setIconVisibleInMenu(True)
			self.actionOrder.setIcon(icon)
			self.actionOrder.setShortcut("Ctrl+T")
			self.actionOrder.setStatusTip(QtGui.QApplication.translate("MainWindow", "Sorts the contents of the table by the number of samples", None, QtGui.QApplication.UnicodeUTF8))
			self.menuEditar.addAction(self.actionOrder)
			self.actionOrder.setText(QtGui.QApplication.translate("MainWindow", "&Order by Sample", None, QtGui.QApplication.UnicodeUTF8))
			#Borrar--------------------------------------------------------
			self.actionBorrar = QtGui.QAction(self.form1)
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("pixmaps/icons/clear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.actionBorrar.setIconVisibleInMenu(True)
			self.actionBorrar.setIcon(icon)
			self.actionBorrar.setShortcut("Delete")
			self.actionBorrar.setStatusTip(QtGui.QApplication.translate("MainWindow", "Delete the content of the selection rows", None, QtGui.QApplication.UnicodeUTF8))
			self.menuEditar.addAction(self.actionBorrar)
			self.actionBorrar.setText(QtGui.QApplication.translate("MainWindow", "Cl&ear Seleccion", None, QtGui.QApplication.UnicodeUTF8))
			
			#Nombre----------------------------------------------------------------------------
			self.actionNombre = QtGui.QAction(self.form1)
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("pixmaps/icons/name.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.actionNombre.setIconVisibleInMenu(True)
			self.actionNombre.setIcon(icon)
			self.actionNombre.setStatusTip(QtGui.QApplication.translate("MainWindow", "Change the sequence's name", None, QtGui.QApplication.UnicodeUTF8))
			#Propietario---------------------------------------------------------------
			self.actionPropietario = QtGui.QAction(self.form1)
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("pixmaps/icons/owner.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.actionPropietario.setIconVisibleInMenu(True)
			self.actionPropietario.setIcon(icon)
			self.actionPropietario.setStatusTip(QtGui.QApplication.translate("MainWindow", "Change the name of the sequence's owner", None, QtGui.QApplication.UnicodeUTF8))
			#Nitrogeno------------------------------------------------------
			self.actionUso_de_Nitr_geno = QtGui.QAction(self.form1)
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("pixmaps/icons/nitrogen.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.actionUso_de_Nitr_geno.setIconVisibleInMenu(True)
			self.actionUso_de_Nitr_geno.setIcon(icon)
			self.actionUso_de_Nitr_geno.setStatusTip(QtGui.QApplication.translate("MainWindow", "Change the use of nitrogen in the sequence", None, QtGui.QApplication.UnicodeUTF8))
			#Tasa de dosis----------------------------------
			self.actionT_sa_de_Dosis = QtGui.QAction(self.form1)
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("pixmaps/icons/dose_rate.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.actionT_sa_de_Dosis.setIconVisibleInMenu(True)
			self.actionT_sa_de_Dosis.setIcon(icon)
			self.actionT_sa_de_Dosis.setStatusTip(QtGui.QApplication.translate("MainWindow", "Change the dose rate of the sequence", None, QtGui.QApplication.UnicodeUTF8))
			#Tasa de dosis externa-------------------------------------------
			self.actionTasa_de_Dosis_Externa = QtGui.QAction(self.form1)
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("pixmaps/icons/ext_dose_rate.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.actionTasa_de_Dosis_Externa.setIconVisibleInMenu(True)
			self.actionTasa_de_Dosis_Externa.setIcon(icon)
			self.actionTasa_de_Dosis_Externa.setStatusTip(QtGui.QApplication.translate("MainWindow", "Change the external dose rate of the sequence", None, QtGui.QApplication.UnicodeUTF8))
			#Protocolo-----------------------------------------------------------
			self.actionProtocolo = QtGui.QAction(self.form1)
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("pixmaps/icons/protocol.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.actionProtocolo.setIconVisibleInMenu(True)
			self.actionProtocolo.setIcon(icon)
			self.actionProtocolo.setStatusTip(QtGui.QApplication.translate("MainWindow", "Change the protocol of the sequence", None, QtGui.QApplication.UnicodeUTF8))
			#Reader_id-----------------------------------------------------------
			self.actionReaderId = QtGui.QAction(self.form1)
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("pixmaps/icons/reader_id.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.actionReaderId.setIconVisibleInMenu(True)
			self.actionReaderId.setIcon(icon)
			self.actionReaderId.setStatusTip(QtGui.QApplication.translate("MainWindow", "Show the sequence's  reader id", None, QtGui.QApplication.UnicodeUTF8))
			self.menuOpciones_de_Secuencia = QtGui.QMenu(self.menuOpciones)
			self.menuOpciones_de_Secuencia.addAction(self.actionNombre)
			self.menuOpciones_de_Secuencia.addAction(self.actionPropietario)
			self.menuOpciones_de_Secuencia.addAction(self.actionUso_de_Nitr_geno)
			self.menuOpciones_de_Secuencia.addAction(self.actionT_sa_de_Dosis)
			self.menuOpciones_de_Secuencia.addAction(self.actionTasa_de_Dosis_Externa)
			self.menuOpciones_de_Secuencia.addAction(self.actionProtocolo)
			self.menuOpciones_de_Secuencia.addAction(self.actionReaderId)
			self.menuOpciones.insertAction(self.menuOpciones_de_GenSec.menuAction(),self.menuOpciones_de_Secuencia.menuAction())
			self.actionNombre.setText(QtGui.QApplication.translate("MainWindow", "&Name", None, QtGui.QApplication.UnicodeUTF8))
			self.actionPropietario.setText(QtGui.QApplication.translate("MainWindow", "&Owner", None, QtGui.QApplication.UnicodeUTF8))
			self.actionUso_de_Nitr_geno.setText(QtGui.QApplication.translate("MainWindow", "Nitrogen &Use", None, QtGui.QApplication.UnicodeUTF8))
			self.actionT_sa_de_Dosis.setText(QtGui.QApplication.translate("MainWindow", "&Dose Rate", None, QtGui.QApplication.UnicodeUTF8))
			self.actionTasa_de_Dosis_Externa.setText(QtGui.QApplication.translate("MainWindow", "&External Dose Rate", None, QtGui.QApplication.UnicodeUTF8))
			self.actionProtocolo.setText(QtGui.QApplication.translate("MainWindow", "&Protocol", None, QtGui.QApplication.UnicodeUTF8))
			self.actionReaderId.setText(QtGui.QApplication.translate("MainWindow", "&Reader ID", None, QtGui.QApplication.UnicodeUTF8))
			self.menuOpciones_de_Secuencia.setTitle(QtGui.QApplication.translate("MainWindow", "&Sequence Options", None, QtGui.QApplication.UnicodeUTF8))
			
			#Color1---------------------------------------------------------
			self.actionColor1= QtGui.QAction(self.form1)
			#Color2---------------------------------------------------------
			self.actionColor2= QtGui.QAction(self.form1)
			#Color3---------------------------------------------------------
			self.actionColor3= QtGui.QAction(self.form1)		
			self.menuColor = QtGui.QMenu(self.menuOpciones_de_GenSec)
			self.menuOpciones_de_GenSec.addAction(self.menuColor.menuAction())	
			self.menuColor.addAction(self.actionColor1)
			self.menuColor.addAction(self.actionColor2)
			self.menuColor.addAction(self.actionColor3)	
			self.menuColor.setTitle(QtGui.QApplication.translate("MainWindow", "&Merge Colors", None, QtGui.QApplication.UnicodeUTF8))
			self.actionColor1.setText(QtGui.QApplication.translate("MainWindow", "Color &1", None, QtGui.QApplication.UnicodeUTF8))
			self.actionColor2.setText(QtGui.QApplication.translate("MainWindow", "Color &2", None, QtGui.QApplication.UnicodeUTF8))
			self.actionColor3.setText(QtGui.QApplication.translate("MainWindow", "Color &3", None, QtGui.QApplication.UnicodeUTF8))		
			
			
			#Merge----------------------------------------------------------------
			self.toolButton_6 = QtGui.QAction(self.form1)
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("pixmaps/icons/merge.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.toolButton_6.setIcon(icon)
			self.toolButton_6.setToolTip(QtGui.QApplication.translate("MainWindow",'Merge', None, QtGui.QApplication.UnicodeUTF8))
			self.toolButton_6.setEnabled(False)
			self.toolButton_6.setStatusTip(QtGui.QApplication.translate("MainWindow", "Merge several commands in the same proces_order", None, QtGui.QApplication.UnicodeUTF8))
			#Destroy Merge----------------------------------------------------------------
			self.toolButton_7 = QtGui.QAction(self.form1)
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("pixmaps/icons/cancel_merge.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.toolButton_7.setIcon(icon)
			self.toolButton_7.setToolTip(QtGui.QApplication.translate("MainWindow",'Split', None, QtGui.QApplication.UnicodeUTF8))
			self.toolButton_7.setEnabled(False)
			self.toolButton_7.setStatusTip(QtGui.QApplication.translate("MainWindow", "Split the selected merges ", None, QtGui.QApplication.UnicodeUTF8))
			#Reset----------------------------------
			self.actionReset = QtGui.QAction(self.form1)
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("pixmaps/icons/reset.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.actionReset.setIconVisibleInMenu(True)
			self.actionReset.setIcon(icon)
			self.actionReset.setShortcut("Ctrl+K")
			self.actionReset.setStatusTip(QtGui.QApplication.translate("MainWindow", "Set all states to 'pend', clean all 'data' tags of all process and restores name, datecreation and reader ID of the sequence.", None, QtGui.QApplication.UnicodeUTF8))
			self.menuOpciones.insertAction(self.actionEjecutar_GenSec,self.actionReset)
			self.menuOpciones.insertSeparator(self.actionEjecutar_GenSec)
			self.actionReset.setText(QtGui.QApplication.translate("MainWindow", "Rese&t", None, QtGui.QApplication.UnicodeUTF8))
			self.Tools_ToolBar.setVisible(True)
			self.Tools_ToolBar.addAction(self.toolButton_6)
			self.Tools_ToolBar.addAction(self.toolButton_7)
			self.Tools_ToolBar.addAction(self.actionReset)

		
		def changeTheme(self,them):
			"""cambia el idioma por defecto de la aplicacion"""
			self.theme=them
			COL1,COL2,COL3,COL4,COL5,COL6,COL7,COL8=LOAD(them)		
			self.form1.setStyleSheet(BASE(COL1,COL2,COL3,COL4,COL5,COL6,COL7,COL8,True))
			
		
		def beforeGenRep(self):
			if not self.isEmpty():
				import commands
				try:
					a=str(commands.getoutput('$HOME'))
					b=a.split('/')
					del b[0]
					c=b[-1].split()
					del b[-1]
					if len(c)>1:
						d=c[0].split(':')
						e=d[0]
					else:
						e=c[0]
					userRoot=''
					for i in b:
						userRoot+='/'+i
					userRoot+='/'+e
					dir=userRoot+'/genSecTmp.slf'
				
				except:
					dir='genSecTmp.slf'
				
				self.saveAs(dir)					
				self.dirToOpen=dir
		
		def isEmpty(self):
			for i in range(self.treeWidget.topLevelItemCount()):
				item = self.treeWidget.topLevelItem( i )
				if item.text(1):
					for column in range(self.comandos+1)[2:]:						
						dato=item.text(column)
						if dato!='':
							return False
			return True
		
		@cursorAction()
		def orderBySample(self,temp=False):
			if not self.isEmpty():
				import commands
				try:
					a=str(commands.getoutput('$HOME'))
					b=a.split('/')
					del b[0]
					c=b[-1].split()
					del b[-1]
					if len(c)>1:
						d=c[0].split(':')
						e=d[0]
					else:
						e=c[0]
					userRoot=''
					for i in b:
						userRoot+='/'+i
					userRoot+='/'+e
					dir=userRoot+'/genSecTmp.slf'
				
				except:
					dir='genSecTmp.slf'
					
				temp=self.directorioArchivo
				self.saveAs(dir)					
				self.new()	
				self.directorioArchivo=dir
				self.open(dir)
				self.directorioArchivo=temp
				os.remove(dir)
			
		
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
		def save(self,temp=False):
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
		def saveAs(self,dir=False):
			"""Ventana para guardar un documanto"""
			self.closeAllDialogs()
			dialog=QtGui.QFileDialog(self.form1)
			if not dir:
				self.directorioArchivo=dialog.getSaveFileName(
					self.form1,
					QtGui.QApplication.translate('MainWindow',"Save"),
					self.fileLocation,
					QtGui.QApplication.translate('MainWindow','File')+' SLF (*.slf *.xml)',
					'0',
					QtGui.QFileDialog.DontUseNativeDialog,
				)
			else:
				self.directorioArchivo=dir
			if self.directorioArchivo:
				self.createXML()
				self.mySEQ.save(str(self.directorioArchivo),True)
				self.thereAreCanges=False
				self.form1.statusBar().showMessage(QtGui.QApplication.translate('MainWindow',"The document has been saved"))
				self.form1.setWindowTitle(self.Title+' *'+self.directorioArchivo)  
				return True
			else:
				self.directorioArchivo=''
				self.form1.setWindowTitle(self.Title+' *Untitled')
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
				if all['id']==1 or all['id']==0:
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
					if self.repetidos():
						self.error(QtGui.QApplication.translate('MainWindow','The irradiation process with external source can not be defined when a sample appears in more than one row.'))
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
		def paste(self,temp=False):
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
											if self.repetidos():
												self.error(QtGui.QApplication.translate('MainWindow','The irradiation process with external source can not be defined when a sample appears in more than one row.'))
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
		def copy(self,temp=False):
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
		def cut(self,temp=False):
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
			
			
		@cursorAction()
		def delete(self,temp=False):
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
							
							if len(self.externalIrradiation)>0:
								info['process_order_id']=int(info['process_order_id'])+len(sorted([j for j in self.externalIrradiation if j<column]))

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
			all=[]
			self.mySEQ=None
			tabla=self.generar()
			self.nmuestras=0
			for row in tabla:
				ran=row[0]
				samples=ran.split(',')				
				for sample in samples:
					if '-' in sample:
						extremos=sample.split('-')
						val1=int(extremos[0])
						val2=int(extremos[-1])
						for val in range(val1,val2+1):
							if not val in all:
								self.nmuestras+=1
								all.append(val)
					elif not int(sample) in all:
						self.nmuestras+=1
						all.append(int(sample))
			
			self.mySEQ=createSLF.SEQ(nmuestras=self.nmuestras,name=self.nombre,owner=self.propietario,n2flow=self.nitrogeno,doserate=self.dosis,extdoserate=self.dosisE,protocol=self.protocolo,reader_id=self.id_lector,datecrea=self.datecrea)
			
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
		def previusly(self,temp=False):
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
							if str(self.processData[str(i)+','+str(column)]['status'])=='running':
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
		def imprimir(self,temp=False):
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
			
		
		def onCloseEvent(self,event):
			"""Se ejecuta al cerrar la aplicacion, pregunta si desa guardar los cambios"""
			if self.dirToOpen!='':
				os.remove(self.dirToOpen)
				self.dirToOpen=''
			ret=self.question()
			if not ret:
				event.ignore()
			elif ret==1 :
				self.closeAllDialogs()
				self.config.saveGeneral(self.fuente,self.size,self.fileLocation,self.opacity,self.lang,self.theme)
				self.config.saveGenSec(self.col1,self.col2,self.col3,self.processDefaults)
				event.accept()
			else:
				if self.save():
					self.closeAllDialogs()
					self.config.saveGeneral(self.fuente,self.size,self.fileLocation,self.opacity,self.lang,self.theme)
					self.config.saveGenSec(self.col1,self.col2,self.col3,self.processDefaults)
					event.accept()
				else:
					event.ignore()
		
		
		def closeRestantDialogs(self):
			"""Cuando se ejecuta se cierran todas las ventanas de Comandos"""
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
			
		
		@seguro(QtGui.QApplication.translate('MainWindow','Are you sure you want to delete all the information?'))	
		def limpiarall(self):
			self.limpiar()
			
		
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
			elif sample=='':
				return True			
			elif sample.isdigit() and int(sample)>0 and int(sample)<24:
				return True
			return False
			
			
		def repetidos(self):
			allSamples=[]
			for i in range(self.treeWidget.topLevelItemCount()):
				item = self.treeWidget.topLevelItem( i )
				if item.text(1):
					if len(list(set(allSamples) & set(self.getSamplesList(item.text(1)))))>0:
						return True
					allSamples+=self.getSamplesList(item.text(1))
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
                                        #try:
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
											if self.externalIrradiation!=[]:
												if not self.existe(n):
													allSamples.append(n)
												else:
													self.error(QtGui.QApplication.translate('MainWindow','Incompatible sample declaration'))
													return False
											else:
												allSamples.append(n)
                                                                                else:
                                                                                        self.error(QtGui.QApplication.translate('MainWindow','There are repeated number in sample sequence'))
                                                                                        return False
                                                                elif str(numeros[0])!='':
                                                                        if not int(numeros[0]) in allSamples:
										if self.externalIrradiation!=[]:
											if not self.existe(int(numeros[0])):
												allSamples.append(int(numeros[0]))
											else:
												self.error(QtGui.QApplication.translate('MainWindow','Incompatible sample declaration'))
												return False
										else:
											allSamples.append(int(numeros[0]))
                                                                        else:
                                                                                self.error(QtGui.QApplication.translate('MainWindow','There are repeated number in sample sequence'))
                                                                                return False				
                                                        self.setValue(row,column,str(sample))
					else:
                                                        self.error(QtGui.QApplication.translate('MainWindow','Samples must have the structure [1-3,4,5]\nonly contains ranges and numbers between 1-24 separated by commas'))
                                        """
					except:
                                               self.error(QtGui.QApplication.translate('MainWindow','Samples must have the structure [1-3,4,5]\nonly contains ranges and numbers between 1-24 separated by commas')) 
					"""
					
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
			self.treeWidget.setItemWidget(item_0, 0,self.toolButtonHeader)	
			self.toolButtonHeader.clicked.connect(self.addGroup)			
			vs=self.treeWidget.verticalScrollBar()
			vs.setValue(vs.maximum())
			self.grupos+=1
			
		def addComand(self):
			"""Adiciona una columna para comandos"""
			self.closeAllDialogs()
			self.treeWidget.headerItem().setText(self.comandos+1, (QtGui.QApplication.translate('MainWindow',"Command ")+str(self.comandos)))
			self.treeWidget.headerItem().setToolTip(self.comandos+1,QtGui.QApplication.translate('MainWindow','Add Command'))
			hs=self.treeWidget.horizontalScrollBar()
			hs.setValue(hs.maximum())			
			self.comandos+=1
