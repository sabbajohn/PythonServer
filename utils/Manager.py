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

class Manager:
	
		

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



