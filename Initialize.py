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

#from servers import server
from services.servicodevalidacao import servicoDeValidacao
from services.DataUpdate import DataUpdate
from services.SMS import SMS

USER = getpass.getuser()

class Initialize(object):
	
	def __init__(self):
		
		#Definindo objeto dos Serviços
		self.SMS = SMS()
		self.DataUpdate = DataUpdate()
		self.servicoDeValidacao = servicoDeValidacao()

		#Definindo objeto das API's
		
		self.isFirstTme={
			"servico_de_validacao":True,
			"dataupdate":True
		}
		self.job_sms = threading.Thread(target=self.SMS.start, name="SMS")
		self.job_servico_de_validacao = threading.Thread(target=self.servicoDeValidacao.start, name="SVC")
		self.job_dataupdate = threading.Thread(target=self.DataUpdate.start, name="SDU")

		# Inicializando
		try:
			self.job_sms.start()
			self.ValidacaoEUpdate()

		except:
			sys.exit("Oops!{0} occured.".format(sys.exc_info()[0]))

	def ValidacaoEUpdate(self):
		while True:
			if self.isFirstTme['servico_de_validacao']:
					self.job_servico_de_validacao.start()
					self.isFirstTme['servico_de_validacao'] = False
					self.job_servico_de_validacao.join()
					if not self.job_servico_de_validacao.isAlive():
						self.job_dataupdate.start()
						self.job_dataupdate.join()


			else:

				if not self.job_servico_de_validacao.isAlive():
					self.job_servico_de_validacao.start()
					self.job_servico_de_validacao.join()
					if not self.job_dataupdate.isAlive():
						self.job_dataupdate.start()
						self.job_dataupdate.join()
						sleep(6000)
	def Jobs(self):
		jobs = {
			"SMS":self.job_sms,
			"SVC":self.job_servico_de_validacao,
			"SDU":self.job_dataupdate
		}
		return jobs
		
		
