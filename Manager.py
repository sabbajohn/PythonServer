#!/usr/bin/python3
# coding: utf-8
import sys
import os
import logging
import time
import configparser
import socket
from datetime import date
import json
import threading
from  urllib import request, parse
from time import sleep
import datetime
import concurrent.futures
import asyncio.coroutines
import getpass
from utils.db import DB
from comtele_sdk.textmessage_service import TextMessageService

#from servers import server
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
	
		self.cfg()
		logging.basicConfig(
			filename=self.Config.get("LOGS","manager_log"),
			filemode='a+',
			level=logging.INFO,
			format='%(asctime)s %(name)18s: %(message)s',
			datefmt='%d-%m-%Y %H:%M:%S'
			#stream=sys.stderr,
		)
		log = logging.getLogger('Modulo de Gerenciamento')
		
		
		self.Variaveis_de_controle = {
			"SMS":{
				"init": self.Config.getboolean("SMS","sms_init"),
				"init_time":None,
				"delay":None,
				"keepAlive": True,
				"lasttimerunning":None,
				"nextrun":None,
				"firstTime":True,
				"stop":False
			},
			"SVC":{
				"init": self.Config.getboolean("SVC","svc_init"),
				"delay":float(self.Config.get("SVC","delay")),
				"init_time":None,
				"keepAlive": True,
				"lasttimerunning":None,
				"nextrun":None,
				"firstTime":True,
				"stop":False
				
			},
			"SDU":{

				"init": self.Config.getboolean("SDU","sdu_init"),
				"init_time":None,
				"delay":None,
				"keepAlive": True,
				"lasttimerunning":None,
				"nextrun":None,
				"firstTime":True,
				"stop":False
			},
			"SRC":{

				"init": self.Config.getboolean("SRC","src_init"),
				"init_time":None,
				"delay":float(self.Config.get("SRC","delay")),
				"keepAlive": True,
				"lasttimerunning":None,
				"nextrun":None,
				"firstTime":True,
				"stop":False
			}
		}
		try:

			self.database = DB(self)
			super().__init__(self)
		except Exception as err:
				if "KILL_ALL" in err.args[0]:
					sys.exit()
				else:
					log.info(sys.exc_info())

		self.USER = getpass.getuser()
		
		self.Jobs = super().Jobs()
		self.inicializando()
	
	def cfg(self):
		self.Config =   configparser.ConfigParser()
		self.Config._interpolation = configparser.ExtendedInterpolation()
		DIR = os.getcwd()
		USER =getpass.getuser()
		self.Config.read("{0}/config/DEFAULT.ini".format(DIR))
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		IP = s.getsockname()[0]
		s.close()
		try:
			self.Config.set("KEY", "root", DIR)
			self.Config.set("KEY", "user",USER)
		except:
			print(sys.exc_info()[0])
		try:	
			if "237.29" in IP or "192.168." in IP :
				self.Config.set("KEY", "env", "BETA")

			elif "242.11" in IP or "242.52" in IP:
				self.Config.set("KEY", "env", "PROD")
			else:
				print("Não foi Possivel identivicar o ambiente!")
				try:
					print("Defina o tipo de Ambiente:")
					print("(1) BETA\n(2) PRODUCAO\n")
					env = input()
					
					if env == '1':
						self.Config.set("KEY", "env", "BETA")
					elif env == '2':
						self.Config.set("KEY", "env", "PROD")
					else:
						sys.exit("Opção invalida!")
				except:
					raise Exception("Não foi Possivel identivicar o ambiente!")
					print(sys.exc_info()[0])
					sys.exit("Erro ao definir env")
				""" self.Config_ENV.read("{0}/config/DEFAULT.ini".format(DIR)) """
	
		except:
			print(sys.exc_info()[0])
		
		with open("{0}/config/DEFAULT.ini".format(DIR), "w+") as configfile:		
			self.Config.write(configfile)

	def inicializando(self):

		try:
			self.Jobs['WATCH'].start()
			
			if self.Variaveis_de_controle['SMS']['init'] is True:
				self.Jobs['SMS'].start()
				self.Variaveis_de_controle['SMS']['init_time'] =str( datetime.datetime.now())
			
			if self.Variaveis_de_controle['SRC']['init'] is True:
				self.Jobs['SRC'].start()
				self.Variaveis_de_controle['SRC']['init_time'] =str( datetime.datetime.now())
				
			if self.Variaveis_de_controle['SDU']['init'] is True:
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
				"message":json.dumps(sys.exc_info()),
				"erro":True,
				"comments":"Arrumar uma forma de identificar melhor tais erros...",
				"time":datetime.datetime.now()
				}
				self.callback(e)
			#Quando a função lança uma exception o fluxo volta para ca
			print("INITALIZE -__init__ Oops!{0} occured.".format(sys.exc_info()[0]))
			#sys.exit()

	def ValidacaoEUpdate(self):
		
			while self.Variaveis_de_controle["SVC"]["keepAlive"] is True:
				if self.Variaveis_de_controle["SVC"]['firstTime']:
						self.Variaveis_de_controle["SVC"]['init_time'] =str( datetime.datetime.now())
						self.Jobs['SVC'].start()
						self.Variaveis_de_controle["SVC"]['firstTime'] = False
						self.Jobs['SVC'].join()
						self.Variaveis_de_controle["SVC"]['lasttimerunning'] = str(datetime.datetime.now())
						if not self.Jobs['SVC'].isAlive():
							try:
								if self.Variaveis_de_controle["SDU"]["init"] is True:
									self.Variaveis_de_controle["SDU"]['init_time'] = str(datetime.datetime.now())
									self.Jobs['SDU'].start()
									self.Jobs['SDU'].join() #Quando a função termina com return o fluxo volta para o join 
									self.Variaveis_de_controle["SDU"]['lasttimerunning'] = str(datetime.datetime.now())
									sleep(self.Variaveis_de_controle['SVC']['delay'])
							except SystemExit:
								pass
							except not SystemExit:
								print("Oops!{0} occured -- VEU :148.".format(sys.exc_info()))
				elif (time.time() - time.mktime(datetime.datetime.strptime(self.Variaveis_de_controle["SVC"]['lasttimerunning'], "%Y-%m-%d %H:%M:%S.%f").timetuple()))>(self.Variaveis_de_controle['SVC']['delay']):
					if ( self.Variaveis_de_controle["SVC"]["keepAlive"] is True) and (not self.Jobs['SVC'].isAlive()):
						
						self.Jobs['SVC'] = threading.Thread(target=self.servicoDeValidacao.start, name="SVC")
						self.Variaveis_de_controle["SVC"]['init_time'] =str(datetime.datetime.now())
						self.Jobs['SVC'].start()
						self.Jobs['SVC'].join()
						self.Variaveis_de_controle["SVC"]['lasttimerunning'] = str(datetime.datetime.now())
						if( not self.Jobs['SDU'].isAlive()) and (self.Variaveis_de_controle["SDU"]["keepAlive"] is True):
							try:
								self.Jobs['SDU'] = threading.Thread(target=self.DataUpdate.start, name="SDU")
								self.Variaveis_de_controle["SVC"]['init_time'] = str(datetime.datetime.now())
								self.Jobs['SDU'].start()
								self.Jobs['SDU'].join()
								self.Variaveis_de_controle["SVC"]['lasttimerunning'] = str(datetime.datetime.now())
								self.Variaveis_de_controle["SVC"]['nextrun'] = str(datetime.datetime.fromtimestamp(time.time()+float(self.Config.get("SVC","delay"))))
								sleep(self.Variaveis_de_controle['SVC']['delay'])
							except SystemExit:
								pass
							except not SystemExit:
								print("Oops!{0} occured -- VEU :148.".format(sys.exc_info()))

	def verifica(self):
		if not self.Jobs['WATCH'].isAlive():
			self.Jobs['WATCH'] = threading.Thread(target=self.Watch.start, name="WATCH")
			self.Jobs['WATCH'].start()
		if (not self.Jobs['SMS'].isAlive()) and (self.Variaveis_de_controle["SMS"]["keepAlive"] is True):
			self.Jobs['SMS'] = threading.Thread(target=self.SMS.start, name="SMS",args=(lambda:self.Variaveis_de_controle["SMS"]["stop"],))
			self.Jobs['SMS'].start()
			self.Variaveis_de_controle['SMS']['init_time'] =str( datetime.datetime.now())
		if (not self.Jobs['SRC'].isAlive()) and (self.Variaveis_de_controle["SRC"]["keepAlive"] is True):
			self.Jobs['SRC'] = threading.Thread(target=self.recuperacaoDeCarrinhos.start, name="SRC",args=(lambda:self.Variaveis_de_controle["SRC"]["stop"],))
			self.Jobs['SRC'].start()
			self.Variaveis_de_controle['SRC']['init_time'] =str( datetime.datetime.now())
	
	def finaliza(self, servico):
		if "sdu" in servico:
			if self.Jobs['SDU'].isAlive():
				self.Variaveis_de_controle["SDU"]["keepAlive"]=False
				self.Variaveis_de_controle["SDU"]["stop"]=True
				self.Jobs["SDU"].raise_exception()
		if "svc" in servico:
			if self.Jobs['SVC'].isAlive():
				self.Variaveis_de_controle["SDU"]["keepAlive"]=False
				self.Variaveis_de_controle["SDU"]["stop"]=True
				self.Jobs["SVC"].raise_exception()

	def inicia(self, servico):
		if "sdu" in servico:
			if self.Variaveis_de_controle["SDU"]['firstTime']:
				self.Variaveis_de_controle["SDU"]['init_time'] =str( datetime.datetime.now())
				self.Variaveis_de_controle["SDU"]["nextrun"]=str(datetime.datetime.fromtimestamp(time.time()+float(self.Config.get("SVC","delay"))))
				self.Variaveis_de_controle["SDU"]["keepAlive"]=True
				self.Variaveis_de_controle["SDU"]["stop"]=False
				self.Jobs['SDU'] = threading.Thread(target=self.DataUpdate.start, name="SDU")
				self.Jobs['SDU'].start()
			else:
				
				
				self.Variaveis_de_controle["SDU"]["keepAlive"]=True
				self.Variaveis_de_controle["SDU"]["stop"]=False
				self.Jobs['SDU'] = threading.Thread(target=self.DataUpdate.start, name="SDU")
				self.Jobs['SDU'].start()

		if "svc" in servico:
			if self.Variaveis_de_controle["SVC"]['firstTime']:
					self.Variaveis_de_controle["SVC"]['init_time'] =str( datetime.datetime.now())
					self.Variaveis_de_controle["SVC"]["nextrun"]=str(datetime.datetime.fromtimestamp(time.time()+float(self.Config.get("SVC","delay"))))
					self.Variaveis_de_controle["SVC"]["keepAlive"]=True
					self.Variaveis_de_controle["SVC"]["stop"]=False
					self.Jobs['SVC'] = threading.Thread(target=self.servicoDeValidacao.start, name="SVC")
					self.Jobs['SVC'].start()
			else:
				self.Variaveis_de_controle["SDU"]["nextrun"]=str(datetime.datetime.fromtimestamp(time.time()+float(self.Config.get("SVC","delay"))))
				self.Variaveis_de_controle["SVC"]["keepAlive"]=True
				self.Variaveis_de_controle["SVC"]["stop"]=False
				self.Jobs['SVC'] = threading.Thread(target=self.servicoDeValidacao.start, name="SVC")
				self.Jobs['SVC'].start()
		if "sms" in servico:
			self.Variaveis_de_controle["SMS"]["keepAlive"]=True
			self.Variaveis_de_controle["SMS"]["stop"]=False
			self.Jobs['SMS'] = threading.Thread(target=self.SMS.start, name="SMS", args=(lambda:self.Variaveis_de_controle["SMS"]["stop"],))
			self.Jobs['SMS'].start()
		if "src" in servico:
			self.Variaveis_de_controle["SRC"]["keepAlive"]=True
			self.Variaveis_de_controle["SRC"]["stop"]=False
			self.Jobs['SRC'] = threading.Thread(target=self.recuperacaoDeCarrinhos.start, name="SRC", args=(lambda:self.Variaveis_de_controle["SRC"]["stop"],))
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
		elif e['class'] == 'Watch':
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
				e["Controle"]=self.Variaveis_de_controle['SMS']
				self.Variaveis_de_controle['SMS']['keepAlive'] = False
				self.Logs(e)
				self.Notificar(e)
				
			elif e['status']== 3:
				self.Variaveis_de_controle['SMS']['keepAlive'] = False
				e["Controle"]=self.Variaveis_de_controle['SMS']
				self.Logs(e)
				self.Notificar(e)
				
			elif e['status']== 4:
				self.Variaveis_de_controle['SMS']['keepAlive'] = False
				e["Controle"]=self.Variaveis_de_controle['SMS']
				self.Logs(e)
				self.Notificar(e)
				sys.exit()
				
			pass
		elif e['class'] == 'Watch':
			
			
			if e['status']== 1:
				self.Logs(e)

			elif e['status']== 2:
				e["Controle"]=self.Variaveis_de_controle['SRC']
				self.Variaveis_de_controle['SRC']['keepAlive'] = False
				self.Logs(e)
				self.Notificar(e)
				
			elif e['status']== 3:
				self.Variaveis_de_controle['SRC']['keepAlive'] = False
				e["Controle"]=self.Variaveis_de_controle['SRC']
				self.Logs(e)
				self.Notificar(e)
				
			elif e['status']== 4:
				self.Variaveis_de_controle['SRC']['keepAlive'] = False
				e["Controle"]=self.Variaveis_de_controle['SRC']
				self.Logs(e)
				self.Notificar(e)
				sys.exit()
				
			pass
		elif e['class'] == 'servicoDeValidacao':
			if e['status']== 1:
				self.Logs(e)
			elif e['status']== 2:
				self.Variaveis_de_controle['SVC']['keepAlive'] = False
				e["Controle"]=self.Variaveis_de_controle['SVC']
				self.Logs(e)
				self.Notificar(e)
			
			elif e['status']== 3:
				self.Variaveis_de_controle['SVC']['keepAlive'] = False
				e["Controle"]=self.Variaveis_de_controle['SVC']
				self.Logs(e)
				self.Notificar(e)
				
			elif e['status']== 4:
				self.Variaveis_de_controle['SVC']['keepAlive'] = False
				e["Controle"]=self.Variaveis_de_controle['SVC']
				self.Logs(e)
				self.Notificar(e)
				sys.exit()
			pass
		elif e['class'] == 'DataUpdate':
			if e['status']== 1:
				self.Logs(e)
			elif e['status']== 2:
				self.Variaveis_de_controle['SDU']['keepAlive'] = False
				e["Controle"]=self.Variaveis_de_controle['SDU']
				self.Logs(e)
				self.Notificar(e)
			
			elif e['status']== 3:
				self.Variaveis_de_controle['SDU']['keepAlive'] = False
				e["Controle"]=self.Variaveis_de_controle['SDU']
				self.Logs(e)
				self.Notificar(e)
			
			elif e['status']== 4:
				self.Variaveis_de_controle['SDU']['keepAlive'] = False
				e["Controle"]=self.Variaveis_de_controle['SDU']
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

		log = logging.getLogger("\t{0}.{1}\t".format(e['class'], e['metodo']))
		for msg in e['message']:
			if msg is not None and msg != "":
				log.info("\t\t\t\t\t\t\t\t#>: {0}".format(msg))
		if e['comments']!="" and e['comments'] is not None:
			log.info("\t\t\t\t\\t\t\tt#>: {0}".format(e['comments']))

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
	
	