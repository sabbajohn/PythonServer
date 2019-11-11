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
from servers import *
import Initialize
class Manager(object):
	# Status
	# -1 - NIVEL LOG INICIALIZANDO
	#  0 - NIVEL LOG TAREFA CONCLUIDA
	#  1 - NIVEL EXCEPT - ERRO
	#  2 - NIVEL EXCEPT - WARNING
	#  3 - NIVEL EXCEPT - DIE 
	#  4 - NIVEL EXCEPT - ATTETION (Erro não tratado) 
	#  5 - NIVEL INFO - ""
	#	
	# e = {
	#	"class": "Nome da Class ou Módulo"
	#	"metodo": "Nome do metodo que retornou a mensagem"
	#	"status":-1 - 5
	#	"erro":	True or False
	#	"comments":"Comentarios livre do programador"
	#	"time": datetime.datetime.now()
	# 	}
	#
	


	def __init__(self):

		log = logging.getLogger('Modulo de Gerenciamento')

		logging.basicConfig(
			filename='/home/{0}/PythonServer/logs/Manager.log'.format(self.USER),
			filemode='a+',
			level=logging.INFO,
			format='PID %(process)5s %(name)18s: %(message)s',
			#stream=sys.stderr,
		)
		Jobs = Initialize.Jobs()
		pass

	def callback(self,e):
		if self.exception['class'] == 'SMS':
			
			if self.exception['status']== 0:

				pass
			elif self.exception['status']== 1:
				pass
			elif self.exception['status']== 2:
				pass
			elif self.exception['status']== 3:
				pass
			elif self.exception['status']== 4:
				""" SEJA O QUE DEUS QUISER! """
				pass
			pass
		elif self.exception['class'] == 'Validacao':
			if self.exception['status']== 0:
				pass
			elif self.exception['status']== 1:
				pass
			elif self.exception['status']== 2:
				pass
			elif self.exception['status']== 3:
				pass
			elif self.exception['status']== 4:
				pass
			pass
		elif self.exception['class'] == 'DataUpdate':
			if self.exception['status']== 0:
				pass
			elif self.exception['status']== 1:
				pass
			elif self.exception['status']== 2:
				pass
			elif self.exception['status']== 3:
				pass
			elif self.exception['status']== 4:
				pass
			pass

		#DAS API'S	
		elif self.exception['class'] == 'Server':
			if self.exception['status']== 0:
				pass
			elif self.exception['status']== 1:
				pass
			elif self.exception['status']== 2:
				pass
			elif self.exception['status']== 3:
				pass
			elif self.exception['status']== 4:
				pass
			pass
		elif self.exception['class'] == 'MockServer':
			if self.exception['status']== 0:
				pass
			elif self.exception['status']== 1:
				pass
			elif self.exception['status']== 2:
				pass
			elif self.exception['status']== 3:
				pass
			elif self.exception['status']== 4:
				pass
			pass
		

		#DOS MODULOS
		elif self.exception['class'] == 'CPF':
			if self.exception['status']== 0:
				pass
			elif self.exception['status']== 1:
				pass
			elif self.exception['status']== 2:
				pass
			elif self.exception['status']== 3:
				pass
			elif self.exception['status']== 4:
				pass
			pass
		elif self.exception['class'] == 'db':
			if self.exception['status']== 0:
				pass
			elif self.exception['status']== 1:
				pass
			elif self.exception['status']== 2:
				pass
			elif self.exception['status']== 3:
				pass
			elif self.exception['status']== 4:
				pass
			pass
		elif self.exception['class'] == 'Relatorios':
			if self.exception['status']== 0:
				pass
			elif self.exception['status']== 1:
				pass
			elif self.exception['status']== 2:
				pass
			elif self.exception['status']== 3:
				pass
			elif self.exception['status']== 4:
				pass
			pass

	
	def Exceptions(self, e):
	

		self.exception = e

		
		#DOS SERVIÇOS
		if self.exception['class'] == 'SMS':
			
			if self.exception['status']== 0:

				pass
			elif self.exception['status']== 1:
				pass
			elif self.exception['status']== 2:
				pass
			elif self.exception['status']== 3:
				pass
			elif self.exception['status']== 4:
				""" SEJA O QUE DEUS QUISER! """
				pass
			pass
		elif self.exception['class'] == 'Validacao':
			if self.exception['status']== 0:
				pass
			elif self.exception['status']== 1:
				pass
			elif self.exception['status']== 2:
				pass
			elif self.exception['status']== 3:
				pass
			elif self.exception['status']== 4:
				pass
			pass
		elif self.exception['class'] == 'DataUpdate':
			if self.exception['status']== 0:
				pass
			elif self.exception['status']== 1:
				pass
			elif self.exception['status']== 2:
				pass
			elif self.exception['status']== 3:
				pass
			elif self.exception['status']== 4:
				pass
			pass

		#DAS API'S	
		elif self.exception['class'] == 'Server':
			if self.exception['status']== 0:
				pass
			elif self.exception['status']== 1:
				pass
			elif self.exception['status']== 2:
				pass
			elif self.exception['status']== 3:
				pass
			elif self.exception['status']== 4:
				pass
			pass
		elif self.exception['class'] == 'MockServer':
			if self.exception['status']== 0:
				pass
			elif self.exception['status']== 1:
				pass
			elif self.exception['status']== 2:
				pass
			elif self.exception['status']== 3:
				pass
			elif self.exception['status']== 4:
				pass
			pass
		

		#DOS MODULOS
		elif self.exception['class'] == 'CPF':
			if self.exception['status']== 0:
				pass
			elif self.exception['status']== 1:
				pass
			elif self.exception['status']== 2:
				pass
			elif self.exception['status']== 3:
				pass
			elif self.exception['status']== 4:
				pass
			pass
		elif self.exception['class'] == 'db':
			if self.exception['status']== 0:
				pass
			elif self.exception['status']== 1:
				pass
			elif self.exception['status']== 2:
				pass
			elif self.exception['status']== 3:
				pass
			elif self.exception['status']== 4:
				pass
			pass
		elif self.exception['class'] == 'Relatorios':
			if self.exception['status']== 0:
				pass
			elif self.exception['status']== 1:
				pass
			elif self.exception['status']== 2:
				pass
			elif self.exception['status']== 3:
				pass
			elif self.exception['status']== 4:
				pass
			pass

	def Logs(self, e):

		pass