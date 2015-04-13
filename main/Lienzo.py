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

from PyQt4 import QtGui ,QtCore

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg  import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.ticker import MultipleLocator
import numpy as npy
from matplotlib.widgets import SpanSelector
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt


class Lienzo(FigureCanvas):
	signal_change = QtCore.pyqtSignal(float,float)
	background_change = QtCore.pyqtSignal(float,float)
	
	def __init__(self,X,Y,w,sl,sh,bl,bh,default,sig,back,h_min,h_max,h_great_unit,h_small_unit,v_min,v_max,v_great_unit,v_small_unit,fondo,auto, parent=None):        
		self.fig = Figure(figsize=(w,8))
		#self.fig.subplots_adjust(left=0, right=0.8)
		self.fig.subplots_adjust(bottom=0.2)
		
		self.h_min=h_min
		self.h_max=h_max
		self.h_great_unit=h_great_unit
		self.h_small_unit=h_small_unit
		self.v_min=v_min
		self.v_max=v_max
		self.v_great_unit=v_great_unit
		self.v_small_unit=v_small_unit
		self.fondo=fondo
		self.font_color='black'
		
		self.allGraphic = self.fig.add_subplot(111,axisbg=self.fondo[1])	
		
		self.active_back=back
		self.active_sig=sig
		
		self.allGraphic_X=X
		self.allGraphic_Y=Y

		self.activeSignal=True
		self.activeBackground=False
	
		self.allGraphic.set_xlabel('Channel',color=self.font_color, size = 14)		
		self.allGraphic.set_xlim(0,10)
		
		self.allGraphic.spines['left'].set_color(self.font_color)
		self.allGraphic.spines['right'].set_color(self.font_color)
		self.allGraphic.spines['top'].set_color(self.font_color)
		self.allGraphic.spines['bottom'].set_color(self.font_color)
		self.allGraphic.tick_params(axis='x', colors=self.font_color)
		
		self.allGraphic.grid(True)
		self.allGraphic.xaxis.grid(True,'minor',linewidth=1)
		self.allGraphic.xaxis.grid(True,'major',linewidth=2)
		try:
			self.allGraphic.xaxis.set_major_locator(MultipleLocator(self.h_great_unit))
			self.allGraphic.xaxis.set_minor_locator(MultipleLocator(self.h_small_unit))
		except:
			pass
		self.allGraphic.yaxis.grid(True,'minor',linewidth=1)
		self.allGraphic.yaxis.grid(True,'major',linewidth=2)
		try:
			self.allGraphic.yaxis.set_major_locator(MultipleLocator(self.v_great_unit))
			self.allGraphic.yaxis.set_minor_locator(MultipleLocator(self.v_small_unit))
		except:
			pass
		
		self.divider = make_axes_locatable(self.allGraphic)
		
		if self.active_sig:
			self.Signal = self.divider.append_axes("left", 1.4, pad=0.4, sharey=self.allGraphic)
			self.line1, = self.Signal.plot([], [], '-',color=self.font_color)
			self.Signal.set_title('Signal(SG)',color='g',position=(0.5,1.05))
			self.allGraphic.grid(True)
			self.Signal.yaxis.grid(True,'minor',linewidth=1)
			self.Signal.yaxis.grid(True,'major',linewidth=2)
			try:
				self.Signal.yaxis.set_major_locator(MultipleLocator(self.v_great_unit))
				self.Signal.yaxis.set_minor_locator(MultipleLocator(self.v_small_unit))
			except:
				pass	
			#*********************************
			self.Signal.xaxis.grid(True,'minor',linewidth=1)
			self.Signal.xaxis.grid(True,'major',linewidth=2)
			try:
				self.Signal.xaxis.set_major_locator(MultipleLocator(self.h_great_unit))
				self.Signal.xaxis.set_minor_locator(MultipleLocator(self.h_small_unit))
			except:
				pass
			#************************************		
			self.Signal.text(
				-0.5,
				0.15, 
				'Count',
				rotation='vertical',
				color=self.font_color,
				size = 14,
				transform=self.Signal.transAxes)
			plt.setp(self.allGraphic.get_yticklabels(),visible=False)
			self.Signal.patch.set_facecolor(self.fondo[1])
			self.Signal.spines['left'].set_color(self.font_color)
			self.Signal.spines['right'].set_color(self.font_color)
			self.Signal.spines['top'].set_color(self.font_color)
			self.Signal.spines['bottom'].set_color(self.font_color)
			self.Signal.tick_params(axis='y', colors=self.font_color)
			self.Signal.tick_params(axis='x', colors=self.font_color)
			
		if self.active_back:
			self.Background = self.divider.append_axes("right", 1.4, pad=0.4, sharey=self.allGraphic)
			self.line2, = self.Background.plot([], [], '-',color=self.font_color)
			self.Background.set_title('Background(BG)',color='#1A297D',position=(0.5,1.05))
			self.Background.yaxis.grid(True,'minor',linewidth=1)
			self.Background.yaxis.grid(True,'major',linewidth=2)
			try:
				self.Background.yaxis.set_major_locator(MultipleLocator(self.v_great_unit))
				self.Background.yaxis.set_minor_locator(MultipleLocator(self.v_small_unit))
			except:
				pass
			#*********************************
			self.Background.xaxis.grid(True,'minor',linewidth=1)
			self.Background.xaxis.grid(True,'major',linewidth=2)
			try:
				self.Background.xaxis.set_major_locator(MultipleLocator(self.h_great_unit))
				self.Background.xaxis.set_minor_locator(MultipleLocator(self.h_small_unit))
			except:
				pass
			#************************************	
			plt.setp(self.Background.get_yticklabels(),visible=False)
			self.Background.patch.set_facecolor(self.fondo[1])
			self.Background.spines['left'].set_color(self.font_color)
			self.Background.spines['right'].set_color(self.font_color)
			self.Background.spines['top'].set_color(self.font_color)
			self.Background.spines['bottom'].set_color(self.font_color)
			self.Background.tick_params(axis='x', colors=self.font_color)
			 
		self.axvspanSignal= self.allGraphic.axvspan(0, 0, facecolor='g', alpha=0)
		self.axvspanBackground= self.allGraphic.axvspan(0, 0, facecolor='#1A297D', alpha=0)
			 
		plt.setp(self.allGraphic.get_xticklabels(), fontsize=10)#, rotation='vertical')
		if self.active_sig:
			plt.setp(self.Signal.get_yticklabels(), fontsize=10)
			plt.setp(self.Signal.get_xticklabels(), fontsize=10)#, rotation='vertical')
		if self.active_back:
			plt.setp(self.Background.get_xticklabels(), fontsize=10)#, rotation='vertical')
		
		FigureCanvas.__init__(self, self.fig)
		self.setParent(parent)
		FigureCanvas.setSizePolicy(self,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)
		
		if X!=[] and Y!=[]:
			if default and not auto:
				if sl==0 and sh==0:
					sl=self.allGraphic_X[:11][0]
					sh=self.allGraphic_X[:11][-1]
				else:
					if sl<self.allGraphic_X[0]:
						sl=self.allGraphic_X[0]
				if bl==0 and bh==0:
					bl=self.allGraphic_X[-11:][0]
					bh=self.allGraphic_X[-11:][-1]
				else:
					if bl==0:
						bl=self.allGraphic_X[-1]
					else:
						bl=self.allGraphic_X[int(bl)]
					if bh==0:
						bh=self.allGraphic_X[-1]
					else:
						bh=self.allGraphic_X[int(bh)]
				sh=self.allGraphic_X[int(sh)]		
			elif default and auto:
				sl=self.allGraphic_X[self.allGraphic_X.index(sl)]
				sh=self.allGraphic_X[self.allGraphic_X.index(sh)]
				bl=self.allGraphic_X[self.allGraphic_X.index(bl)]
				bh=self.allGraphic_X[self.allGraphic_X.index(bh)]
			
			self.Signal_X=sl
			self.Signal_Y=False
			self.Background_X=bl
			self.Background_Y=False
		
			self.allGraphic.plot(self.allGraphic_X, self.allGraphic_Y, '-')
			
			if self.h_min==-1:
				self.h_min=min(self.allGraphic_X)
			if self.h_max==-1:
				self.h_max=max(self.allGraphic_X)			
			self.allGraphic.set_xlim(self.h_min, self.h_max)
			
			self.onselect(sl,sh)
			self.activeBackground=True
			self.onselect(bl,bh)
	
	def fillSignal(self,x,y,typ,manual=False):
		if self.active_sig:
			self.line1.remove()
			self.line1, = self.Signal.plot([], [], typ,color='blue')
			self.line1.set_data(x, y)
			self.Signal_X=x
			self.Signal_Y=y
			self.Signal.set_xlim(min(x), max(x))	
			if not manual:
				self.signal_change.emit(float(min(x)), float(max(x)))
			
			if self.v_min==-1:
				self.v_min=min(self.allGraphic_Y)
			if self.v_max==-1:
				self.v_max=max(self.allGraphic_Y)			
			self.Signal.set_ylim(self.v_min, self.v_max)

			self.axvspanSignal.set_alpha(0)			
			if str(type(x))=="<type 'list'>":
				self.axvspanSignal= self.allGraphic.axvspan(x[0], x[-1], facecolor='g', alpha=0.5)
			else:
				self.axvspanSignal=self.allGraphic.axvline(x=x, color='g')
			self.Signal.patch.set_facecolor(self.fondo[1])
		self.activeSignal=False
		

	def fillBackground(self,x,y,typ,manual=False):
		if self.active_back:
			self.line2.remove()
			self.line2, = self.Background.plot([], [], typ,color='blue')
			self.line2.set_data(x, y)
			self.Background_X=x
			self.Background_Y=y
			self.Background.set_xlim(min(x), max(x))
			if not manual:
				self.background_change.emit(float(min(x)), float(max(x)))
			
			if self.v_min==-1:
				self.v_min=min(self.allGraphic_Y)
			if self.v_max==-1:
				self.v_max=max(self.allGraphic_Y)			
			self.Background.set_ylim(self.v_min, self.v_max)
			
			self.axvspanBackground.set_alpha(0)			
			if str(type(x))=="<type 'list'>":
				self.axvspanBackground= self.allGraphic.axvspan(x[0], x[-1], facecolor='#1A297D', alpha=0.5)
			else:
				self.axvspanBackground=self.allGraphic.axvline(x=x, color='#1A297D')
			self.Background.patch.set_facecolor(self.fondo[1])
		self.activeBackground=False
		
		
	def onselect(self,xmin, xmax, manual=False):		
		if self.activeBackground or self.activeSignal:			
			if xmin>=min(self.allGraphic_X) and xmax<=max(self.allGraphic_X):
				
				if manual:
					indmin=self.allGraphic_X.index(xmin)
					indmax=self.allGraphic_X.index(xmax)
				else:
					indmin, indmax = npy.searchsorted(self.allGraphic_X, (xmin, xmax))				
					if indmin>xmin:
						indmin-=1
				if indmin!= indmax:
					x=self.allGraphic_X[indmin:indmax+1]
					y=self.allGraphic_Y[indmin:indmax+1]
					
					if self.activeSignal:
						self.fillSignal(x,y,'-',manual)
					if self.activeBackground:
						self.fillBackground(x,y,'-',manual)
				else:
					x=[self.allGraphic_X[indmin]]
					y=[self.allGraphic_Y[indmin]]
					
					if self.activeSignal:
						self.fillSignal(x,y,'.',manual)
					if self.activeBackground:
						self.fillBackground(x,y,'.',manual)			
			else:
				#puedo mostrar un mensage de k deve seleccionar una zona valida
				self.activeSignal=False
				self.Signal.patch.set_facecolor(self.fondo[1])
				self.activeBackground=False	
				self.Background.patch.set_facecolor(self.fondo[1])
				
			self.fig.canvas.draw()
		
