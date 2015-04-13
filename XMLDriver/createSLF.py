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

from xml.dom.minidom import Document
import os
import datetime
import time

class Sample:
	"""Crea una muestra"""
	def __init__(self,sample_id):
		self.xml = Document()
		#identificador de la muestra
		self.Sample_ID =self.xml.createElement("Sample_ID")
		self.Sample_ID.setAttribute("sample", str(sample_id))
		
class ProcessOrder:
	"""Crea un ordenador de precesos de una muestra"""
	def __init__(self,process_order_id,type,status,process):
		self.xml = Document()
		#sequencial, empieza con 1 y continua con cada proceso
		self.processOrder =self.xml.createElement("Process_order")
		self.processOrder.setAttribute("number", str(process_order_id))
		#(pend, ext, done) define el estatus del proceso 
		self.status=status
		# define el tipo de proceso (irad, meas, pc)
		self.type=type			
		
		Status =self.xml.createElement("Status")
		Status.appendChild(self.xml.createTextNode(str(self.status)))
		Type =self.xml.createElement("Type")
		if self.type:
			Type.appendChild(self.xml.createTextNode(str(self.type)))
		self.processOrder.appendChild(Status)
		self.processOrder.appendChild(Type)

		for proc in process:			
			self.processOrder.appendChild(proc)
			
		
class Process:
	"""Crea un proceso """
	def __init__(self,process_id,parameters,data,column):
		self.xml = Document()
		#define el código del proceso
		self.process=self.xml.createElement("Process_ID")
		self.process.setAttribute("column", str(column))
		self.process.setAttribute("id", str(process_id))		
		self.Param =self.xml.createElement("Param")
		self.info =self.xml.createElement("info")
		self.data =self.xml.createElement("data")
		self.process.appendChild(self.Param)
		self.process.appendChild(self.info)
		self.process.appendChild(self.data)
				
		#Parameters
		Light_source =self.xml.createElement("light_source")
		Start_Optical_power =self.xml.createElement("start_optical_power")
		End_Optical_power =self.xml.createElement("end_optical_power")
		time =self.xml.createElement("time")
		datapoints1 =self.xml.createElement("datapoints1")
		datapoints2 =self.xml.createElement("datapoints2")
		datapoints3 =self.xml.createElement("datapoints3")
		number_of_scans =self.xml.createElement("number_of_scans")
		save_temp =self.xml.createElement("save_temp")
		heating_rate =self.xml.createElement("heating_rate")
		T1 =self.xml.createElement("T1")
		tT1 =self.xml.createElement("tT1")
		dT1 =self.xml.createElement("dT1")
		dP1 =self.xml.createElement("dP1")
		ExcV =self.xml.createElement("ExcV")
		ExcF =self.xml.createElement("ExcF")		
		
		
		try:
			Light_source.appendChild(self.xml.createTextNode(str(parameters['light_source']))),
		except:
			pass
		try:
			Start_Optical_power.appendChild(self.xml.createTextNode(str(parameters['start_optical_power']))),
		except:
			pass
		try:
			End_Optical_power.appendChild(self.xml.createTextNode(str(parameters['end_optical_power']))),
		except:
			pass
		try:
			time.appendChild(self.xml.createTextNode(str(parameters['time']))),
		except:
			pass
		try:
			datapoints1.appendChild(self.xml.createTextNode(str(parameters['datapoints1']))),
		except:
			pass
		try:
			datapoints2.appendChild(self.xml.createTextNode(str(parameters['datapoints2']))),
		except:
			pass
		try:
			datapoints3.appendChild(self.xml.createTextNode(str(parameters['datapoints3']))),
		except:
			pass
		try:
			number_of_scans.appendChild(self.xml.createTextNode(str(parameters['number_scan']))),
		except:
			pass
		try:
			save_temp.appendChild(self.xml.createTextNode(str(parameters['save_temp']))),
		except:
			pass
		try:
			heating_rate.appendChild(self.xml.createTextNode(str(parameters['heating_rate']))),
		except:
			pass
		try:
			T1.appendChild(self.xml.createTextNode(str(parameters['final_temp']))),
		except:
			pass
		try:
			tT1.appendChild(self.xml.createTextNode(str(parameters['time_final_temp']))),
		except:
			pass
		try:
			dT1.appendChild(self.xml.createTextNode(str(parameters['stabilization']))),
		except:
			pass
		try:
			dP1.appendChild(self.xml.createTextNode(str(parameters['dP1']))),
		except:
			pass
		try:
			ExcV.appendChild(self.xml.createTextNode(str(parameters['excV']))),
		except:
			pass
		try:
			ExcF.appendChild(self.xml.createTextNode(str(parameters['excF'])))
		except:
			pass			
		
		self.Param.appendChild(Light_source)
		self.Param.appendChild(Start_Optical_power)
		self.Param.appendChild(End_Optical_power)
		self.Param.appendChild(time)
		self.Param.appendChild(datapoints1)
		self.Param.appendChild(datapoints2)
		self.Param.appendChild(datapoints3)
		self.Param.appendChild(number_of_scans)
		self.Param.appendChild(save_temp)
		self.Param.appendChild(heating_rate)
		self.Param.appendChild(T1)
		self.Param.appendChild(tT1)
		self.Param.appendChild(dT1)
		self.Param.appendChild(dP1)
		self.Param.appendChild(ExcV)
		self.Param.appendChild(ExcF)
			
		#Info
		Datatype =self.xml.createElement("Datatype")
		comment =self.xml.createElement("comment")
		
		all_I=(
			Datatype.appendChild(self.xml.createTextNode(str(parameters['date_type']))),
			comment.appendChild(self.xml.createTextNode(str(parameters['comments'])))
		)
		for i in all_I:
			try:
				i
			except:
				pass	
		
		self.info.appendChild(Datatype)
		self.info.appendChild(comment)
		
		#Data
		Curva1 =self.xml.createElement("Curva1")
		Curva2 =self.xml.createElement("Curva2")
		Curva3 =self.xml.createElement("Curva3")
		Tiempo1 =self.xml.createElement("Tiempo1")
		Tiempo2 =self.xml.createElement("Tiempo2")
		
		all_D=(
			Curva1.appendChild(self.xml.createTextNode(str(data['Curva1']))),
			Curva2.appendChild(self.xml.createTextNode(str(data['Curva2']))),
			Curva3.appendChild(self.xml.createTextNode(str(data['Curva3']))),
			Tiempo1.appendChild(self.xml.createTextNode(str(data['Tiempo1']))),
			Tiempo2.appendChild(self.xml.createTextNode(str(data['Tiempo2'])))
		)
		for d in all_D:
			try:
				d
			except:
				pass	
		
		self.data.appendChild(Curva1)
		self.data.appendChild(Curva2)
		self.data.appendChild(Curva3)
		self.data.appendChild(Tiempo1)
		self.data.appendChild(Tiempo2)
		
		
class SEQ:
	"""Crea toda la estructura xml organizada"""
	def __init__(self,nmuestras,name,owner,n2flow,doserate,extdoserate,protocol,reader_id,datecrea):
		self.xml = Document()
		self.SEQ = self.xml.createElement("SEQ")
		self.xml.appendChild(self.SEQ)
		
		self.name=name
		#define el dueñoo de la secuencia
		self.owner=owner
		#se utilizará nitrógeno en la cámara
		self.n2flow=n2flow
		#tasa de Dosis, se obtiene del setting del equipo
		self.doserate=doserate
		#tasa de dosis externa
		self.extdoserate=extdoserate
		#Dato opcional del tipo de secuencia
		self.protocol=protocol
		#define el estatus de la secuencia
		self.status='pend'
		#número de muestras en la secuencia
		self.nmuestras=nmuestras
		#define la fecha de creación
		now=str(datetime.datetime.fromtimestamp(time.time()))
		if datecrea=='':
			self.datecrea =now
		else:
			self.datecrea=datecrea
		#define la fecha de modificación
		self.datemod=now
		#Id del lector
		self.reader_id=reader_id
		
		self.Name = self.xml.createElement("Name")
		self.STATUS = self.xml.createElement("STATUS")
		self.Datecrea = self.xml.createElement("Datecrea")
		self.Datemod = self.xml.createElement("Datemod")
		self.Owner = self.xml.createElement("Owner")
		self.NMuestras = self.xml.createElement("NMuestras")
		self.ReaderId = self.xml.createElement("Reader_ID")
		self.N2Flow =self. xml.createElement("N2Flow")
		self.Doserate = self.xml.createElement("Doserate")
		self.ExtDoserate = self.xml.createElement("ExtDoserate")
		self.Protocol = self.xml.createElement("Protocol")
		self.seq = self.xml.createElement("seq")
		
		self.Name .appendChild(self.xml.createTextNode(str(self.name)))
		self.STATUS.appendChild(self.xml.createTextNode(str(self.status)))
		self.Datecrea .appendChild(self.xml.createTextNode(str(self.datecrea)))
		self.Datemod.appendChild(self.xml.createTextNode(str(self.datemod)))
		self.Owner.appendChild(self.xml.createTextNode(str(self.owner)))
		self.NMuestras.appendChild(self.xml.createTextNode(str(self.nmuestras)))
		self.ReaderId.appendChild(self.xml.createTextNode(str(self.reader_id)))
		self.N2Flow.appendChild(self.xml.createTextNode(str(self.n2flow)))
		self.Doserate.appendChild(self.xml.createTextNode(str(self.doserate)))
		self.ExtDoserate.appendChild(self.xml.createTextNode(str(self.extdoserate)))
		self.Protocol.appendChild(self.xml.createTextNode(str(self.protocol)))

		self.SEQ.appendChild(self.Name)
		self.SEQ.appendChild(self.STATUS)
		self.SEQ.appendChild(self.Datecrea)
		self.SEQ.appendChild(self.Datemod)
		self.SEQ.appendChild(self.Owner)
		self.SEQ.appendChild(self.NMuestras)
		self.SEQ.appendChild(self.ReaderId)
		self.SEQ.appendChild(self.N2Flow)
		self.SEQ.appendChild(self.Doserate)
		self.SEQ.appendChild(self.ExtDoserate)
		self.SEQ.appendChild(self.Protocol)
		self.SEQ.appendChild(self.seq)
		
	def setDateMod(self):
		"""Cambia la fecha de modificado"""
		self.datemod =datetime.datetime.fromtimestamp(time.time())
		self.Datemod.firstChild.data=str(self.datemod)
		
	def createSample(self,sample_id):
		"""Ordena que se cree una muestra"""
		self.setDateMod()
		s_ids=self.xml.getElementsByTagName("seq")[0].getElementsByTagName('Sample_ID')
		sample=Sample(sample_id).Sample_ID
		if len(s_ids)>0:
			for sam in s_ids:
				value= sam.attributes['sample'].value
				if int(value)==int(sample_id):
					return sam
				
				if int(value)>int(sample_id):
					self.seq.insertBefore(sample,sam)
					return sample
		
		self.seq.appendChild(sample)
		return sample

		
	def createProcess(self,process_id,parameters,data,column):
		"""Ordena crear un comando"""
		process=Process(process_id,parameters,data,column)
		self.setDateMod()
		return process.process	
		
	def createProcessOrder(self,Sample_ID,process_order_id,type,status,process):
		"""Crea un proceso con un conjunto de comandos para una determinada muestra"""
		processO=ProcessOrder(process_order_id,type,status,process)
		Sample_ID.appendChild(processO.processOrder)
		self.setDateMod()
		return processO
		
	def preview(self):
		return self.xml.toprettyxml(indent="    ")
	
	def save(self,d,rewrite=False):
		"""Imprime en consla la estructura xml, y guarda el archivo en la direccion entrada"""	
		if os.path.exists(d):
			if os.path.isfile(d):
				ext=d.split('.')[-1]
				if ext!='slf' and ext!='xml':
					raise ValueError( 'Incorrect format, must be a slf file')
				else:				
					if rewrite:
						try:
							document=open(d,'w')
							self.xml.writexml(document, addindent='    ', newl='\n',encoding='iso-8859-1')
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
				if ext!='slf' and ext!='xml':
					d=d+'.slf'
				document=open(d,'w')
				self.xml.writexml(document, addindent='    ', newl='\n',encoding='iso-8859-1')
				return True
			else:
				raise ValueError( 'Directory does not exist '+directorio)	
				
		