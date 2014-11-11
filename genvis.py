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


import sys
from PyQt4 import QtCore  
from PyQt4 import QtGui 
from genvis_main import UI_GenVis
from config import config

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
    
	conf=config()
	c=conf.load()
	locale=''
	if c:	
		locale=c[7]
	if locale=='' or locale=='locale' or locale=='None':	
		locale =unicode(QtCore.QLocale.system().name())
	translator=QtCore.QTranslator()
	translator.load("Locale/gensec_"+locale)
	app.installTranslator(translator)
	
	qtTranslator=QtCore.QTranslator()
	qtTranslator.load("qt_"+ locale,QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath))
	app.installTranslator(qtTranslator)
    
	dirs=[False]
	if len(sys.argv)>1:
		dirs=sys.argv[1:]
	
	windows =[]
	for dir in  dirs:
		w=UI_GenVis(conf,dir)
		windows.append(w)
	for current_child_window in windows:
             current_child_window
		
	sys.exit(app.exec_())
	
	