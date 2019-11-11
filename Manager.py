#!/usr/bin/python3
# coding: utf-8
import sys
import os
import logging
import time
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
import Initialize 
class Manager(object):
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
	


	def __init__(self, *args, **kwargs):
	 
		self.USER = getpass.getuser()
		log = logging.getLogger('Modulo de Gerenciamento')

		logging.basicConfig(
			filename='/home/{0}/PythonServer/logs/Manager.log'.format(self.USER),
			filemode='a+',
			level=logging.INFO,
			format='PID %(process)5s %(name)18s: %(message)s',
			#stream=sys.stderr,
		)
	def start(self):
		I =Initialize.Initialize()
		#I =Initialize.Initialize.__init__()

	
		
	def callback(self,e):
		
		if e['class'] == 'SMS':
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
		elif e['class'] == 'Validacao':
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
				self.Exceptionse(e)
			elif e['status']== 5:
				self.Logs(e)
			pass
			
		elif e['class'] == 'DataUpdate':
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
				e(e)
			elif e['status']== 2:
				e(e)
			elif e['status']== 3:
				e(e)
			elif e['status']== 4:
				e(e)
			elif e['status']== 5:
				self.Logs(e)
			pass
		elif e['class'] == 'db':
			if e['status']== -1:
				self.Logs(e)
			elif e['status']== 0:
				self.Logs(e)
			elif e['status']== 1:
				e(e)
			elif e['status']== 2:
				e(e)
			elif e['status']== 3:
				e(e)
			elif e['status']== 4:
				e(e)
			elif e['status']== 5:
				self.Logs(e)
			pass
		elif e['class'] == 'Relatorios':
			if e['status']== -1:
				self.Logs(e)
			elif e['status']== 0:
				self.Logs(e)
			elif e['status']== 1:
				e(e)
			elif e['status']== 2:
				e(e)
			elif e['status']== 3:
				e(e)
			elif e['status']== 4:
				e(e)
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
				self.Kill()
			pass
		elif e['class'] == 'Validacao':
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
				self.Kill()
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
				self.Kill()
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
				self.Kill()
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
				self.Kill()
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
				self.Kill()
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
	M.start()
	sys.exit(0)