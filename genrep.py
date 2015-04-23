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


import sys,os
from PyQt4 import QtCore  
from PyQt4 import QtGui 
from main.genrepMain import classGenRep
from config import config
from theme.baseTheme import BASE
from theme.loadTheme import LOAD
if os.path.dirname(sys.argv[0]):
	os.chdir(os.path.dirname(sys.argv[0]))

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	conf=config()
	c=conf.loadGeneral()
	theme=c[5]
	
	COL1,COL2,COL3,COL4,COL5,COL6,COL7,COL8=LOAD(theme)	
	app.setStyleSheet(BASE(COL1,COL2,COL3,COL4,COL5,COL6,COL7,COL8,False))

	locale=''
	if c:	
		locale=c[4]
	if locale=='' or locale=='locale' or locale=='None':	
		locale =unicode(QtCore.QLocale.system().name())
	translator=QtCore.QTranslator()
	translator.load("locale/Sequence_ToolKit_"+locale)
	app.installTranslator(translator)
	
	qtTranslator=QtCore.QTranslator()
	qtTranslator.load("qt_"+ locale,QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath))
	app.installTranslator(qtTranslator)
    
	dirs=[False]
	if len(sys.argv)>1:
		dirs=sys.argv[1:]
	
	windows =[]
	for dir in  dirs:
		w=classGenRep(dir)
		windows.append(w)
	for current_child_window in windows:
             current_child_window.form1.showMaximized()
		
	sys.exit(app.exec_())
	
	