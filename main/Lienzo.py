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
	
	def __init__(self,X,Y,w,sl,sh,bl,bh,sig,back, parent=None):        
		self.fig = Figure(figsize=(w,8))
		self.allGraphic = self.fig.add_subplot(111,axisbg='#ffffff')	
		
		self.active_back=back
		self.active_sig=sig
		
		self.allGraphic_X=X
		self.allGraphic_Y=Y
			
		self.activeSignal=True
		self.activeBackground=False
		
		self.allGraphic.grid(True)
		self.allGraphic.set_xlabel('Channel',color='b', size = 14)
		
		self.divider = make_axes_locatable(self.allGraphic)
		
		if self.active_sig:
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
		if self.active_back:
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
			if sl==0 and sh==0:
				sl=self.allGraphic_X[:11][0]
				sh=self.allGraphic_X[:11][-1]
			if bl==0 and bh==0:
				bl=self.allGraphic_X[-11:][0]
				bh=self.allGraphic_X[-11:][-1]
			
			self.Signal_X=sl
			self.Signal_Y=False
			self.Background_X=bl
			self.Background_Y=False
		
			self.allGraphic.plot(self.allGraphic_X, self.allGraphic_Y, '-')
			self.allGraphic.set_xlim(min(self.allGraphic_X), max(self.allGraphic_X))
		
			self.onselect(sl,sh)
			self.activeBackground=True
			self.onselect(bl,bh)
			
	
	def fillSignal(self,x,y,typ):
		if self.active_sig:
			self.line1.remove()
			self.line1, = self.Signal.plot([], [], typ,color='blue')
			self.line1.set_data(x, y)
			self.Signal_X=x
			self.Signal_Y=y
			self.Signal.set_xlim(min(x), max(x))			
			self.signal_change.emit(float(min(x)), float(max(x)))
			self.Signal.set_ylim(min(self.allGraphic_Y), max(self.allGraphic_Y))

			self.axvspanSignal.set_alpha(0)			
			if str(type(x))=="<type 'list'>":
				self.axvspanSignal= self.allGraphic.axvspan(x[0], x[-1], facecolor='g', alpha=0.5)
			else:
				self.axvspanSignal=self.allGraphic.axvline(x=x, color='g')
			self.Signal.patch.set_facecolor('#ffffff')
		self.activeSignal=False
		

	def fillBackground(self,x,y,typ):
		if self.active_back:
			self.line2.remove()
			self.line2, = self.Background.plot([], [], typ,color='blue')
			self.line2.set_data(x, y)
			self.Background_X=x
			self.Background_Y=y
			self.Background.set_xlim(min(x), max(x))
			self.background_change.emit(float(min(x)), float(max(x)))
			self.Background.set_ylim(min(self.allGraphic_Y), max(self.allGraphic_Y))
			
			self.axvspanBackground.set_alpha(0)			
			if str(type(x))=="<type 'list'>":
				self.axvspanBackground= self.allGraphic.axvspan(x[0], x[-1], facecolor='#1A297D', alpha=0.5)
			else:
				self.axvspanBackground=self.allGraphic.axvline(x=x, color='#1A297D')
			self.Background.patch.set_facecolor('#ffffff')
		self.activeBackground=False
		
		
	def onselect(self,xmin, xmax):
		if self.activeBackground or self.activeSignal:
			if xmin>=min(self.allGraphic_X) and xmax<=max(self.allGraphic_X):
				indmin, indmax = npy.searchsorted(self.allGraphic_X, (xmin, xmax))
				if indmin>xmin:
					indmin-=1
				if indmin!= indmax:
					x=self.allGraphic_X[indmin:indmax]
					y=self.allGraphic_Y[indmin:indmax]
					
					if self.activeSignal:
						self.fillSignal(x,y,'-')
					if self.activeBackground:
						self.fillBackground(x,y,'-')					
				else:
					x=[self.allGraphic_X[indmin]]
					y=[self.allGraphic_Y[indmin]]
					
					if self.activeSignal:
						self.fillSignal(x,y,'.')
					if self.activeBackground:
						self.fillBackground(x,y,'.')
			
			else:
				#puedo mostrar un mensage de k deve seleccionar una zona valida
				self.activeSignal=False
				self.Signal.patch.set_facecolor('#ffffff')
				self.activeBackground=False	
				self.Background.patch.set_facecolor('#ffffff')
				
			self.fig.canvas.draw()
		
