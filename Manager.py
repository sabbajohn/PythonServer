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


class Manager(Initialize):
	# Status
	# -1 - NIVEL LOG 				INICIALIZANDO 					[...]
	#  0 - NIVEL LOG 				TAREFA CONCLUIDA'				[OK]
	#  1 - NIVEL EXCEPT - 			ERRO							[X]				Notificar-me	->	Pausar Thread
	#  2 - NIVEL EXCEPT - 			WARNING							[!]
	#  3 - NIVEL EXCEPT - 			DIE 							[DIE]			Notificar-me	->	Pausar Thread
	#  4 - NIVEL EXCEPT - 			ATTETION (Erro não tratado) 	[!!!]			Notificar-me	->	Pausar Thread
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
		time.time() 
		
		
		try:
			super().__init__(self)
	
		except Exception as e:
			print(type(e))
			print(e)
			sys.exit(0)
		
		log = logging.getLogger('Modulo de Gerenciamento')
		self.Jobs = super().Jobs()
		self.inicializando(self.Controle.servicos)#So precisa de modulos, so vai modulos!
	
	def inicializando(self, modulos):
		
		try:
			self.Jobs['WATCH'].start()
			
			if modulos.SMS.init is True:
				self.Jobs['SMS'].start()
				modulos.SMS.init_time =datetime.datetime.now()
				
			
			if modulos.SRC.init is True:
				Jobs['SRC'].start()
				modulos.SRC.init_time = datetime.datetime.now()
				
				
			if modulos.SDU.init is True:
				self.ValidacaoEUpdate(self.Controle.servicos.SVC, self.Controle.servicos.SDU)


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
				"message":json.dumps(sys.exc_info()),
				"erro":True,
				"comments":"Arrumar uma forma de identificar melhor tais erros...",
				"time":datetime.datetime.now()
				}
				self.callback(e)
			#Quando a função lança uma exception o fluxo volta para ca
			print("INITALIZE -__init__ Oops!{0} occured.".format(sys.exc_info()[0]))
			#sys.exit()

	def ValidacaoEUpdate(self, SVC_c, SDU_c):
		
			while SVC_c.keepAlive is True:
				if SVC_c.firstTime:
						SVC_c.init_time =datetime.datetime.now()
						
						self.Jobs['SVC'].start()
						SVC_c.firstTime= False
						self.Jobs['SVC'].join()
						SVC_c.lasttimerunning = datetime.datetime.now()
						if not self.Jobs['SVC'].isAlive():
							try:
								if SDU_c.init is True:
									SDU_c.init_time = datetime.datetime.now()
									self.Jobs['SDU'].start()
									self.Jobs['SDU'].join() #Quando a função termina com return o fluxo volta para o join 
									SDU_c.lasttimerunning = datetime.datetime.now()
									sleep(SVC_c.delay)
							except SystemExit:
								pass
							except not SystemExit:
								print("Oops!{0} occured -- VEU :148.".format(sys.exc_info()))
				elif (time.time() - datetime.datetime.timestamp(SVC_c.lasttimerunning))>(SVC_c.delay):
					if ( SVC_c.keepAlive is True) and (not self.Jobs['SVC'].isAlive()):
						
						self.Jobs['SVC'] = threading.Thread(target=self.servicoDeValidacao.start, name="SVC")
						SVC_c.init_time =datetime.datetime.now()
						self.Jobs['SVC'].start()
						self.Jobs['SVC'].join()
						SVC_c.lasttimerunning = datetime.datetime.now()
						if( not self.Jobs['SDU'].isAlive()) and (SDU_c.keepAlive is True):
							try:
								self.Jobs['SDU'] = threading.Thread(target=self.DataUpdate.start, name="SDU")
								SVC_c.init_time = datetime.datetime.now()
								self.Jobs['SDU'].start()
								self.Jobs['SDU'].join()
								SVC_c.lasttimerunning = datetime.datetime.now()
								SVC_c.nextrun = datetime.datetime.fromtimestamp(time.time()+SVC_c.delay)
								sleep(SVC_c.delay)
							except SystemExit:
								pass
							except not SystemExit:
								print("Oops!{0} occured -- VEU :148.".format(sys.exc_info()))

	def verifica(self):
		if not self.Jobs['WATCH'].isAlive():
			self.Jobs['WATCH'] = threading.Thread(target=self.Watch.start, name="WATCH")
			self.Jobs['WATCH'].start()
		if (not self.Jobs['SMS'].isAlive()) and (self.Controle.servicos.SMS.keepAlive is True):
			self.Jobs['SMS'] = threading.Thread(target=self.SMS.start, name="SMS",args=(lambda:self.Controle.servicos.SMS.stop,))
			self.Jobs['SMS'].start()
			self.Controle.servicos.SMS.init_time =datetime.datetime.now()
		if (not self.Jobs['SRC'].isAlive()) and (self.Controle.servicos.SRC.keepAlive is True):
			self.Jobs['SRC'] = threading.Thread(target=self.recuperacaoDeCarrinhos.start, name="SRC",args=(lambda:self.Controle.servicos.SRC.stop,))
			self.Jobs['SRC'].start()
			self.Controle.servicos.SRC.init_time = datetime.datetime.now()
	
	def finaliza(self, servico):
		if "sdu" in servico:
			if self.Jobs['SDU'].isAlive():
				self.Controle.servicos.SDU.keepAlive=False
				self.Controle.servicos.SDU.stop=True
				self.Jobs["SDU"].raise_exception()
		if "svc" in servico:
			if self.Jobs['SVC'].isAlive():
				self.Controle.servicos.SDU.keepAlive=False
				self.Controle.servicos.SDU.stop=True
				self.Jobs["SVC"].raise_exception()
	
	def run(self,s):
		if "src" in s:
				loop = asyncio.new_event_loop()
				return_value = loop.run_until_complete(self.recuperacaoDeCarrinhos.runNow())
			
				return return_value
		if "sms" in s:
			loop = asyncio.new_event_loop()
			return_value = loop.run_until_complete(self.SMS.runNow())
			return return_value

	def inicia(self, servico):
		if "sdu" in servico:
			if self.Controle.servicos.SDU.firstTime:
				self.Controle.servicos.SDU.init_time =datetime.datetime.now()
				self.Controle.servicos.SDU.nextrun=datetime.datetime.fromtimestamp(time.time()+float(self.Config.get("SVC","delay")))
				self.Controle.servicos.SDU.keepAlive=True
				self.Controle.servicos.SDU.stop=False
				self.Jobs['SDU'] = threading.Thread(target=self.DataUpdate.start, name="SDU")
				self.Jobs['SDU'].start()
			else:
				
				
				self.Controle.servicos.SDU.keepAlive=True
				self.Controle.servicos.SDU.stop=False
				self.Jobs['SDU'] = threading.Thread(target=self.DataUpdate.start, name="SDU")
				self.Jobs['SDU'].start()

		if "svc" in servico:
			if self.Controle.servicos.SVC.firstTime:
					self.Controle.servicos.SVC.init_time =datetime.datetime.now()
					self.Controle.servicos.SVC.nextrun=datetime.datetime.fromtimestamp(time.time()+float(self.Config.get("SVC","delay")))
					self.Controle.servicos.SVC.keepAlive=True
					self.Controle.servicos.SVC.stop=False
					self.Jobs['SVC'] = threading.Thread(target=self.servicoDeValidacao.start, name="SVC")
					self.Jobs['SVC'].start()
			else:
				self.Controle.servicos.SDU.nextrun=datetime.datetime.fromtimestamp(time.time()+float(self.Config.get("SVC","delay")))
				self.Controle.servicos.SVC.keepAlive=True
				self.Controle.servicos.SVC.stop=False
				self.Jobs['SVC'] = threading.Thread(target=self.servicoDeValidacao.start, name="SVC")
				self.Jobs['SVC'].start()
		if "sms" in servico:
			self.Controle.servicos.SMS.keepAlive=True
			self.Controle.servicos.SMS.stop=False
			self.Jobs['SMS'] = threading.Thread(target=self.SMS.start, name="SMS", args=(lambda:self.Controle.servicos.SMS.stop,))
			self.Jobs['SMS'].start()
		if "src" in servico:
			self.Controle.servicos.SRC.keepAlive=True
			self.Controle.servicos.SRC.stop=False
			self.Jobs['SRC'] = threading.Thread(target=self.recuperacaoDeCarrinhos.start, name="SRC", args=(lambda:self.Controle.servicos.SRC.stop,))
			self.Jobs['SRC'].start()

	def callback(self,e):
		
		if e['class'] == 'SMS':
			if e['status']== -1:
				self.Logs(e)
			elif e['status']== 0:
				self.Logs(e)
			elif e['status']== 1:
				self.Exceptions(e)
			elif e['status']== 2:
				self.Exceptions(e)
			elif e['status']== 3:
				self.Exceptions(e)
			elif e['status']== 4:
				self.Exceptions(e)
			elif e['status']== 5:
				self.Logs(e)
			pass
		elif e['class'] == 'recuperacaoDeCarrinhos':
			if e['status']== -1:
				self.Logs(e)
			elif e['status']== 0:
				self.Logs(e)
			elif e['status']== 1:
				self.Exceptions(e)
			elif e['status']== 2:
				self.Exceptions(e)
			elif e['status']== 3:
				self.Exceptions(e)
			elif e['status']== 4:
				self.Exceptions(e)
			elif e['status']== 5:
				self.Logs(e)
			pass
		elif e['class'] == 'servicoDeValidacao':
			if e['status']== -1:
				self.Logs(e)
			elif e['status']== 0:
				self.Logs(e)
				return 
			elif e['status']== 1:
				self.Exceptions(e)
			elif e['status']== 2:
				self.Exceptions(e)
			elif e['status']== 3:
				self.Exceptions(e)
			elif e['status']== 4:
				self.Exceptionse(e)
			elif e['status']== 5:
				self.Logs(e)
			pass
			
		elif e['class'] == 'DataUpdate':
			if e['status']== -1:
				self.Logs(e)
			elif e['status']== 0:
				self.Logs(e)
				return
			elif e['status']== 1:
				self.Exceptions(e)
			elif e['status']== 2:
				self.Exceptions(e)
			elif e['status']== 3:
				self.Exceptions(e)
			elif e['status']== 4:
				self.Exceptions(e)
			elif e['status']== 5:
				self.Logs(e)
			pass
		#DAS API'S	
		elif e['class'] == 'Server':
			if e['status']== -1:
				self.Logs(e)
			elif e['status']== 0:
				self.Logs(e)
				self.Kill()
			elif e['status']== 1:
				self.Exceptions(e)
			elif e['status']== 2:
				self.Exceptions(e)
			elif e['status']== 3:
				self.Exceptions(e)
			elif e['status']== 4:
				self.Exceptions(e)
			elif e['status']== 5:
				self.Logs(e)
			pass
		elif e['class'] == 'MockServer':
			if e['status']== -1:
				self.Logs(e)
			elif e['status']== 0:
				self.Logs(e)
			elif e['status']== 1:
				self.Exceptions(e)
			elif e['status']== 2:
				self.Exceptions(e)
			elif e['status']== 3:
				self.Exceptions(e)
			elif e['status']== 4:
				self.Exceptions(e)
			elif e['status']== 5:
				self.Logs(e)
			pass
		

		#DOS MODULOS
		elif e['class'] == 'CPF':
			if e['status']== -1:
				self.Logs(e)
			elif e['status']== 0:
				self.Logs(e)
			elif e['status']== 1:
				self.Exceptions(e)
			elif e['status']== 2:
				self.Exceptions(e)
			elif e['status']== 3:
				self.Exceptions(e)
			elif e['status']== 4:
				self.Exceptions(e)
			elif e['status']== 5:
				self.Logs(e)
			pass
		elif e['class'] == 'DB':
			if e['status']== -1:
				self.Logs(e)
			elif e['status']== 0:
				self.Logs(e)
			elif e['status']== 1:
				self.Exceptions(e)
			elif e['status']== 2:
				self.Exceptions(e)
			elif e['status']== 3:
				self.Exceptions(e)
			elif e['status']== 4:
				self.Exceptions(e)
			elif e['status']== 5:
				self.Logs(e)
			pass
		elif e['class'] == 'Relatorios':
			if e['status']== -1:
				self.Logs(e)
			elif e['status']== 0:
				self.Logs(e)
			elif e['status']== 1:
				self.Exceptions(e)
			elif e['status']== 2:
				self.Exceptions(e)
			elif e['status']== 3:
				self.Exceptions(e)
			elif e['status']== 4:
				self.Exceptions(e)
			elif e['status']== 5:
				self.Logs(e)
			pass

	def Exceptions(self, e):
		""" TODO: 
		! revisar erros e execeções!
		"""
		
		#DOS SERVIÇOS
		if e['class'] == 'SMS':	
			if e['status']== 1:
				e["Controle"]=self.Controle.servicos.SMS.__dict__
				self.Controle.servicos.SMS.keepAlive = False
				self.Controle.servicos.SMS.stop = True
				self.Logs(e)
				self.Notificar(e)
				self.Logs(e)

			elif e['status']== 2:
			
				self.Logs(e)
				
				
			elif e['status']== 3:
				e["Controle"]=self.Controle.servicos.SMS.__dict__
				self.Controle.servicos.SMS.keepAlive = False
				self.Controle.servicos.SMS.stop = True
				self.Logs(e)
				self.Notificar(e)
				self.Logs(e)
				
			elif e['status']== 4:
				e["Controle"]=self.Controle.servicos.SMS.__dict__
				self.Controle.servicos.SMS.keepAlive = False
				self.Controle.servicos.SMS.stop = True
				self.Logs(e)
				self.Notificar(e)
				self.Logs(e)
				
				
			pass
		elif e['class'] == 'recuperacaoDeCarrinhos':
			
			
			if e['status']== 1:
				self.Logs(e)

			elif e['status']== 2:
				e["Controle"]=self.controle['SRC']
				self.controle['SRC']['keepAlive'] = False
				self.Logs(e)
				self.Notificar(e)
				
			elif e['status']== 3:
				self.controle['SRC']['keepAlive'] = False
				e["Controle"]=self.controle['SRC']
				self.Logs(e)
				self.Notificar(e)
				
			elif e['status']== 4:
				self.controle['SRC']['keepAlive'] = False
				e["Controle"]=self.controle['SRC']
				self.Logs(e)
				self.Notificar(e)
				sys.exit()
				
			pass
		elif e['class'] == 'servicoDeValidacao':
			if e['status']== 1:
				self.Logs(e)
			elif e['status']== 2:
				self.controle['SVC']['keepAlive'] = False
				e["Controle"]=self.controle['SVC']
				self.Logs(e)
				self.Notificar(e)
			
			elif e['status']== 3:
				self.controle['SVC']['keepAlive'] = False
				e["Controle"]=self.controle['SVC']
				self.Logs(e)
				self.Notificar(e)
				
			elif e['status']== 4:
				self.controle['SVC']['keepAlive'] = False
				e["Controle"]=self.controle['SVC']
				self.Logs(e)
				self.Notificar(e)
				sys.exit()
			pass
		elif e['class'] == 'DataUpdate':
			if e['status']== 1:
				self.Logs(e)
			elif e['status']== 2:
				self.controle['SDU']['keepAlive'] = False
				e["Controle"]=self.controle['SDU']
				self.Logs(e)
				self.Notificar(e)
			
			elif e['status']== 3:
				self.controle['SDU']['keepAlive'] = False
				e["Controle"]=self.controle['SDU']
				self.Logs(e)
				self.Notificar(e)
			
			elif e['status']== 4:
				self.controle['SDU']['keepAlive'] = False
				e["Controle"]=self.controle['SDU']
				self.Logs(e)
				self.Notificar(e)
				sys.exit()
			pass

		#DAS API'S	
		elif e['class'] == 'Server':
			if e['status']== 1:
				self.Logs(e)
			elif e['status']== 2:
				self.Logs(e)
			elif e['status']== 3:
				self.Logs(e)
			elif e['status']== 4:
				self.Logs(e)
				
			pass
		elif e['class'] == 'MockServer':
			if e['status']== 1:
				self.Logs(e)
			elif e['status']== 2:
				self.Logs(e)
			elif e['status']== 3:
				self.Logs(e)
			elif e['status']== 4:
				self.Logs(e)
			
			pass
		

		#DOS MODULOS
		elif e['class'] == 'CPF':
			if e['status']== 1:
				self.Logs(e)
			elif e['status']== 2:
				self.Logs(e)
			elif e['status']== 3:
				self.Logs(e)
			elif e['status']== 4:
				self.Logs(e)
				
			pass
		elif e['class'] == 'DB':
			if e['status']== 1:
				self.Logs(e)
			elif e['status']== 2:
				self.Logs(e)
				self.Notificar(e)
				sys.exit()

			elif e['status']== 3:
				self.Logs(e)
				self.Notificar(e)
				sys.exit()
			elif e['status']== 4:
				self.Logs(e)
				self.Notificar(e)
				sys.exit()
			pass
		elif e['class'] == 'Relatorios':
			if e['status']== 1:
				self.Logs(e)
			elif e['status']== 2:
				self.Logs(e)
			elif e['status']== 3:
				self.Logs(e)
			elif e['status']== 4:
				self.Logs(e)
				self.Notificar(e)
				sys.exit()
			pass

	def Logs(self, e):
		e["ENV"] = self.Config.get("KEY", "env")
		log = logging.getLogger('{message:{fill}^{width}}'.format(message=e['class']+"."+e['metodo'],fill=" ",align="^",width=50	))
		for msg in e['message']:
			if msg is not None and msg != "":
				log.info(" {0} ".format(msg))
		if e['comments']!="" and e['comments'] is not None:
			log.info(" {0} ".format(e['comments']))

	def Notificar(self, e):
		e["AMBIENTE"]= self.Controle.Key.env
		administradores = [
			'47997619694',
			'47988948000',
			'47991566969'
		]
		log = logging.getLogger("Manager")
		log.info( '{0}[!]Notificando Administradores!'.format(datetime.datetime.now()))
		log.info(e)
		
		__api_key = '3aa20522-7c0a-4562-b25d-70ffc3f27f8e'
		textmessage_service = TextMessageService(__api_key)
		
		
		try:
			result = textmessage_service.send('MS_.Manager - Error', json.dumps(e), administradores)
			log.info( '{0}[!]Notificação de Falha enviada!!'.format(datetime.datetime.now()))
		except :
			log.info( '{0}[!!!]Não foi ossivel notificar!'.format(datetime.datetime.now()))
			
			
		pass


	
if __name__ == "__main__":
	pass
	M = Manager()
	
	