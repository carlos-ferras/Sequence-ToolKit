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
		pass
	
	
	def saveGenRep(self):
		pass
			
	
		
		
		
		
		
		