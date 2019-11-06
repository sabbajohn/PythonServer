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
USER = getpass.getuser()
from Class import *
from servers import *
from services import SMS, DataUpdate, servico_de_validacao


if sys.version_info[0] < 3:

	raise Exception("[!]Must be using Python 3, You can install it using: # apt-get install python3")
try:
   import asyncio
	
except:
	try:
		comando = os.system
		comando('sudo pip3 install asyncio')
		print('[!] Tentando Instalar as Dependencias')	
	except:
		if IOError:	
			sys.exit("[!] Please install the asyncio library: sudo pip3 install asyncio")
		else:
			sleep(7) 
			comando('python3 servico_de_validacao.py')

try:
   import aiohttp
except:
	try:
		comando = os.system
		comando('sudo pip3 install aiohttp')
		print('[!] Tentando Instalar as Dependencias')
	except:

		if IOError:	
			sys.exit("[!] Please install the aiohttp library: sudo pip3 install aiohttp")	
		
		else:  
			sleep(10)   
			comando('python3 servico_de_validacao.py')	
			
try:
   import mysql.connector
except:
	try:
		comando = os.system
		comando('sudo pip3 install mysql')
		print('[!] Tentando Instalar as Dependencias')
	except:
		if IOError:	
			sys.exit("[!] Please install the mysql library: sudo pip3 install mysql")	
		
		else:  
			sleep(10)   
			comando('python3 servico_de_validacao.py')	
			

try:
  from aiofile import AIOFile, LineReader, Writer

except:
	try:
			
		comando = os.system
		comando('sudo pip3 install aiofile')
		print('[!] Tentando Instalar as Dependencias')
	except:

		if IOError:	
			sys.exit("[!] Please install the aiofile library: sudo pip3 install aiofile")	
		
		else:  
			sleep(10)   
			comando('python3 servico_de_validacao.py')	

class Manager(object):
	def __init__(self, *args, **kwargs):
	 super().__init__(*args, **kwargs)
	 logging.basicConfig(
		filename='/home/{0}/PythonServer/logs/Manager.log'.format(self.USER),
		filemode='a+',
		level=logging.INFO,
		format='PID %(process)5s %(name)18s: %(message)s',
		#stream=sys.stderr,
 		)

	def Initialize(self):
		
		#Definindo objeto dos Serviços
		self.SMS = SMS()
		self.DataUpdate = DataUpdate()
		self.servicoDeValidacao = servico_de_validacao()

		#Definindo objeto das API's
		
		self.isFirstTme={
			"servico_de_validacao":True,
			"dataupdate":True
		}
		self.job_sms = threading.Thread(target=self.SMS.start)
		self.job_servico_de_validacao = threading.Thread(target=self.servicoDeValidacao.start)
		self.job_dataupdate = threading.Thread(target=self.DataUpdate.start)

		# Inicializando
		try:
			self.job_sms.start()

		except:
			sys.exit("Oops!",sys.exc_info()[0],"occured.")

 	def ValidacaoEUpdate(self):
		 while True:
			if self.isFirstTme['servico_de_validacao']:
					self.job_servico_de_validacao.start()
					self.isFirstTme['servico_de_validacao'] = False
					self.job_servico_de_validacao.join()
					if not self.job-servico_de_validacao.isAlive():
						self.job_dataupdate.start()
						self.job_dataupdate.join()


			else:

				if not self.job-servico_de_validacao.isAlive():
					self.job_servico_de_validacao.start()
					self.job_servico_de_validacao.join()
					if not self.job_dataupdate.isAlive():
						self.job_dataupdate.start()
						self.job_dataupdate.join()
						sleep(6000)

	def Exceptions(self, e):
		log = logging.getLogger('Exceptions')

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



if __name__ == "__main__":
	M = Manager()
	M.Initialize()