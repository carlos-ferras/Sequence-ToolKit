#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#~ Copyright (C) 2014 Carlos Manuel Ferras Hernandez <c4rlos.ferra5@gmail.com>
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

from PyQt4 import QtGui ,QtCore

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg  import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

import numpy as npy
from matplotlib.widgets import SpanSelector
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt


class Lienzo(FigureCanvas):
	signal_change = QtCore.pyqtSignal(float,float)
	background_change = QtCore.pyqtSignal(float,float)
	
	def __init__(self,X,Y,w, parent=None):        
		self.fig = Figure(figsize=(w,4))
		self.allGraphic = self.fig.add_subplot(111,axisbg='#ffffff')	
		
		self.allGraphic_X=X
		self.allGraphic_Y=Y
			
		self.activeSignal=True
		self.activeBackground=False
		
		self.allGraphic.grid(True)
		self.allGraphic.set_xlabel('Channel',color='b', size = 14)
		
		self.divider = make_axes_locatable(self.allGraphic)

		self.Signal = self.divider.append_axes("left", 1.4, pad=0.4, sharey=self.allGraphic)
		self.line1, = self.Signal.plot([], [], '-',color='b')
		self.Signal.set_title('Signal(SG)',color='g',position=(0.5,1.05))
		self.Signal.grid(True)
		self.Signal.text(
			-0.5,
			0.15, 
			'Count',
			rotation='vertical',
			color='b',
			size = 14,
			transform=self.Signal.transAxes)
	
		self.Background = self.divider.append_axes("right", 1.4, pad=0.4, sharey=self.allGraphic)
		self.line2, = self.Background.plot([], [], '-',color='b')
		self.Background.set_title('Background(BG)',color='#1A297D',position=(0.5,1.05))
		self.Background.grid(True)

		plt.setp(self.allGraphic.get_yticklabels() + self.Background.get_yticklabels(),visible=False)
			 
		self.axvspanSignal= self.allGraphic.axvspan(0, 0, facecolor='g', alpha=0)
		self.axvspanBackground= self.allGraphic.axvspan(0, 0, facecolor='#1A297D', alpha=0)
			 
		FigureCanvas.__init__(self, self.fig)
		self.setParent(parent)
		FigureCanvas.setSizePolicy(self,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)
		
		if X!=[] and Y!=[]:			
			self.Signal_X=min(X)
			self.Signal_Y=False
			self.Background_X=max(X)
			self.Background_Y=False
		
			self.allGraphic.plot(self.allGraphic_X, self.allGraphic_Y, '-')
			self.allGraphic.set_xlim(min(self.allGraphic_X), max(self.allGraphic_X))
		
			self.onselect(min(self.allGraphic_X),min(self.allGraphic_X))
			self.activeBackground=True
			self.onselect(max(self.allGraphic_X),max(self.allGraphic_X))
		
	
	def calc_m(self,x1,y1,x2,y2):
		m=float((y2-y1)/(x2-x1))
		return m
	
	def calc_n(self,x,y,m):
		n=float(y-(m*x))
		return n
	
	def function(self,x1,y1,x2,y2):
		m=self.calc_m(x1,y1,x2,y2)
		n=self.calc_n(x1,y1,m)
		return m,n	
	

	def getf(self,typ,xmin,xmax):
		if typ=='min':
			tope=xmin
		else:
			tope=xmax
		try:
			xmenor=sorted([i for i in self.allGraphic_X if i<tope])[-1]
		except:
			xmenor=tope
		try:
			xmayor=sorted([i for i in self.allGraphic_X if i>tope])[0]
		except:
			xmayor=tope
		y_xmenor=self.allGraphic_Y[self.allGraphic_X.index(xmenor)]
		y_xmayor=self.allGraphic_Y[self.allGraphic_X.index(xmayor)]
		m,n=self.function(xmenor,y_xmenor,xmayor,y_xmayor)
		ymin=tope*m+n
		return ymin,xmenor,xmayor	
	
	
	def fillSignal(self,x,y,typ,tope=False):
		self.line1.remove()
		self.line1, = self.Signal.plot([], [], typ,color='blue')
		self.line1.set_data(x, y)
		self.Signal_X=x
		self.Signal_Y=y
		if tope:
			self.Signal.set_xlim(tope[0], tope[-1])
			self.signal_change.emit(float(x), float(x))
		else:
			self.Signal.set_xlim(min(x), max(x))			
			self.signal_change.emit(float(min(x)), float(max(x)))
		self.Signal.set_ylim(min(self.allGraphic_Y), max(self.allGraphic_Y))
		
		self.axvspanSignal.set_alpha(0)			
		if str(type(x))=="<type 'list'>":
			self.axvspanSignal= self.allGraphic.axvspan(x[0], x[-1], facecolor='g', alpha=0.5)
		else:
			self.axvspanSignal=self.allGraphic.axvline(x=x, color='g')
		self.activeSignal=False
		self.Signal.patch.set_facecolor('#ffffff')
		

	def fillBackground(self,x,y,typ,tope=False):
		self.line2.remove()
		self.line2, = self.Background.plot([], [], typ,color='blue')
		self.line2.set_data(x, y)
		self.Background_X=x
		self.Background_Y=y
		if tope:
			self.Background.set_xlim(tope[0], tope[-1])
			self.background_change.emit(float(x), float(x))
		else:
			self.Background.set_xlim(min(x), max(x))
			self.background_change.emit(float(min(x)), float(max(x)))
		self.Background.set_ylim(min(self.allGraphic_Y), max(self.allGraphic_Y))
		
		self.axvspanBackground.set_alpha(0)			
		if str(type(x))=="<type 'list'>":
			self.axvspanBackground= self.allGraphic.axvspan(x[0], x[-1], facecolor='#1A297D', alpha=0.5)
		else:
			self.axvspanBackground=self.allGraphic.axvline(x=x, color='#1A297D')
		self.activeBackground=False
		self.Background.patch.set_facecolor('#ffffff')
		
		
	def onselect(self,xmin, xmax):
		if self.activeBackground or self.activeSignal:
			if xmin>=min(self.allGraphic_X) and xmax<=max(self.allGraphic_X):
				if xmin!= xmax:
					indmin, indmax = npy.searchsorted(self.allGraphic_X, (xmin, xmax))
					indmax = min(len(self.allGraphic_X)-1, indmax)
					
					x=self.allGraphic_X[indmin:indmax]
					y=self.allGraphic_Y[indmin:indmax]
					
					ymin=self.getf('min',xmin,xmax)[0]
					ymax=self.getf('max',xmin,xmax)[0]
					
					x.insert(0,xmin)
					y.insert(0,ymin)
					x.append(xmax)
					y.append(ymax)
					
					if self.activeSignal:
						self.fillSignal(x,y,'-')
					if self.activeBackground:
						self.fillBackground(x,y,'-')
				else:
					ymin,xmenor,xmayor=self.getf('min',xmin,xmax)
					if self.activeSignal:
						self.fillSignal(xmin,ymin,'.',[xmenor,xmayor])
					if self.activeBackground:
						self.fillBackground(xmin,ymin,'.',[xmenor,xmayor])
			
			else:
				#puedo mostrar un mensage de k deve seleccionar una zona valida
				self.activeSignal=False
				self.Signal.patch.set_facecolor('#ffffff')
				self.activeBackground=False	
				self.Background.patch.set_facecolor('#ffffff')
				
			self.fig.canvas.draw()
		
