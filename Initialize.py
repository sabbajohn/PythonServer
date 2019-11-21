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
from services.recupecaoDeCarrinhos import recuperacaoDeCarrinhos



class Initialize:
	
	def __init__(self,M):
		
		self.USER = getpass.getuser()
		
		#Definindo objeto dos Serviços
		self.SMS = SMS(M)
		self.recuperacaoDeCarrinhos = recuperacaoDeCarrinhos(M)
		self.DataUpdate = DataUpdate(M)
		self.servicoDeValidacao = servicoDeValidacao(M)
		self.Watch = Watch(M)

		#Definindo objeto das API's
		
		self.job_sms = threading.Thread(target=self.SMS.start, name="SMS", args=(lambda:M.Variaveis_de_controle["SMS"]["stop"],))
		self.job_src = threading.Thread(target=self.recuperacaoDeCarrinhos.start, name="SRC", args=(lambda:M.Variaveis_de_controle["SRC"]["stop"],))
		self.job_servico_de_validacao = threading.Thread(target=self.servicoDeValidacao.start, name="SVC")
		self.job_dataupdate = threading.Thread(target=self.DataUpdate.start, name="SDU")
		self.job_watch = threading.Thread(target=self.Watch.start, name="WATCH")
		# Inicializando
	
	def Jobs(self):
		jobs = {
			'SMS': self.job_sms,
			'SVC': self.job_servico_de_validacao,
			'SDU': self.job_dataupdate,
			'WATCH':self.job_watch,
			'SRC':self.job_src
		}
		return jobs
	
		
		
