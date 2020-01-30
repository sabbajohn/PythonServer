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
		self.SMS_controle = self.Controle.servicos.SMS
		self.SVC_controle = self.Controle.servicos.SVC
		self.SDU_controle = self.Controle.servicos.SDU
		self.SRC_controle = self.Controle.servicos.SRC
		self.SMS_info = self.SMS_c.getControle()
		self.SVC_info = self.SVC_c.getControle()
		self.SDU_info = self.SDU_c.getControle()
		self.SRC_info = self.SRC_c.getControle()
		self.inicializando()#So precisa de modulos, so vai modulos!
	
	def update_info():
		self.SMS_info = self.SMS_c.getControle()
		self.SVC_info = self.SVC_c.getControle()
		self.SDU_info = self.SDU_c.getControle()
		self.SRC_info = self.SRC_c.getControle()

	def inicializando(self):
		self.update_info()
		try:
			self.Jobs['WATCH'].start()
			
			if self.SMS_info["init"] is True:
				self.Jobs['SMS'].start()
				self.SMS_info['init_time']=datetime.datetime.now()
				self.SMS_controle.setControle(self.SMS_info)

			if self.SRC_info['init'] is True:
				self.Jobs['SRC'].start()
				self.SRC_info['init_time']=datetime.datetime.now()
				self.SRC_controle.setControle(self.SRC_info) 

			if self.SVC_info['init'] is True:
				
				self.ValidacaoEUpdate()


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
				"time":datetime.datetime.now()
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
				"time":datetime.datetime.now()
				}
				self.callback(e)
			#Quando a função lança uma exception o fluxo volta para ca
			print("INITALIZE -__init__ Oops!{0} occured.".format(sys.exc_info()[0]))
			#sys.exit()

	def ValidacaoEUpdate(self):
		
		self.update_info()
		self.SVC_info['init_time']=datetime.datetime.now()
		self.SVC_controle.setControle(self.SVC_info) 
		self.SDU_info['init_time']=datetime.datetime.now()
		self.SDU_controle.setControle(self.SDU_info) 
		schedule.every(3).minutes.do(self.inicia, "svc")
		schedule.every(3).minutes.do(self.inicia, "sdu")
		self.SVC_controle.setControle(dict('nextrun': schedule.jobs[0].next_run))
		self.SDU_controle.setControle(dict('nextrun': schedule.jobs[0].next_run))
		
			
		while SVC_c.keepAlive is True:
					schedule.run_pending()
					time.sleep(1)

	def verifica(self):
		self.update_info()
		if not self.Jobs['WATCH'].isAlive():
			self.Jobs['WATCH'] = threading.Thread(target=self.Watch.start, name="WATCH")
			self.Jobs['WATCH'].start()
		if (not self.Jobs['SMS'].isAlive()) and (self.SMS_info['keepAlive'] is True):
			self.Jobs['SMS'] = threading.Thread(target=self.SMS.start, name="SMS",args=(lambda:self.SMS_info['stop'],))
			self.Jobs['SMS'].start()
			self.SMS_controle.setControle(dict('init_time': datetime.datetime.now()))
		if (not self.Jobs['SRC'].isAlive()) and (self.SRC_info['keepAlive'] is True):
			self.Jobs['SRC'] = threading.Thread(target=self.recuperacaoDeCarrinhos.start, name="SRC",args=(lambda:self.SRC_info['stop'],))
			self.Jobs['SRC'].start()
			self.SRC_controle.setControle(dict('init_time': datetime.datetime.now()))

	def finaliza(self, servico):
		if "sdu" in servico:
			self.SDU_controle.setControle(dict("keepAlive":False))
			self.SDU_controle.setControle(dict("stop":True))
			self.update_info()
			if self.Jobs['SDU'].isAlive():
				self.Jobs["SDU"].raise_exception()
				

		elif "svc" in servico:
			self.SVC_controle.setControle(dict("keepAlive":False))
			self.SVC_controle.setControle(dict("stop":True))
			self.update_info()
			if self.Jobs['SVC'].isAlive():
				self.Jobs["SVC"].raise_exception()
			
		elif "sms" in servico:
		
			self.SMS_controle.setControle(dict("keepAlive":False))
			self.SMS_controle.setControle(dict("stop":True))
			self.update_info()

				
		elif "src" in servico:
			self.SRC_controle.setControle(dict("keepAlive":False))
			self.SRC_controle.setControle(dict("stop":True))
			self.update_info()
		
		elif "all" in servico:
			if self.Jobs['SVC'].isAlive():
				self.Jobs["SVC"].raise_exception()
			if self.Jobs['SDU'].isAlive():
				self.Jobs["SDU"].raise_exception()

			self.SVC_controle.setControle(dict("keepAlive":False))
			self.SVC_controle.setControle(dict("stop":True))

			self.SDU_controle.setControle(dict("keepAlive":False))
			self.SDU_controle.setControle(dict("stop":True))

			self.SMS_controle.setControle(dict("keepAlive":False))
			self.SMS_controle.setControle(dict("stop":True))

			self.SRC_controle.setControle(dict("keepAlive":False))
			self.SRC_controle.setControle(dict("stop":True))
			self.update_info()

	def run(self,s):
		if "src" in s:
			loop = asyncio.new_event_loop()
			return_value = loop.run_until_complete(self.recuperacaoDeCarrinhos.runNow())
		
			return return_value
		if "sms" in s:
			loop = asyncio.new_event_loop()
			return_value = loop.run_until_complete(self.SMS.runNow())
			return return_value
		
		if "sdu" in s:
			self.Jobs['SDU'] = threading.Thread(target=self.DataUpdate.start, name="SDU")
			self.Jobs['SDU'].start()
		else :
			return False

	def inicia(self, servico):
		
		elif "svc" in servico:
			
			self.SVC_controle.setControle(dict('keepAlive': True))
			self.SVC_controle.setControle(dict('stop': False))
		elif "sms" in servico:
			self.SMS_controle.setControle(dict('keepAlive': True))
			self.SMS_controle.setControle(dict('stop': False))
			self.verifica()

		elif "src" in servico:
			self.SRC_controle.setControle(dict('keepAlive': True))
			self.SRC_controle.setControle(dict('stop': False))
			self.verifica()

		elif "all" in servico:
			self.SVC_controle.setControle(dict('keepAlive': True))
			self.SVC_controle.setControle(dict('stop': False))

			self.SMS_controle.setControle(dict('keepAlive': True))
			self.SMS_controle.setControle(dict('stop': False))
			
			self.SRC_controle.setControle(dict('keepAlive': True))
			self.SRC_controle.setControle(dict('stop': False))
			self.inicializando()

	def callback(self,e):
		
		if any(status in e['status'] for status in ['1','2','3','4'] ):
			self.Exceptions(e)
		else:
			self.logs(e)

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
			self.SMS_controle.setControle(self.SMS_info)
			self.Logs(e)
			
			if  any(status in e['status'] for status in ['1','3','4'] ):
				self.Notificar(e)
				self.finaliza('sms')
			else:
				self.Logs(e)

			
		elif 'recuperacaoDeCarrinhos' in e['class']  :

			e["Controle"]=self.SRC_info
			self.SRC_info['keepAlive'] = False
			self.SRC_info['stop'] = True
			self.SRC_controle.setControle(self.SRC_info)
			self.Logs(e)
			
			if  any(status in e['status'] for status in ['1','3','4'] ):
				self.Notificar(e)
				self.finaliza('src')
			else:
				self.Logs(e)

		elif 'servicoDeValidacao' in e['class'] :
			e["Controle"]=self.SVC_info
			self.SVC_info['keepAlive'] = False
			self.SVC_info['stop'] = True
			self.SVC_controle.setControle(self.SVC_info)
			self.Logs(e)
			
			if  any(status in e['status'] for status in ['1','3','4'] ):
				self.Notificar(e)
				self.finaliza('svc')
			else:
				self.Logs(e)

		elif 'DataUpdate' in e['class']:
			e["Controle"]=self.SDU_info
			self.SDU_info['keepAlive'] = False
			self.SDU_info['stop'] = True
			self.SDU_controle.setControle(self.SDu_info)
			self.Logs(e)
			
			if  any(status in e['status'] for status in ['1','3','4'] ):
				self.Notificar(e)
				self.finaliza('sdu')
			else:
				self.Logs(e)

		elif 'DB' in e['class'] :
			self.Logs(e)
			if  any(status in e['status'] for status in ['1','3','4'] ):
				self.Notificar(e)
				self.finaliza('src')
			else:
				self.Logs(e)

	def Logs(self, e):
		e["ENV"] = self.Controle.Key.env
		log = logging.getLogger('{message:{fill}^{width}}'.format(message=e['class']+"."+e['metodo'],fill=" ",align="^",width=50	))
		for msg in e['message']:
			if msg is not None and msg != "":
				log.info(" {0} ".format(msg))
		if e['comments']!="" and e['comments'] is not None:
			log.info(" {0} ".format(e['comments']))

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
