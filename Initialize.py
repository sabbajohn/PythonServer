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
import socket
import config
from services.servicodevalidacao import servicoDeValidacao
from services.DataUpdate import DataUpdate
from services.SMS import SMS
from services.watch import Watch



class Initialize:
	
	def __init__(self,M):
		
		self.USER = getpass.getuser()
		
		#Definindo objeto dos Serviços
		self.SMS = SMS(M)
		self.DataUpdate = DataUpdate(M)
		self.servicoDeValidacao = servicoDeValidacao(M)
		self.Watch = Watch(M)
		#Definindo objeto das API's
		
		self.job_sms = threading.Thread(target=self.SMS.start, name="SMS", args=(lambda:M.Variaveis_de_controle["SMS"]["stop"],))
		self.job_servico_de_validacao = threading.Thread(target=self.servicoDeValidacao.start, name="SVC")
		self.job_dataupdate = threading.Thread(target=self.DataUpdate.start, name="SDU")
		self.job_watch = threading.Thread(target=self.Watch.start, name="WATCH")
		# Inicializando
		

	def inicializando(self):
		try:
			self.job_sms.start()
			self.ValidacaoEUpdate()

		except:
			#Quando a função lança uma exception o fluxo volta para ca
			print("INITALIZE -__init__ Oops!{0} occured.".format(sys.exc_info()[0]))
	
	def ValidacaoEUpdate(self):
		while True:
			if self.isFirstTme['servico_de_validacao']:
					self.job_servico_de_validacao.start()
					self.isFirstTme['servico_de_validacao'] = False
					self.job_servico_de_validacao.join()
					if not self.job_servico_de_validacao.isAlive():
						try:
							self.job_dataupdate.start()
							self.job_dataupdate.join() #Quando a função termina com return o fluxo volta para o join 
						except:
							print("Oops!{0} occured.".format(sys.exc_info()[0]))
			else:

				if not self.job_servico_de_validacao.isAlive():
					self.job_servico_de_validacao = threading.Thread(target=self.servicoDeValidacao.start, name="SVC")
					self.job_servico_de_validacao.start()
					self.job_servico_de_validacao.join()
					if not self.job_dataupdate.isAlive():
						try:
							self.job_dataupdate = threading.Thread(target=self.DataUpdate.start, name="SDU")
							self.job_dataupdate.start()
							self.job_dataupdate.join()
							sleep(6000)
						except:
							print("Oops!{0} occured.".format(sys.exc_info()[0]))
	
	def Jobs(self):
		jobs = {
			'SMS': self.job_sms,
			'SVC': self.job_servico_de_validacao,
			'SDU': self.job_dataupdate,
			'WATCH':self.job_watch
		}
		return jobs
	
		
		
