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
			self.dir=self.userRoot+'/.genSec.conf'
		except:
			self.dir='genSec.conf'
		
	def load(self):		
		if os.path.exists(self.dir):
			file=open(self.dir,'r')
			try:
				config=['Novason',12,'',1,'#6695df','#4e72aa','#8665df','',[]]
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
					elif not line.find('Color1 '):
						config[4] =str(line.split("[")[1].split("]")[0])
					elif not line.find('Color2 '):
						config[5] =str(line.split("[")[1].split("]")[0])
					elif not line.find('Color3 '):
						config[6] =str(line.split("[")[1].split("]")[0])
					elif not line.find('Lang '):
						config[7] =str(line.split("[")[1].split("]")[0])
					elif not line.find('Defaults Process'):
						config[8] =pickle.load(file)
						if config[8] ==[]:
							config[8] =[False,False,False,False,False,False,False,[False,False],False]
				return config
			except:
				return False
			file.close()
		return False
			
	def save(self,fuente,size,fileLocation,opacity,lang,col1=False,col2=False,col3=False,processDefaults=False):
		if col1==False:
			try:
				actual=self.load()
				col1=actual[4]
				col2=actual[5]
				col3=actual[6]
				processDefaults=actual[8]
			except:
				col1='#6695df'
				col2='#4e72aa'
				col3='#8665df'
				processDefaults=[False,False,False,False,False,False,False,[False,False],False]
		file=open(self.dir,'w+').close()
		file=open(self.dir,'w+')
		file.write("Font ["+str(fuente)+"]\n"+"Size ["+str(size)+"]\n"+"File Location ["+str(fileLocation)+"]\n"+"Opacity ["+str(opacity)+"]\n"+"Color1 ["+str(col1)+"]\n"+"Color2 ["+str(col2)+"]\n"+"Color3 ["+str(col3)+"]\n"+"Lang ["+str(lang)+"]\n"+"Defaults Process\n")
		pickle.dump(processDefaults,file)
		file.close()
		return True
		
		
		
		
		
		