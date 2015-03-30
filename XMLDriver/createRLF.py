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
		self.Sample_ID =self.xml.createElement("Sample_ID")
		self.Sample_ID.setAttribute("sample", str(sample_id))
		
class ProcessOrder:
	"""Crea una etiqueta de tipo process_order"""
	def __init__(self,process_order_id,ptype,dtype,curves,parameters):
		self.xml = Document()
		self.processOrder =self.xml.createElement("Process_order")
		self.processOrder.setAttribute("order", str(process_order_id))
		self.ptype=ptype
		self.dtype=dtype			
		
		Process =self.xml.createElement("Process")
		Process.appendChild(self.xml.createTextNode(str(self.ptype)))
		Data_type =self.xml.createElement("Data_type")
		Data_type.appendChild(self.xml.createTextNode(str(self.dtype)))
		self.processOrder.appendChild(Process)
		self.processOrder.appendChild(Data_type)
		
		#Curves
		for curve in curves:			
			self.processOrder.appendChild(curve)
		
		#Parameters
		Beta_irradiation_time =self.xml.createElement("Beta_irradiation_time")
		Beta_dose =self.xml.createElement("Beta_dose")
		External_irradiation =self.xml.createElement("External_irradiation")
		External_dose =self.xml.createElement("External_dose")
		Preheating_temperature =self.xml.createElement("Preheating_temperature")
		Measuring_temperature =self.xml.createElement("Measuring_temperature")
		Preheating_rate =self.xml.createElement("Preheating_rate")
		Heating_rate =self.xml.createElement("Heating_rate")
		Light_source =self.xml.createElement("Light_source")
		Optical_power =self.xml.createElement("Optical_power")
		Electric_stimulation =self.xml.createElement("Electric_stimulation")
		Electric_frequency =self.xml.createElement("Electric_frequency")
		Time_beta_irradiation =self.xml.createElement("Time_beta_irradiation")
		Time_external_irradiation =self.xml.createElement("Time_external_irradiation")
		Time_measurement =self.xml.createElement("Time_measurement")
		Illumination_source  =self.xml.createElement("Illumination_source")
		Illumination_power=self.xml.createElement("Illumination_power")
		Illumination_temperature=self.xml.createElement("Illumination_temperature")
			
		try:
			Beta_irradiation_time.appendChild(self.xml.createTextNode(str(parameters['Beta_irradiation_time']))),
			self.processOrder.appendChild(Beta_irradiation_time)
		except:
			pass
		try:
			Beta_dose.appendChild(self.xml.createTextNode(str(parameters['Beta_dose']))),
			self.processOrder.appendChild(Beta_dose)
		except:
			pass
		try:
			External_irradiation.appendChild(self.xml.createTextNode(str(parameters['External_irradiation']))),
			self.processOrder.appendChild(External_irradiation)
		except:
			pass
		try:
			External_dose.appendChild(self.xml.createTextNode(str(parameters['External_dose']))),
			self.processOrder.appendChild(External_dose)
		except:
			pass
		try:
			Preheating_temperature.appendChild(self.xml.createTextNode(str(parameters['Preheating_temperature']))),
			self.processOrder.appendChild(Preheating_temperature)
		except:
			pass
		try:
			Measuring_temperature.appendChild(self.xml.createTextNode(str(parameters['Measuring_temperature']))),
			self.processOrder.appendChild(Measuring_temperature)
		except:
			pass
		try:
			Preheating_rate.appendChild(self.xml.createTextNode(str(parameters['Preheating_rate']))),
			self.processOrder.appendChild(Preheating_rate)
		except:
			pass
		try:
			Heating_rate.appendChild(self.xml.createTextNode(str(parameters['Heating_rate']))),
			self.processOrder.appendChild(Heating_rate)
		except:
			pass
		try:
			Light_source.appendChild(self.xml.createTextNode(str(parameters['Light_source']))),
			self.processOrder.appendChild(Light_source)
		except:
			pass
		try:
			Optical_power.appendChild(self.xml.createTextNode(str(parameters['Optical_power']))),
			self.processOrder.appendChild(Optical_power)
		except:
			pass
		try:
			Electric_stimulation.appendChild(self.xml.createTextNode(str(parameters['Electric_stimulation']))),
			self.processOrder.appendChild(Electric_stimulation)
		except:
			pass
		try:
			Electric_frequency.appendChild(self.xml.createTextNode(str(parameters['Electric_frequency']))),
			self.processOrder.appendChild(Electric_frequency)
		except:
			pass
		try:
			Time_beta_irradiation.appendChild(self.xml.createTextNode(str(parameters['Time_beta_irradiation']))),
			self.processOrder.appendChild(Time_beta_irradiation)
		except:
			pass
		try:
			Time_external_irradiation.appendChild(self.xml.createTextNode(str(parameters['Time_external_irradiation']))),
			self.processOrder.appendChild(Time_external_irradiation)
		except:
			pass
		try:
			Time_measurement.appendChild(self.xml.createTextNode(str(parameters['Time_measurement']))),
			self.processOrder.appendChild(Time_measurement)
		except:
			pass
		try:
			Illumination_source.appendChild(self.xml.createTextNode(str(parameters['Illumination_source']))),
			self.processOrder.appendChild(Illumination_source)
		except:
			pass
		try:
			Illumination_power.appendChild(self.xml.createTextNode(str(parameters['Illumination_power']))),
			self.processOrder.appendChild(Illumination_power)
		except:
			pass
		try:
			Illumination_temperature.appendChild(self.xml.createTextNode(str(parameters['Illumination_temperature']))),
			self.processOrder.appendChild(Illumination_temperature)
		except:
			pass
		
		
class Curve:
	def __init__(self,num,signal,background,Conteos_SG, Canal_inf_SG, Canal_sup_SG, Conteos_BG, Canal_inf_BG,Canal_sup_BG):
		self.xml = Document()		
		self.Curve =self.xml.createElement("Curve"+str(num))
		if signal:
			self.Conteos_SG =self.xml.createElement("Conteos_SG")
			self.Canal_inf_SG =self.xml.createElement("Canal_inf_SG")
			self.Canal_sup_SG =self.xml.createElement("Canal_sup_SG")
			self.Conteos_SG.appendChild(self.xml.createTextNode(str(Conteos_SG)))
			self.Canal_inf_SG.appendChild(self.xml.createTextNode(str(Canal_inf_SG)))
			self.Canal_sup_SG.appendChild(self.xml.createTextNode(str(Canal_sup_SG)))
			self.Curve.appendChild(self.Conteos_SG)
			self.Curve.appendChild(self.Canal_inf_SG)
			self.Curve.appendChild(self.Canal_sup_SG)
		if background:
			self.Conteos_BG =self.xml.createElement("Conteos_BG")
			self.Canal_inf_BG =self.xml.createElement("Canal_inf_BG")
			self.Canal_sup_BG =self.xml.createElement("Canal_sup_BG")		
			self.Conteos_BG.appendChild(self.xml.createTextNode(str(Conteos_BG)))
			self.Canal_inf_BG.appendChild(self.xml.createTextNode(str(Canal_inf_BG)))
			self.Canal_sup_BG.appendChild(self.xml.createTextNode(str(Canal_sup_BG)))		
			self.Curve.appendChild(self.Conteos_BG)
			self.Curve.appendChild(self.Canal_inf_BG)
			self.Curve.appendChild(self.Canal_sup_BG)
	
		
class REP:
	"""Crea toda la estructura xml organizada"""
	def __init__(self,nmuestras,name,owner,n2flow,doserate,extdoserate,protocol,status,reader_id,datecrea):
		self.xml = Document()
		self.REP = self.xml.createElement("REP")
		self.xml.appendChild(self.REP)
		
		self.name=name
		self.owner=owner
		self.n2flow=n2flow
		self.doserate=doserate
		self.extdoserate=extdoserate
		self.protocol=protocol
		self.status=status
		self.nmuestras=nmuestras
		now=str(datetime.datetime.fromtimestamp(time.time()))
		if datecrea=='':
			self.datecrea =now
		else:
			self.datecrea=datecrea
		self.datemod=now
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
		self.rep = self.xml.createElement("rep")
		
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

		self.REP.appendChild(self.Name)
		self.REP.appendChild(self.STATUS)
		self.REP.appendChild(self.Datecrea)
		self.REP.appendChild(self.Datemod)
		self.REP.appendChild(self.Owner)
		self.REP.appendChild(self.NMuestras)
		self.REP.appendChild(self.ReaderId)
		self.REP.appendChild(self.N2Flow)
		self.REP.appendChild(self.Doserate)
		self.REP.appendChild(self.ExtDoserate)
		self.REP.appendChild(self.Protocol)
		self.REP.appendChild(self.rep)
		
	def setDateMod(self):
		"""Cambia la fecha de modificado"""
		self.datemod =datetime.datetime.fromtimestamp(time.time())
		self.Datemod.firstChild.data=str(self.datemod)
		
	def createSample(self,sample_id):
		"""Ordena que se cree una muestra"""
		self.setDateMod()
		s_ids=self.xml.getElementsByTagName("rep")[0].getElementsByTagName('Sample_ID')
		sample=Sample(sample_id).Sample_ID
		if len(s_ids)>0:
			for sam in s_ids:
				value= sam.attributes['sample'].value
				if int(value)==int(sample_id):
					return sam
				
				if int(value)>int(sample_id):
					self.rep.insertBefore(sample,sam)
					return sample
		
		self.rep.appendChild(sample)
		return sample

		
	def createProcessOrder(self,Sample_ID,process_order_id,ptype,dtype,curves,parameters):
		"""Crea un proceso con un conjunto de comandos para una determinada muestra"""
		processO=ProcessOrder(process_order_id,ptype,dtype,curves,parameters)
		Sample_ID.appendChild(processO.processOrder)
		self.setDateMod()
		return processO
		
	def createCurve(self,num,signal,background,Conteos_SG, Canal_inf_SG, Canal_sup_SG, Conteos_BG, Canal_inf_BG,Canal_sup_BG):
		curve=Curve(num,signal,background,Conteos_SG, Canal_inf_SG, Canal_sup_SG, Conteos_BG, Canal_inf_BG,Canal_sup_BG)
		self.setDateMod()
		return curve.Curve	
		
	def preview(self):
		return self.xml.toprettyxml(indent="    ")
	
	def save(self,d,rewrite=False):
		"""Imprime en consla la estructura xml, y guarda el archivo en la direccion entrada"""	
		if os.path.exists(d):
			if os.path.isfile(d):
				ext=d.split('.')[-1]
				if ext!='rlf' and ext!='xml':
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
				if ext!='rlf' and ext!='xml':
					d=d+'.rlf'
				document=open(d,'w')
				self.xml.writexml(document, addindent='    ', newl='\n',encoding='iso-8859-1')
				return True
			else:
				raise ValueError( 'Directory does not exist '+directorio)	
