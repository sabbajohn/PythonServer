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
			format='PID %(process)5s %(name)18s: %(message)s',
			#stream=sys.stderr,
		)
		self.database = DB()
		super().__init__(self)
		self.USER = getpass.getuser()
		log = logging.getLogger('Modulo de Gerenciamento')
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
			if "237.29" in IP:
				self.Config.set("KEY", "env", "BETA")

			elif "242.11" in IP or "242.52" in IP:
				self.Config.set("KEY", "env", "PROD")
			else:
				print("Não foi Possivel identivicar o ambiente!")
				try:
					print("Defina o tipo de Ambiente:")
					print("(1) BETA\n(2) PRODUCAO\n")
					""" env = input() """
					env='1'
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
			self.Jobs['SMS'].start()
			
			self.ValidacaoEUpdate()

		except:
			message = []
			message.append("Eita Juliana o forninho caiu!")
			e= {
			"class":"Só deus sabe",
			"metodo":"Se eu não sei nem a classe...",
			"status":4,
			"message":message,
			"erro":True,
			"comments":"Arrumar uma forma de identificar melhor tais erros...",
			"time":datetime.datetime.now()
		}
			
			self.callback(e)
			#Quando a função lança uma exception o fluxo volta para ca
			print("INITALIZE -__init__ Oops!{0} occured.".format(sys.exc_info()[0]))
	
	def ValidacaoEUpdate(self):
		while True:
			if self.isFirstTme['servico_de_validacao']:
					self.Jobs['SVC'].start()
					self.isFirstTme['servico_de_validacao'] = False
					self.Jobs['SVC'].join()
					if not self.Jobs['SVC'].isAlive():
						try:
							self.Jobs['SDU'].start()
							self.Jobs['SDU'].join() #Quando a função termina com return o fluxo volta para o join 
						except:
							print("Oops!{0} occured -- VEU :148.".format(sys.exc_info()))
			else:

				if not self.Jobs['SVC'].isAlive():
					self.Jobs['SVC'] = threading.Thread(target=self.servicoDeValidacao.start, name="SVC")
					self.Jobs['SVC'].start()
					self.Jobs['SVC'].join()
					if not self.Jobs['SDU'].isAlive():
						try:
							self.Jobs['SDU'] = threading.Thread(target=self.DataUpdate.start, name="SDU")
							self.Jobs['SDU'].start()
							self.Jobs['SDU'].join()
							sleep(6000)
						except:
							print("Oops!{0} occured -- VEU :148".format(sys.exc_info()))
	
	
	
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
		elif e['class'] == 'db':
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
				self.Logs(e)
			elif e['status']== 3:
				self.Logs(e)
			elif e['status']== 4:
				self.Logs(e)
				
			pass
		elif e['class'] == 'servicoDeValidacao':
			if e['status']== 1:
				self.Logs(e)
			elif e['status']== 2:
				self.Logs(e)
			elif e['status']== 3:
				self.Logs(e)
			elif e['status']== 4:
				self.Logs(e)
				self.Kill()
			pass
		elif e['class'] == 'DataUpdate':
			if e['status']== 1:
				self.Logs(e)
			elif e['status']== 2:
				self.Logs(e)
			elif e['status']== 3:
				self.Logs(e)
			elif e['status']== 4:
				self.Logs(e)
				
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
		elif e['class'] == 'db':
			if e['status']== 1:
				self.Logs(e)
			elif e['status']== 2:
				self.Logs(e)
			elif e['status']== 3:
				self.Logs(e)
			elif e['status']== 4:
				self.Logs(e)
				
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
				self.Kill()
			pass

	def Logs(self, e):

		log = logging.getLogger("{0}.{1}".format(e['class'], e['metodo']))
		log.info(e['status'])
		for msg in e['message']:
			log.info("{0}: {1}".format(e['time'], msg))
		if e['comments']!="":
			log.info("{0}: {1}".format(e['time'], e['comments']))

	def Kill(self):
		self.end()
if __name__ == "__main__":
	pass
	M = Manager()
	
	