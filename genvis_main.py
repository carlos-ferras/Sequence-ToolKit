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
import datetime
import time
from functools import partial

from UI import MainWindows_genvis as mainWindows
from UI.style import *
from Dialogs.fontSelect import fontS 
from Dialogs.about_genvis import about

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg  import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

class Lienzo(FigureCanvas):    
    def __init__(self,X,Y, parent=None):
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        self.axes.plot(X, Y);
        self.axes.grid(True)
        #self.axes.set_ylabel('Eje Y')
	#self.axes.set_xlabel('Eje X')
        
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class UI_GenVis(mainWindows.Ui_MainWindow):
	def __init__(self,config,dir=False,parent=None):
		self.form1 =QtGui.QMainWindow()
		self.setupUi(self.form1)
		self.form1.show()
		
		QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		
		self.header=self.treeWidget.header()	
		self.form1.closeEvent=self.onCloseEvent
		self.treeWidget_2.itemClicked.connect(self.chage)
		
		X=[i for i in range(100)]
		Y=[i*i for i in X]
		canvas = Lienzo(X,Y,self.verticalLayoutWidget)	
		ToolBarr = NavigationToolbar(canvas, self.verticalLayoutWidget)		
		ToolBarr.pan()
		for act in ToolBarr.actions():
			toolTip=str(act.toolTip())
			if toolTip=='Configure subplots' or toolTip=='Edit curves line and axes parameters':
				ToolBarr.removeAction(act)		
			elif toolTip=='Reset original view':		
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
				act.setToolTip(QtGui.QApplication.translate("MainWindow", 'Drag'))
				act.setStatusTip(QtGui.QApplication.translate("MainWindow", 'Drag with left mouse, zoom with right'))
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap("pixmaps/icons/transform.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				act.setIcon(icon)
			elif toolTip=='Zoom to rectangle':
				act.setToolTip(QtGui.QApplication.translate("MainWindow", 'Zoom'))
				act.setStatusTip(QtGui.QApplication.translate("MainWindow", 'Zoom the rectangle'))
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap("pixmaps/icons/zoom.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				act.setIcon(icon)
			elif toolTip=='Save the figure':
				act.setToolTip(QtGui.QApplication.translate("MainWindow", 'Save'))
				act.setStatusTip(QtGui.QApplication.translate("MainWindow", 'Save the figure as image'))		
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap("pixmaps/icons/save2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				act.setIcon(icon)
		
		canvas.fig.set_facecolor('#f0f0f0')
		canvas.axes.set_axis_bgcolor('#ffffff')
		ToolBarr.setStyleSheet('background:#f0f0f0;')		
		self.verticalLayout.addWidget(canvas)
		self.verticalLayout.addWidget(ToolBarr)
		
		self.actionAyuda.triggered.connect(self.help)
		self.actionOpacity.triggered.connect(self.setOpacity)
		self.actionDir_defecto.triggered.connect(self.defaultLocation)
		self.actionFuente.triggered.connect(self.font)
		self.actionImprimir.triggered.connect(self.imprimir)
		self.actionDfgfh.triggered.connect(self.salir)
		self.actionAcerda_de.triggered.connect(partial(about,self.form1))
		self.actionCopiar.triggered.connect(self.copy)
		
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
		self.languageTranslator = QtCore.QTranslator()			
		
		self.config=config
		conf=self.config.load()
		if conf:
			self.fuente=conf[0]
			self.size=conf[1]
			self.fileLocation=conf[2]
			if self.fileLocation=='None':
				self.fileLocation=''
			self.opacity=float(conf[3])
			self.lang=conf[7]
			
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
			self.lang=''
		
		#Rows
		item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
		item_0.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
		self.treeWidget.setItemWidget(item_0, 0,QtGui.QWidget())	
		vs=self.treeWidget.verticalScrollBar()
		vs.setValue(vs.maximum())
		
		self.treeWidget.hideColumn(8)
		self.treeWidget.hideColumn(9)
		self.treeWidget.hideColumn(10)
		
		self.form1.statusBar().showMessage(QtGui.QApplication.translate('MainWindow',"Ready"))
		QtGui.QApplication.restoreOverrideCursor()		
		self.assistant= QtCore.QProcess()
		self.treeWidget.customContextMenuRequested.connect(self.popup)
		
		
	def popup(self,pos):
		menu = QtGui.QMenu()
		menu.addAction(self.actionCopiar)
		action = menu.exec_(self.treeWidget.mapToGlobal(pos))	
		
		
	def chage(self,item):
		headerName= str(item.text(0))
		if item.isSelected():
			self.showColumn(headerName)
		else:
			self.hideColumn(headerName)
	
	
	def definedColumnNumber(self,headerName):
		data={'Columna8':8,'Columna9':9,'Columna10':10}
		return data[headerName]
		
		
	def hideColumn(self,headerName):
		column=self.definedColumnNumber(headerName)
		self.treeWidget.hideColumn(column)
		self.treeWidget.header().setDefaultSectionSize(120)
		
		
	def showColumn(self,headerName):
		column=self.definedColumnNumber(headerName)
		self.treeWidget.showColumn(column)
		self.treeWidget.header().setDefaultSectionSize(120)


	def onCloseEvent(self,event):
		self.closeAllDialogs()
		self.config.save(self.fuente,self.size,self.fileLocation,self.opacity,self.lang)
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


	def help(self):
			"""Corre la ayuda de la aplicacion"""
			if (self.assistant.state() != QtCore.QProcess.Running):
				#app = QLibraryInfo.location(QLibraryInfo.BinariesPath) + QDir.separator()
				app ="assistant ";
				args="-collectionFile documentation/asistente.qhc -enableRemoteControl"
				self.assistant.start(str(app)+str(args))
	
	
	def changeLang(self,lang):
			self.lang=lang
			QtGui.QMessageBox.about(self.form1, "GenVis", QtGui.QApplication.translate('MainWindow','To save the changes you must restart'))				
		
	
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
			hora='<table><tr><td> GenVis : '+str(datetime.datetime.fromtimestamp(time.time()))+'</td></tr></td></tr><tr><td> </td></tr></table>'
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
			
			
	def addRow(self):
		"""Adiciona una fila de la tabla"""
		item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
		item_0.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
		self.treeWidget.setItemWidget(item_0, 0,QtGui.QWidget())	
		vs=self.treeWidget.verticalScrollBar()
		vs.setValue(vs.maximum())
			
			
	def addColumn(self):
			"""Adiciona una columna para comandos"""
			self.treeWidget.headerItem().setText(9,'otra')
			self.treeWidget.headerItem().setToolTip(9,'otra')
			hs=self.treeWidget.horizontalScrollBar()
			hs.setValue(hs.maximum())
			
			
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
			
	
	def defaultLocation(self):
			"""Para escoger el directorio por defecto donde se van a guardar los archivos, y de donde seran cargados"""
			self.closeAllDialogs()
			self.fileLocation=QtGui.QFileDialog.getExistingDirectory (self.form1,'', self.fileLocation)
			if not self.fileLocation:
				self.fileLocation=''	
	
	
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
	
	
	def setValue(self,row,column,valor):
		"""Introduce un valor en determinado campo, column, tiene que ser mayor que 0"""
		item=self.treeWidget.topLevelItem( row )
		if not item.text(column):
			item.setTextColor(column,QtGui.QColor('#000000'))
		item.setText(column,valor)
		
		
	def error(self,text):
			"""Muestra una ventana de error"""
			self.closeAllDialogs()
			msgBox = QtGui.QMessageBox(self.form1)
			msgBox.setWindowTitle(QtGui.QApplication.translate('MainWindow','Error'))
			msgBox.setStyleSheet(ERROR_STYLE)
			msgBox.setText(text)
			msgBox.addButton(QtGui.QPushButton(QtGui.QApplication.translate('MainWindow','Accept')), QtGui.QMessageBox.YesRole)
			ret = msgBox.exec_()
		  
   
   