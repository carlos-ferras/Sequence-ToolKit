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

import xml.etree.cElementTree as cET
import os
from xml.etree.ElementTree import tostring

class Loader:
	def __init__(self,dir):
		self.load(dir)
	
	def load(self,dir):
		"""carga el xml desde la direccion"""
		if os.path.exists(dir):
			if os.path.isfile(dir):
				ext=dir.split('.')[-1]
				if ext!='slf':
					raise ValueError( 'Incorrect format, must be a slf file')
			else:
				raise ValueError( 'The address is not valid, must be a slf file')
		else:
			raise ValueError( 'Directory does not exist '+dir)
		try:
			self.dir=dir
			self.tree = cET.parse(self.dir)
			self.root = self.tree.getroot()
		except:
			raise ValueError( 'Existing document corrupt')
	
	def getValue(self,root,etq):
		"""Devuelve el contenido de la etiqueta pasada por parametro que este contenida dentro de root"""
		try:
			self.value = root.find(str(etq)).text
			return self.value
		except:
			raise ValueError('There is not tag '+str(etq)+' at the current level of document')
		
		
	def setValue(self,root,etq,v):
		"""Cambia el valor la etiqueta pasada por parametro que este contenida dentro de root"""
		try:
			etiquetas=etq.split('/')
			etqAct=root
			for e in etiquetas[:-1]:
				etqAct=root.find(str(e))
			for imp in etqAct.getiterator(str(etiquetas[-1])):
				imp.text = str(v)
			return True
		except:
			raise ValueError('There is not tag '+str(etq)+' at the current level of document')
			
	def getAttr(self,element,attr):
		try:
			return element.get(attr)
		except:
			raise ValueError('Error in input parameters')
	
	def setAttr(self,element,attr,value):
		try:
			element.set(attr, value)
			return True		
		except:
			raise ValueError('Error in input parameters')
		
	def getSample(self,id):
		"""retorna la muestra con con el id pasado"""
		return self.root.find("seq/Sample_ID[@sample='"+str(id)+"']")
		
	def getProcessOrder(self,sample,id):
		"""retorna el ordenador de procesos con el id pasadop que pertenece a la muestra pasada"""
		return sample.find("Process_order[@number='"+str(id)+"']")
		
	def getProcess(self,processO,id):
		"""retorna el proceso con el id pasado que pertenece al ordenador de procesos pasado"""
		return processO.find("Process_ID[@id='"+str(id)+"']")
		
	def construir(self,raiz):
		"""Crea una estructura en forma de lista con 3 elementos,
		el primero es la raiz,
		el segundo es una lista con todos sus hijos donde cada hijo es una estructura igual a la misma estructura principal, si no tiene hijos es el valor k tiene
		y el tercero es una lista con 2 elemntos, el primero es una lista con todos los atributos de la raiz, y el segundo otra lista con los valores de los atributos"""
		hijos=raiz.getchildren()
		attrs=raiz.keys()
		values=[]
		for attr in attrs:
			values.append(raiz.get(attr))		
		arbol=[raiz,hijos,[attrs,values]]
		if len(hijos)==0:
			arbol[1]=raiz.text
		else:		
			for i in range(len(arbol[1])):		
				item=self.construir(arbol[1][i])
				arbol[1][i]=item
		return arbol
		
	def exportExtructure(self):
		"""Ejecuta el metodo construir para la raiz del archivo"""
		return self.construir(self.root)	

	def save(self,rewrite=False,*dir):
		"""Salva el xml en la direccion pasada por parametro, si existe la direccion, devuelve falso, indicando
		que es necesario sobrescribir, de ser exitosa la salva retorna true"""
		if len(dir)==0:
			d=self.dir
		else:
			d=dir[0]			
		if os.path.exists(d):
			if os.path.isfile(d):
				ext=d.split('.')[-1]
				if ext!='slf':
					raise ValueError( 'Incorrect format, must be a slf file')
				else:				
					if rewrite:
						try:
							self.tree.write(d, encoding="iso-8859-1")
							return True
						except:
							raise ValueError( 'Existing document corrupt')
					return False
			else:
				raise ValueError( 'Should put a file name')
		else:
			directorio=os.path.dirname(d)
			if os.path.exists(directorio) or directorio=='':
				base=os.path.basename(d)
				ext=base.split('.')[-1]
				if ext!='slf':
					d=d+'.slf'
				self.tree.write(d, encoding="iso-8859-1")
				return True
			else:
				raise ValueError( 'Directory does not exist '+directorio)		
