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

class Manager(object):
	
	

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
				log.info("SEJA O QUE DEUS QUISER! \n{0}".format(e))
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



