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

import commands
import os
import pickle

class config:
	
	def __init__(self):
		self.win=False
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
			self.userRoot=''
			for i in b:
				self.userRoot+='/'+i
			self.userRoot+='/'+e
			self.dir=self.userRoot+'/'
		except:
			self.win=True
		if not self.win:
			self.generalconf=self.dir+'.lf02.conf'
			self.gensecconf=self.dir+'.genSec.conf'
			self.genrepconf=self.dir+'.genRep.conf'
		else:
			self.generalconf='lf02.conf'
			self.gensecconf='genSec.conf'
			self.genrepconf='genRep.conf'
			
	
	def loadGeneral(self):
		if os.path.exists(self.generalconf):
			file=open(self.generalconf,'r')
			try:
				config=['Novason',12,'',1,'']
				while True:
					line =file.readline()
					if not line:
						break
					if not line.find('Font '):
						config[0]=str(line.split("[")[1].split("]")[0])
					elif not line.find('Size '):
						try:
							config[1]=int(line.split("[")[1].split("]")[0])
						except:
							pass
					elif not line.find('File Location '):
						config[2] =str(line.split("[")[1].split("]")[0])
					elif not line.find('Opacity '):
						try:
							config[3]=float(line.split("[")[1].split("]")[0])
						except:
							pass
					elif not line.find('Lang '):
						config[4] =str(line.split("[")[1].split("]")[0])
				return config
			except:
				return False
			file.close()
		return False
	
	
	def saveGeneral(self,fuente,size,fileLocation,opacity,lang):
		file=open(self.generalconf,'w+').close()
		file=open(self.generalconf,'w+')
		file.write("Font ["+str(fuente)+"]\n"+"Size ["+str(size)+"]\n"+"File Location ["+str(fileLocation)+"]\n"+"Opacity ["+str(opacity)+"]\n"+"Lang ["+str(lang)+"]\n")
		file.close()
		return True
		
		
	def loadGenSec(self):
		if os.path.exists(self.gensecconf):
			file=open(self.gensecconf,'r')
			try:
				config=['#6695df','#4e72aa','#8665df',[]]
				while True:
					line =file.readline()
					if not line:
						break
					if not line.find('Color1 '):
						config[0] =str(line.split("[")[1].split("]")[0])
					elif not line.find('Color2 '):
						config[1] =str(line.split("[")[1].split("]")[0])
					elif not line.find('Color3 '):
						config[2] =str(line.split("[")[1].split("]")[0])
					elif not line.find('Defaults Process'):
						config[3] =pickle.load(file)
						if config[3] ==[]:
							config[3] =[False,False,False,False,False,False,False,[False,False],False]
				return config
			except:
				return False
			file.close()
		return False
	
	
	def saveGenSec(self,col1,col2,col3,processDefaults):
		file=open(self.gensecconf,'w+').close()
		file=open(self.gensecconf,'w+')
		file.write("Color1 ["+str(col1)+"]\n"+"Color2 ["+str(col2)+"]\n"+"Color3 ["+str(col3)+"]\n"+"Defaults Process\n")
		pickle.dump(processDefaults,file)
		file.close()
		return True
		
	
	def loadGenRep(self):
		if os.path.exists(self.genrepconf):
			file=open(self.genrepconf,'r')
			try:
				config=[1,0,'lineal',-1,-1,-1,-1,'lineal',-1,-1,-1,-1,[]]
				while True:
					line =file.readline()
					if not line:
						break
					if not line.find('Curve to show '):
						try:
							config[0]=int(line.split("[")[1].split("]")[0])
						except:
							pass
					elif not line.find('Show TL '):
						try:
							config[1]=int(line.split("[")[1].split("]")[0])
						except:
							pass
					elif not line.find('Horizontal Scale '):
						config[2]=str(line.split("[")[1].split("]")[0])
					elif not line.find('Horizontal Minimum '):
						try:
							config[3]=float(line.split("[")[1].split("]")[0])
						except:
							pass	
					elif not line.find('Horizontal Maximum '):
						try:
							config[4]=float(line.split("[")[1].split("]")[0])
						except:
							pass
					elif not line.find('Horizontal Greater Unity '):
						try:
							config[5]=float(line.split("[")[1].split("]")[0])
						except:
							pass
					elif not line.find('Horizontal Smallest Unity '):
						try:
							config[6]=float(line.split("[")[1].split("]")[0])
						except:
							pass
					elif not line.find('Vertical Scale '):
						config[7]=str(line.split("[")[1].split("]")[0])
					elif not line.find('Vertical Minimum '):
						try:
							config[8]=float(line.split("[")[1].split("]")[0])
						except:
							pass
					elif not line.find('Vertical Maximum '):
						try:
							config[9]=float(line.split("[")[1].split("]")[0])
						except:
							pass
					elif not line.find('Vertical Greater Unity '):
						try:
							config[10]=float(line.split("[")[1].split("]")[0])
						except:
							pass
					elif not line.find('Vertical Smallest Unity '):
						try:
							config[11]=float(line.split("[")[1].split("]")[0])
						except:
							pass
					elif not line.find('Parameters '):
						try:
							temp=str(line.split("[")[1].split("]")[0])
							ints=[int(i) for i in temp.split(',')]
							if ints[0]!='':
								config[12]=ints
						except:
							pass
				return config
			except:
				return False
			file.close()
		return False
	
	
	def saveGenRep(self,curve_to_show,show_tl,h_scale,h_min,h_max,h_great_unit,h_small_unit,v_scale,v_min,v_max,v_great_unit,v_small_unit,parameters):
		file=open(self.genrepconf,'w+').close()
		file=open(self.genrepconf,'w+')
		parameters=str(parameters)[1:-1]
		file.write("Curve to show ["+str(curve_to_show)+"]\n"+"Show TL ["+str(show_tl)+"]\n"+"Horizontal Scale ["+str(h_scale)+"]\n"+"Horizontal Minimum ["+str(h_min)+"]\n"+"Horizontal Maximum ["+str(h_max)+"]\n"+"Horizontal Greater Unity ["+str(h_great_unit)+"]\n"+"Horizontal Smallest Unity ["+str(h_small_unit)+"]\n"+"Vertical Scale ["+str(v_scale)+"]\n"+"Vertical Minimum ["+str(v_min)+"]\n"+"Vertical Maximum ["+str(v_max)+"]\n"+"Vertical Greater Unity ["+str(v_great_unit)+"]\n"+"Vertical Smallest Unity ["+str(v_small_unit)+"]\n"+"Parameters ["+str(parameters)+"]\n")
		file.close()
		return True
	
		
		
		
		
		
		