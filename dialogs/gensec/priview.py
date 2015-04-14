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
from ui.gensec import uiPreview

class classPriview(uiPreview.classUiPreview):
	"""Ventana para la vista previa"""
	def __init__(self,parent):
		self.form1 =QtGui.QMainWindow(parent)
		self.setupUi(self.form1)
		self.form1.show()	