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
from services import SMS, DataUpdate,servico_de_validacao
import Manager



class Initialize(object):
	
	def Initialize(self):
		
		#Definindo objeto dos Serviços
		self.SMS = SMS()
		self.DataUpdate = DataUpdate(self.Manager)
		self.servicoDeValidacao = servico_de_validacao(self.Manager)

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
			ValidacaoEUpdate()

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
	
if __name__ == "__main__":
	pass