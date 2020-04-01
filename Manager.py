#!/usr/bin/python3
# coding: utf-8
import sys
import os
import time
from time import sleep
import datetime
from datetime import date
import configparser
import json
import socket
from  urllib import request, parse
import threading
import concurrent.futures
import asyncio.coroutines
import logging
from comtele_sdk.textmessage_service import TextMessageService
from initialize import Initialize
from termcolor import colored
import schedule



class Manager(Initialize):
	# Status
	# -1 - NIVEL LOG 				INICIALIZANDO 					[...]
	#  0 - NIVEL LOG 				TAREFA CONCLUIDA				[OK]
	#  1 - NIVEL EXCEPT - 			ERRO COMUM						[X]				Notificar-me	->	Pausar Thread
	#  2 - NIVEL EXCEPT - 			WARNING							[!]
	#  3 - NIVEL EXCEPT - 			ERRO DADOS						[SQL ERRO]		Notificar-me	->	Pausar Thread
	#  4 - NIVEL EXCEPT - 										 	[!!!]			Notificar-me	->	Pausar Thread
	#  5 - NIVEL INFO - 			""								[INFO]
	#	
	# e = {
	#	"class": "Nome da Class ou Módulo"
	#	"metodo": "Nome do metodo que retornou a mensagem"
	#	"status":-1 - 5
	#	"message": []
	#	"erro":	True or False
	#	"comments":"Comentarios livre do programador"
	#	"time": datetime.datetime.now()
	# 	}
	#
	
	def __init__(self): 
		try:
			super().__init__(self)
	
		except Exception as e:
			print(type(e))
			print(e)
			sys.exit(0)
		
		log = logging.getLogger('Modulo de Gerenciamento')
		self.Jobs = super().Jobs()
		#Serviços
		
		

		self.inicializando()#So precisa de modulos, so vai modulos!
	
	def update_info(self): # TODO: Melhorar esse metodo
		#SET
		self.SMS_controle.setControle(self.SMS_info,self)
		self.SVC_controle.setControle(self.SVC_info,self)
		self.SDU_controle.setControle(self.SDU_info,self)
		self.SRC_controle.setControle(self.SRC_info,self)
		
		self.VIACEP_controle.setControle(self.VIACEP_info,self)
		self.MANDRILL_controle.setControle(self.MANDRILL_info,self)
		self.COMTELE_controle.setControle(self.COMTELE_info,self)
		self.SOA_controle.setControle(self.SOA_info,self)
		self.HUBD_controle.setControle(self.HUBD_info,self)
		self.MP_controle.setControle(self.MP_info,self)
		self.DIGIMAIS_controle.setControle(self.DIGIMAIS_info,self)
	
		#GET
		self.SMS_info = self.SMS_controle.getControle()
		self.SVC_info = self.SVC_controle.getControle()
		self.SDU_info = self.SDU_controle.getControle()
		self.SRC_info = self.SRC_controle.getControle()

		self.VIACEP_info		= self.VIACEP_controle.getControle()
		self.MANDRILL_info		= self.MANDRILL_controle.getControle()
		self.COMTELE_info		= self.COMTELE_controle.getControle()
		self.SOA_info			= self.SOA_controle.getControle()
		self.HUBD_info			= self.HUBD_controle.getControle()
		self.MP_info			= self.MP_controle.getControle()
		self.DIGIMAIS_info		= self.DIGIMAIS_controle.getControle()


		self.LINK_info			= self.Controle.LINK.getControle()
		self.Controle.writeConfigFile(self)
		return
	

	def inicializando(self):
		self.update_info()
		try:
			self.Jobs['WATCH'].start()
			self.Agenda['UPDATE'] = schedule.every(4).hours.do(self.atualiza).tag('UPDATE')
			if self.SMS_info["init"] is True:
				self.SMS_info['init_time']=str(datetime.datetime.now())
				self.Agenda['SMS'] = schedule.every(1).minutes.do(self.SMS_f).tag("SMS")
				self.SMS_info['next_run'] = str(self.Agenda["SMS"].next_run)
				#self.SMS_controle.setControle(self.SMS_info,self)


			if self.SRC_info['init'] is True:
				self.SRC_info['init_time']=str(datetime.datetime.now())
				#self.Agenda['SRC'] = schedule.every(10).seconds.do(self.SRC_f).tag('SRC')
				self.Agenda['SRC'] = schedule.every().hour.at(":00").do(self.SRC_f).tag('SRC')
				self.SRC_info['next_run'] = str(self.Agenda["SRC"].next_run)
				#self.SRC_controle.setControle(self.SRC_info,self)


			if self.SVC_info['init'] is True:
				self.SVC_info['init_time']=str(datetime.datetime.now())
				self.Agenda['SVC'] = schedule.every(2).minutes.do(self.SVC_f).tag("SVC")
				self.SVC_info['next_run'] = str(self.Agenda["SVC"].next_run)
				#self.SVC_controle.setControle(self.SVC_info,self) 

		
		except Exception as err:
			if "KILL_ALL" in err.args[0]:
				
				
				message = []
				message.append(err.args[0])
				
				e= {
				"class":"???",
				"metodo":"Se eu não sei nem a classe...",
				"status":4,
				"message":message,
				"erro":True,
				"comments":"Arrumar uma forma de identificar melhor tais erros...",
				"time":str(datetime.datetime.now())
				}
				self.callback(e)
			else:
				e= {
				"class":"???",
				"metodo":"Se eu não sei nem a classe...",
				"status":4,
				"message": [err, type(err)],
				"erro":True,
				"comments":"Arrumar uma forma de identificar melhor tais erros...",
				"time":str(datetime.datetime.now())
				}
				self.callback(e)
			#Quando a função lança uma exception o fluxo volta para ca
			print("INITALIZE -__init__ Oops!{0} occured.".format(sys.exc_info()[0]))
			#sys.exit()
		
		
		self.Agendados()

	def atualiza(self):
		shedule.clear()
		self.inicializando()

	def Agendados(self):
		while True:
			
			if  self.SVC_info['stop']:
				schedule.clear('SVC')
			elif  self.SRC_info['stop']:
				schedule.clear('SRC')
			elif  self.SMS_info['stop']:
				schedule.clear('SMS')
			elif self.SVC_info['stop'] and self.SRC_info['stop'] and self.SMS_info['stop']:
				schedule.clear()
				break
			schedule.run_pending()
		return
	
	def verifica(self):
		self.update_info()
		setting ={'init_time': datetime.datetime.now()}
		if not self.Jobs['WATCH'].isAlive():
			self.Jobs['WATCH'] = threading.Thread(target=self.Watch.start, name="WATCH")
			self.Jobs['WATCH'].start()
		if (self.Agenda["SMS"] is None) and (self.SMS_info['keepAlive'] is True):
			self.SMS_info['init_time'] = str(datetime.datetime.now())
			self.Agenda['SMS'] = schedule.every(1).minutes.do(self.SMS_f).tag("SMS")
			self.SMS_info['next_run'] = str(self.Agenda["SMS"].next_run)
			self.SMS_controle.setControle(self.SMS_info,self)

		if (not self.Agenda['SRC'] is None ) and (self.SRC_info['keepAlive'] is True):

			self.SRC_info['init_time'] = str(datetime.datetime.now())
			self.Agenda['SRC'] = schedule.every().hour.at(":00").do(self.SRC_f).tag('SRC')
			self.SRC_info['next_run'] = str(self.Agenda["SRC"].next_run)
			self.SRC_controle.setControle(self.SRC_info,self)

		if (not self.Jobs['SVC'] is None) and (self.SVC_info['keepAlive'] is True):

			self.SVC_info['init_time'] = str(datetime.datetime.now())
			self.Agenda['SVC'] = schedule.every(2).minutes.do(self.SVC_f).tag("SVC")
			self.SVC_info['next_run'] = str(self.Agenda["SVC"].next_run)
			self.SVC_controle.setControle(self.SVC_info,self) 

	def finaliza(self, servico):
		""" /* *
		TODO: Um metodo para evitar essa repetição de instruções
		*/ """
		
		
		if "SDU" in servico:
			
			self.update_info()
			if self.Jobs['SDU'].isAlive():
				self.Jobs["SDU"].raise_exception()
				

		elif "SVC" in servico:
			self.SVC_info['stop'] = True
			self.SVC_info['keepAlive'] = False
			self.update_info()
			if self.Jobs['SVC'].isAlive():
				self.Jobs["SVC"].raise_exception()
			schedule.clear('SVC')
			self.Agenda['SVC'] = None
		elif "SMS" in servico:
		
			self.SMS_info['stop'] = True
			self.SMS_info['keepAlive'] = False
			self.update_info()
			schedule.clear('SMS')
			self.Agenda['SMS'] = None
		elif "SRC" in servico:
			self.SRC_info['stop'] = True
			self.SRC_info['keepAlive'] = False
			self.update_info()
			schedule.clear('SRC')
			self.Agenda['SRC'] = None
		elif "ALL" in servico:
			if self.Jobs['SVC'].isAlive():
				self.Jobs["SVC"].raise_exception()
			if self.Jobs['SDU'].isAlive():
				self.Jobs["SDU"].raise_exception()

			self.SVC_info['stop'] = True
			self.SVC_info['keepAlive'] = False
			self.SMS_info['stop'] = True
			self.SMS_info['keepAlive'] = False
			self.SRC_info['stop'] = True
			self.SRC_info['keepAlive'] = False
			self.SRC_info['stop'] = True
			self.SRC_info['keepAlive'] = False
			self.update_info()
			schedule.clear()
			self.Agenda = None
			self.Agenda = []
	
	def run(self,s):
		if "SRC" in s:
			loop = asyncio.new_event_loop()
			return_value = loop.run_until_complete(self.recuperacaoDeCarrinhos.runNow())
		
			return return_value
		if "SMS" in s:
			loop = asyncio.new_event_loop()
			return_value = loop.run_until_complete(self.SMS.runNow())
			return return_value
		
		if "SDU" in s:
			self.Jobs['SDU'] = threading.Thread(target=self.DataUpdate.start, name="SDU")
			self.Jobs['SDU'].start()
		else :
			return False

	def inicia(self, servico):
		
		if "SVC" in servico:
			
			self.SVC_info['stop'] = False
			self.SVC_info['keepAlive'] = True
			self.verifica()
		elif "SMS" in servico:
			self.SMS_info['stop'] = False
			self.SMS_info['keepAlive'] = True
			
			self.verifica()

		elif "SRC" in servico:
			self.SRC_info['stop'] = False
			self.SRC_info['keepAlive'] = True
		
			self.verifica()

		elif "ALL" in servico:
			self.SVC_info['stop'] = False
			self.SVC_info['keepAlive'] = True

			self.SMS_info['stop'] = False
			self.SMS_info['keepAlive'] = True

			self.SRC_info['stop'] = False
			self.SRC_info['keepAlive'] = True
			
			self.inicializando()

	def callback(self,e):
		
		if any(status in str(e['status']) for status in ['1','2','3','4'] ) and not str(e['status']) =='-1':
			self.Exceptions(e)
		else:
			self.Logs(e)

	def Exceptions(self, e):
		self.update_info()
		""" TODO: 
		! revisar erros e execeções!
		"""
		#DOS SERVIÇOS
		if 'SMS' in e['class']:	
			e["Controle"]=self.SMS_info
			self.SMS_info['keepAlive'] = False
			self.SMS_info['stop'] = True
			self.SMS_controle.setControle(self.SMS_info,self)
			self.Logs(e)
			
			if  any(status in str(e['status']) for status in ['1','3','4'] ) and not str(e['status']) =='-1':
				self.Notificar(e)
				self.finaliza('sms')
			else:
				self.Logs(e)

			
		elif 'recuperacaoDeCarrinhos' in e['class']  :

			e["Controle"]=self.SRC_info
			self.SRC_info['keepAlive'] = False
			self.SRC_info['stop'] = True
			self.SRC_controle.setControle(self.SRC_info,self)
			self.Logs(e)
			
			if  any(status in str(e['status']) for status in ['1','3','4'] ) and not str(e['status']) =='-1':
				self.Notificar(e)
				self.finaliza('src')
			else:
				self.Logs(e)

		elif 'servicoDeValidacao' in e['class'] :
			e["Controle"]=self.SVC_info
			self.SVC_info['keepAlive'] = False
			self.SVC_info['stop'] = True
			self.SVC_controle.setControle(self.SVC_info,self)
			self.Logs(e)
			
			if  any(status in str(e['status']) for status in ['1','3','4'] ) and not str(e['status']) =='-1':
				self.Notificar(e)
				self.finaliza('svc')
			else:
				self.Logs(e)

		elif 'DataUpdate' in e['class']:
			e["Controle"]=self.SDU_info
			self.SDU_info['keepAlive'] = False
			self.SDU_info['stop'] = True
			self.SDU_controle.setControle(self.SDU_info,self)
			self.Logs(e)
			
			if  any(status in str(e['status']) for status in ['1','3','4'] ) and not str(e['status']) =='-1':
				self.Notificar(e)
				self.finaliza('sdu')
			else:
				self.Logs(e)

		elif 'DB' in e['class'] :
			self.Logs(e)
			if  any(status in str(e['status']) for status in ['1','3','4'] ) and not str(e['status']) =='-1':
				self.Notificar(e)
				self.finaliza('src')
			else:
				self.Logs(e)

	def Logs(self, e):
		""" 
		TODO:Definir arquivos de logs individuais para cada serviço para melhor analise dos mesmos
		"""
		e["ENV"] = self.Controle.Key.env
		log = logging.getLogger('{message:{fill}^{width}}'.format(message=e['class']+"."+e['metodo'],fill=" ",align="^",width=50	))
		for msg in e['message']:
			if msg is not None and msg != "":
				log.info(" {0} ".format(msg))
		if e['comments']!="" and e['comments'] is not None:
			log.info(" {0} ".format(e['comments']))
	#TODO INSERIR INFORMAÇÔES DE NOTIFICAÇÂO NO CONTROLER TAMBÈM
	def Notificar(self, e):
		Comtele = self.Controle.API.comtele.getControle()
		e["AMBIENTE"]= self.Controle.Key.env
		administradores = [
			'47997619694',
			'47988948000',
			'47991566969'
		]
		for x in e['Controle']:
			e['Controle'][x] = str(e['Controle'][x])
		log = logging.getLogger("Manager")
		log.info( '{0}[!]Notificando Administradores!'.format(datetime.datetime.now()))
		log.info(e)
		
		
		textmessage_service = TextMessageService(Comtele['api_key'])
		
		
		try:
			result = textmessage_service.send('MS_.Manager - Error', json.dumps(e), administradores)
			log.info( '{0}[!]Notificação de Falha enviada!!'.format(datetime.datetime.now()))
		except Exception as e :
			log.info( '{0}[!!!]Não foi possivel notificar!'.format(datetime.datetime.now()))
			log.info( '{0}[!!!]{1}'.format(datetime.datetime.now(),e))
			
		return

if __name__ == "__main__":
	pass
	M = Manager()
