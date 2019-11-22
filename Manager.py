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
from Initialize import Initialize


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
		self.time() 
		logging.basicConfig(
			filename=self.Config.get("LOGS","manager_log"),
			filemode='a+',
			level=logging.INFO,
			format='%(asctime)s %(name)18s #> %(message)s',
			datefmt='%d-%m-%Y %H:%M:%S'
			#stream=sys.stderr,
		)
		log = logging.getLogger('Modulo de Gerenciamento')
		
		try:
			super().__init__(self)
		
		except Exception as e:
			print(type(e))
			print(e)
			sys.exit(0)
		
		self.Jobs = super().Jobs()
		self.inicializando(self.controle["modulos"])#So precisa de modulos, so vai modulos!
	
	
	def inicializando(self, controle):
		
		try:
			self.Jobs['WATCH'].start()
			
			if controle['SMS']['init'] is True:
				self.Jobs['SMS'].start()
				controle['SMS']['init_time'] =datetime.datetime.now()
				self.controle["modulos"] = controle
			
			if controle['SRC']['init'] is True:
				Jobs['SRC'].start()
				controle['SRC']['init_time'] = datetime.datetime.now()
				self.controle["modulos"] = controle
				
			if controle['SDU']['init'] is True:
				self.ValidacaoEUpdate(controle["SVC"], controle["SDU"])


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
		
			while SVC_c["keepAlive"] is True:
				if SVC_c['firstTime']:
						SVC_c['init_time'] =datetime.datetime.now()
						
						self.Jobs['SVC'].start()
						SVC_c['firstTime'] = False
						self.Jobs['SVC'].join()
						SVC_c['lasttimerunning'] = datetime.datetime.now()
						if not self.Jobs['SVC'].isAlive():
							try:
								if SDU_c["init"] is True:
									SDU_c['init_time'] = datetime.datetime.now()
									self.Jobs['SDU'].start()
									self.Jobs['SDU'].join() #Quando a função termina com return o fluxo volta para o join 
									SDU_c['lasttimerunning'] = datetime.datetime.now()
									sleep(self.controle['SVC']['delay'])
							except SystemExit:
								pass
							except not SystemExit:
								print("Oops!{0} occured -- VEU :148.".format(sys.exc_info()))
				elif (time.time() - time.mktime(datetime.datetime(SVC_c['lasttimerunning']).timetuple()))>(self.controle['SVC']['delay']):
					if ( SVC_c["keepAlive"] is True) and (not self.Jobs['SVC'].isAlive()):
						
						self.Jobs['SVC'] = threading.Thread(target=self.servicoDeValidacao.start, name="SVC")
						SVC_c['init_time'] =datetime.datetime.now()
						self.Jobs['SVC'].start()
						self.Jobs['SVC'].join()
						SVC_c['lasttimerunning'] = datetime.datetime.now()
						if( not self.Jobs['SDU'].isAlive()) and (SDU_c["keepAlive"] is True):
							try:
								self.Jobs['SDU'] = threading.Thread(target=self.DataUpdate.start, name="SDU")
								SVC_c['init_time'] = datetime.datetime.now()
								self.Jobs['SDU'].start()
								self.Jobs['SDU'].join()
								SVC_c['lasttimerunning'] = datetime.datetime.now()
								SVC_c['nextrun'] = datetime.datetime.fromtimestamp(time.time()+float(self.Config.get("SVC","delay")))
								sleep(self.controle['SVC']['delay'])
							except SystemExit:
								pass
							except not SystemExit:
								print("Oops!{0} occured -- VEU :148.".format(sys.exc_info()))

	def verifica(self):
		if not self.Jobs['WATCH'].isAlive():
			self.Jobs['WATCH'] = threading.Thread(target=self.Watch.start, name="WATCH")
			self.Jobs['WATCH'].start()
		if (not self.Jobs['SMS'].isAlive()) and (self.controle["SMS"]["keepAlive"] is True):
			self.Jobs['SMS'] = threading.Thread(target=self.SMS.start, name="SMS",args=(lambda:self.controle["SMS"]["stop"],))
			self.Jobs['SMS'].start()
			self.controle['SMS']['init_time'] =datetime.datetime.now()
		if (not self.Jobs['SRC'].isAlive()) and (self.controle["SRC"]["keepAlive"] is True):
			self.Jobs['SRC'] = threading.Thread(target=self.recuperacaoDeCarrinhos.start, name="SRC",args=(lambda:self.controle["SRC"]["stop"],))
			self.Jobs['SRC'].start()
			self.controle['SRC']['init_time'] = datetime.datetime.now()
	
	def finaliza(self, servico):
		if "sdu" in servico:
			if self.Jobs['SDU'].isAlive():
				self.controle["SDU"]["keepAlive"]=False
				self.controle["SDU"]["stop"]=True
				self.Jobs["SDU"].raise_exception()
		if "svc" in servico:
			if self.Jobs['SVC'].isAlive():
				self.controle["SDU"]["keepAlive"]=False
				self.controle["SDU"]["stop"]=True
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
			if self.controle["SDU"]['firstTime']:
				self.controle["SDU"]['init_time'] =datetime.datetime.now()
				self.controle["SDU"]["nextrun"]=datetime.datetime.fromtimestamp(time.time()+float(self.Config.get("SVC","delay")))
				self.controle["SDU"]["keepAlive"]=True
				self.controle["SDU"]["stop"]=False
				self.Jobs['SDU'] = threading.Thread(target=self.DataUpdate.start, name="SDU")
				self.Jobs['SDU'].start()
			else:
				
				
				self.controle["SDU"]["keepAlive"]=True
				self.controle["SDU"]["stop"]=False
				self.Jobs['SDU'] = threading.Thread(target=self.DataUpdate.start, name="SDU")
				self.Jobs['SDU'].start()

		if "svc" in servico:
			if self.controle["SVC"]['firstTime']:
					self.controle["SVC"]['init_time'] =datetime.datetime.now()
					self.controle["SVC"]["nextrun"]=datetime.datetime.fromtimestamp(time.time()+float(self.Config.get("SVC","delay")))
					self.controle["SVC"]["keepAlive"]=True
					self.controle["SVC"]["stop"]=False
					self.Jobs['SVC'] = threading.Thread(target=self.servicoDeValidacao.start, name="SVC")
					self.Jobs['SVC'].start()
			else:
				self.controle["SDU"]["nextrun"]=datetime.datetime.fromtimestamp(time.time()+float(self.Config.get("SVC","delay")))
				self.controle["SVC"]["keepAlive"]=True
				self.controle["SVC"]["stop"]=False
				self.Jobs['SVC'] = threading.Thread(target=self.servicoDeValidacao.start, name="SVC")
				self.Jobs['SVC'].start()
		if "sms" in servico:
			self.controle["SMS"]["keepAlive"]=True
			self.controle["SMS"]["stop"]=False
			self.Jobs['SMS'] = threading.Thread(target=self.SMS.start, name="SMS", args=(lambda:self.controle["SMS"]["stop"],))
			self.Jobs['SMS'].start()
		if "src" in servico:
			self.controle["SRC"]["keepAlive"]=True
			self.controle["SRC"]["stop"]=False
			self.Jobs['SRC'] = threading.Thread(target=self.recuperacaoDeCarrinhos.start, name="SRC", args=(lambda:self.controle["SRC"]["stop"],))
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
	
		
		#DOS SERVIÇOS
		if e['class'] == 'SMS':
			
			
			if e['status']== 1:
				self.Logs(e)

			elif e['status']== 2:
				e["Controle"]=self.controle['SMS']
				self.controle['SMS']['keepAlive'] = False
				self.Logs(e)
				self.Notificar(e)
				
			elif e['status']== 3:
				self.controle['SMS']['keepAlive'] = False
				e["Controle"]=self.controle['SMS']
				self.Logs(e)
				self.Notificar(e)
				
			elif e['status']== 4:
				self.controle['SMS']['keepAlive'] = False
				e["Controle"]=self.controle['SMS']
				self.Logs(e)
				self.Notificar(e)
				sys.exit()
				
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
	
	