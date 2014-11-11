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

from PyQt4 import QtCore, QtGui
from style import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):		
		MainWindow.setObjectName(_fromUtf8("GenVis"))		
		widget=QtGui.QDesktopWidget()
		mainScreenSize = widget.availableGeometry(widget.primaryScreen())
		W= mainScreenSize.width()
		H= mainScreenSize.height()		
		MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,W,H).size()).expandedTo(MainWindow.minimumSizeHint())) 
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(_fromUtf8("pixmaps/genvis.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		MainWindow.setWindowIcon(icon)	
		
		#TreeWidget
		self.treeWidget = QtGui.QTreeWidget()
		self.treeWidget.setAlternatingRowColors(True)
		self.treeWidget.setIndentation(0)
		font = QtGui.QFont()
		font.setFamily(_fromUtf8("Novason"))
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
		self.treeWidget.setStyleSheet(TREEW_STYLE)	
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
		self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
		cant=11
		for i in range(cant):
			self.treeWidget.headerItem().setText(i, _fromUtf8(QtGui.QApplication.translate('MainWindow',"Column ")+str(i)))		
		
		self.treeWidget.header().setMovable(True)		
		self.treeWidget.header().setDefaultSectionSize(120)
		self.treeWidget.header().setHighlightSections(True)
		self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		
		#Para la grafica
		self.verticalLayoutWidget = QtGui.QWidget()
		self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
		self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		
		#derecha de la grafica
		self.edit = QtGui.QTextEdit()
		self.edit.setText(_fromUtf8("verticalLayout"))
		
		#isquierda de la grafica
		self.treeWidget_2 = QtGui.QTreeWidget()
		self.treeWidget_2.setIndentation(0)
		font = QtGui.QFont()
		font.setFamily(_fromUtf8("Novason"))
		font.setPointSize(12)
		font.setBold(False)
		font.setItalic(False)
		font.setUnderline(False)
		font.setWeight(53)
		self.treeWidget_2.setFont(font)
		self.treeWidget_2.setFocusPolicy(QtCore.Qt.ClickFocus)
		self.treeWidget_2.setFrameShape(QtGui.QFrame.StyledPanel)
		self.treeWidget_2.setFrameShadow(QtGui.QFrame.Sunken)
		self.treeWidget_2.setMidLineWidth(0)
		self.treeWidget_2.setEditTriggers(QtGui.QAbstractItemView.SelectedClicked|QtGui.QAbstractItemView.EditKeyPressed)
		self.treeWidget_2.setTabKeyNavigation(True)
		self.treeWidget_2.setStyleSheet(TREEW2_STYLE)
		self.treeWidget_2.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
		self.treeWidget_2.setUniformRowHeights(True)
		self.treeWidget_2.setHeaderHidden(False)
		self.treeWidget_2.setExpandsOnDoubleClick(False)
		self.treeWidget_2.setObjectName(_fromUtf8("treeWidget_2"))
		self.treeWidget_2.headerItem().setText(0, _fromUtf8(QtGui.QApplication.translate('MainWindow',"Columns")))					
		self.treeWidget_2.header().setDefaultSectionSize(117)
		
		item = QtGui.QTreeWidgetItem(self.treeWidget_2)
		item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
		item.setText(0,'Columna8')
		self.treeWidget_2.setItemWidget(item, 0,QtGui.QWidget())
		
		item = QtGui.QTreeWidgetItem(self.treeWidget_2)
		item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
		item.setText(0,'Columna9')
		self.treeWidget_2.setItemWidget(item, 0,QtGui.QWidget())
		
		item = QtGui.QTreeWidgetItem(self.treeWidget_2)
		item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
		item.setText(0,'Columna10')
		self.treeWidget_2.setItemWidget(item, 0,QtGui.QWidget())
		
		
		
		self.mainWidget=QtGui.QWidget()
		MainWindow.setCentralWidget(self.mainWidget)	
		
		self.layout=QtGui.QGridLayout(self.mainWidget)
		self.layout.setRowMinimumHeight(1,220)
		self.layout.setColumnMinimumWidth(1,300)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.layout.addWidget(self.treeWidget, 1, 0, 1, -1)
		self.layout.addWidget(self.edit,2,0,1,1)
		self.layout.addWidget(self.verticalLayoutWidget,2,1,1,1)
		self.layout.addWidget(self.treeWidget_2,2,2,1,1)
		
		
		#Menus---------------------------------------------------------
		self.menubar = QtGui.QMenuBar(MainWindow)
		self.menubar.setStyleSheet(MENU_STYLE)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 805, 23))
		self.menubar.setObjectName(_fromUtf8("menubar"))
		self.menuArchivo = QtGui.QMenu(self.menubar)
		self.menuArchivo.setObjectName(_fromUtf8("menuArchivo"))
		self.menuEditar = QtGui.QMenu(self.menubar)
		self.menuEditar.setObjectName(_fromUtf8("menuEditar"))
		self.menuOpciones = QtGui.QMenu(self.menubar)
		self.menuOpciones.setObjectName(_fromUtf8("menuOpciones"))		
		self.menuLanguage = QtGui.QMenu(self.menuOpciones)
		self.menuLanguage.setObjectName(_fromUtf8("menuLanguage"))
		self.menuAyuda = QtGui.QMenu(self.menubar)
		self.menuAyuda.setObjectName(_fromUtf8("menuAyuda"))
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtGui.QStatusBar(MainWindow)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		MainWindow.setStatusBar(self.statusbar)		
		
		#Abrir
		self.actionAbrir = QtGui.QAction(MainWindow)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(_fromUtf8("pixmaps/icons/open.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.actionAbrir.setIconVisibleInMenu(True)
		self.actionAbrir.setIcon(icon)
		self.actionAbrir.setShortcut("Ctrl+O")
		self.actionAbrir.setStatusTip(QtGui.QApplication.translate("MainWindow", "Open an existing file", None, QtGui.QApplication.UnicodeUTF8))
		self.actionAbrir.setObjectName(_fromUtf8("actionAbrir"))
		#Copiar
		self.actionCopiar = QtGui.QAction(MainWindow)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(_fromUtf8("pixmaps/icons/copy.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.actionCopiar.setIconVisibleInMenu(True)
		self.actionCopiar.setIcon(icon)
		self.actionCopiar.setShortcut("Ctrl+C")
		self.actionCopiar.setStatusTip(QtGui.QApplication.translate("MainWindow", "Copy the current selection content to the clipboard", None, QtGui.QApplication.UnicodeUTF8))
		self.actionCopiar.setObjectName(_fromUtf8("actionCopiar"))
		#Salir
		self.actionDfgfh = QtGui.QAction(MainWindow)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(_fromUtf8("pixmaps/icons/exit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.actionDfgfh.setIconVisibleInMenu(True)
		self.actionDfgfh.setIcon(icon)
		self.actionDfgfh.setShortcut("Escape")
		self.actionDfgfh.setStatusTip(QtGui.QApplication.translate("MainWindow", "Close the application", None, QtGui.QApplication.UnicodeUTF8))
		self.actionDfgfh.setObjectName(_fromUtf8("actionDfgfh"))
		#Imprimir
		self.actionImprimir = QtGui.QAction(MainWindow)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(_fromUtf8("pixmaps/icons/print.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.actionImprimir.setIconVisibleInMenu(True)
		self.actionImprimir.setIcon(icon)
		self.actionImprimir.setShortcut("Ctrl+P")
		self.actionImprimir.setStatusTip(QtGui.QApplication.translate("MainWindow", "Print the current table", None, QtGui.QApplication.UnicodeUTF8))
		self.actionImprimir.setObjectName(_fromUtf8("actionImprimir"))
		#Fuente
		self.actionFuente = QtGui.QAction(MainWindow)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(_fromUtf8("pixmaps/icons/font.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.actionFuente.setIconVisibleInMenu(True)
		self.actionFuente.setIcon(icon)
		self.actionFuente.setShortcut("Ctrl+F")
		self.actionFuente.setStatusTip(QtGui.QApplication.translate("MainWindow", "Change the font type and size", None, QtGui.QApplication.UnicodeUTF8))
		self.actionFuente.setObjectName(_fromUtf8("actionFuente"))
		#Directorio por defecto
		self.actionDir_defecto = QtGui.QAction(MainWindow)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(_fromUtf8("pixmaps/icons/default_dir.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.actionDir_defecto.setIconVisibleInMenu(True)
		self.actionDir_defecto.setIcon(icon)
		self.actionDir_defecto.setShortcut("Ctrl+D")
		self.actionDir_defecto.setStatusTip(QtGui.QApplication.translate("MainWindow", "Change the default file location", None, QtGui.QApplication.UnicodeUTF8))
		self.actionDir_defecto.setObjectName(_fromUtf8("actionDir_defecto"))	
		#Opacidad
		self.actionOpacity = QtGui.QAction(MainWindow)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(_fromUtf8("pixmaps/icons/opacity.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.actionOpacity.setIconVisibleInMenu(True)
		self.actionOpacity.setIcon(icon)
		self.actionOpacity.setShortcut("Ctrl+Y")
		self.actionOpacity.setStatusTip(QtGui.QApplication.translate("MainWindow", "Change the opacity of the windows", None, QtGui.QApplication.UnicodeUTF8))
		self.actionOpacity.setObjectName(_fromUtf8("actionOpacity"))
		#Ayuda
		self.actionAyuda = QtGui.QAction(MainWindow)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(_fromUtf8("pixmaps/icons/help.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.actionAyuda.setIconVisibleInMenu(True)
		self.actionAyuda.setIcon(icon)
		self.actionAyuda.setShortcut("F1")
		self.actionAyuda.setStatusTip(QtGui.QApplication.translate("MainWindow", "Open the help of the application", None, QtGui.QApplication.UnicodeUTF8))
		self.actionAyuda.setObjectName(_fromUtf8("actionAyuda"))
		#Acerca de 
		self.actionAcerda_de = QtGui.QAction(MainWindow)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(_fromUtf8("pixmaps/icons/about.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.actionAcerda_de.setIconVisibleInMenu(True)
		self.actionAcerda_de.setIcon(icon)
		self.actionAcerda_de.setShortcut("Ctrl+I")
		self.actionAcerda_de.setStatusTip(QtGui.QApplication.translate("MainWindow", "Show information about the application", None, QtGui.QApplication.UnicodeUTF8))
		self.actionAcerda_de.setObjectName(_fromUtf8("actionAcerda_de"))
		
		self.menuArchivo.addAction(self.actionAbrir)
		self.menuArchivo.addAction(self.actionImprimir)
		self.menuArchivo.addAction(self.actionDfgfh)
		self.menuEditar.addAction(self.actionCopiar)
		self.menuOpciones.addAction(self.menuLanguage.menuAction())
		self.menuOpciones.addAction(self.actionFuente)
		self.menuOpciones.addAction(self.actionDir_defecto)
		self.menuOpciones.addAction(self.actionOpacity)
		self.menuAyuda.addAction(self.actionAyuda)
		self.menuAyuda.addAction(self.actionAcerda_de)
		self.menubar.addAction(self.menuArchivo.menuAction())
		self.menubar.addAction(self.menuEditar.menuAction())
		self.menubar.addAction(self.menuOpciones.menuAction())
		self.menubar.addAction(self.menuAyuda.menuAction())
		self.ToolBar= MainWindow.addToolBar(QtGui.QApplication.translate("MainWindow","Tool bar"))
		self.ToolBar.setStyleSheet(TOOLBUTTON_STYLE)
		self.ToolBar.addAction(self.actionAbrir)
		self.ToolBar.addAction(self.actionImprimir)
		

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle("GenVis")
		__sortingEnabled = self.treeWidget.isSortingEnabled()
		self.treeWidget.setSortingEnabled(False)
		self.treeWidget.setSortingEnabled(__sortingEnabled)
		self.menuArchivo.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
		self.menuEditar.setTitle(QtGui.QApplication.translate("MainWindow", "&Edit", None, QtGui.QApplication.UnicodeUTF8))
		self.menuOpciones.setTitle(QtGui.QApplication.translate("MainWindow", "&Options", None, QtGui.QApplication.UnicodeUTF8))
		self.menuLanguage.setTitle(QtGui.QApplication.translate("MainWindow", "&Select Language", None, QtGui.QApplication.UnicodeUTF8))
		self.menuAyuda.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
		self.actionAbrir.setText(QtGui.QApplication.translate("MainWindow", "&Open", None, QtGui.QApplication.UnicodeUTF8))
		self.actionDfgfh.setText(QtGui.QApplication.translate("MainWindow", "&Exit", None, QtGui.QApplication.UnicodeUTF8))
		self.actionAcerda_de.setText(QtGui.QApplication.translate("MainWindow", "&About", None, QtGui.QApplication.UnicodeUTF8))
		self.actionImprimir.setText(QtGui.QApplication.translate("MainWindow", "Prin&t", None, QtGui.QApplication.UnicodeUTF8))
		self.actionFuente.setText(QtGui.QApplication.translate("MainWindow", "&Font", None, QtGui.QApplication.UnicodeUTF8))
		self.actionAyuda.setText(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
		self.actionDir_defecto.setText(QtGui.QApplication.translate("MainWindow", "&Default Location", None, QtGui.QApplication.UnicodeUTF8))
		self.actionOpacity.setText(QtGui.QApplication.translate("MainWindow", "Window &Opacity", None, QtGui.QApplication.UnicodeUTF8))
		self.actionCopiar.setText(QtGui.QApplication.translate("MainWindow", "&Copy", None, QtGui.QApplication.UnicodeUTF8))
		
		