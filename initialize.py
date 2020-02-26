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
import configparser
import concurrent.futures
import asyncio.coroutines
import getpass
import socket
import config
from services.SVC.servicodevalidacao import servicoDeValidacao
from services.SDU.DataUpdate import DataUpdate
from services.SMS.SMS import SMS
from services.WATCH.watch import Watch
from services.SRC.recupecaoDeCarrinhos import recuperacaoDeCarrinhos
from utils.db import DB
from controle import Controle
from termcolor import colored


class Initialize:
	
	def __init__(self,M):
		
		self.__cfg() 
		logging.basicConfig(
			filename=self.Config.get("LOGS","manager_log"),
			filemode='a+',
			level=logging.INFO,
			format='%(asctime)s %(name)18s #> %(message)s',
			datefmt='%d-%m-%Y %H:%M:%S'
			#stream=sys.stderr,
		)
		#Definindo objeto dos Serviços

		self.Controle = Controle(self)
		self.SMS_controle 			= self.Controle.servicos.SMS
		self.SVC_controle 			= self.Controle.servicos.SVC
		self.SDU_controle 			= self.Controle.servicos.SDU
		self.SRC_controle 			= self.Controle.servicos.SRC
	
		self.SMS_info 				= self.SMS_controle.getControle()
		self.SVC_info 				= self.SVC_controle.getControle()
		self.SDU_info 				= self.SDU_controle.getControle()
		self.SRC_info 				= self.SRC_controle.getControle()
		#API
		self.VIACEP_controle 		= self.Controle.API.viacep
		self.MANDRILL_controle 		= self.Controle.API.mandrill
		self.COMTELE_controle 		= self.Controle.API.comtele
		self.SOA_controle 			= self.Controle.API.soa
		self.HUBD_controle 			= self.Controle.API.hubd

		self.VIACEP_info			= self.VIACEP_controle.getControle()
		self.MANDRILL_info			= self.MANDRILL_controle.getControle()
		self.COMTELE_info			= self.COMTELE_controle.getControle()
		self.SOA_info				= self.SOA_controle.getControle()
		self.HUBD_info				= self.HUBD_controle.getControle()

		#LINK
		self.LINK_controle 			= self.Controle.LINK
		self.LINK_info				= self.Controle.LINK.getControle()
		
		
		self.Files					= self.Controle.files.getControle()
		self.servicos 				= self.Controle.servicos
		self.database 				= DB(self)
		self.Agenda 				= {"SMS":None,"SRC":None,"SVC":None}
		self.SMS 					= SMS(M)
		self.recuperacaoDeCarrinhos = recuperacaoDeCarrinhos(M)
		self.DataUpdate 			= DataUpdate(M)
		self.servicoDeValidacao 	= servicoDeValidacao(M)
		
		self.Watch 				= Watch(M)

		#Definindo objeto das API's
		
		self.job_sms 					= threading.Thread(target=self.SMS.start, name="SMS", args=(lambda:self.Controle.servicos.SMS.stop,))
		self.job_src 					= threading.Thread(target=self.recuperacaoDeCarrinhos.start, name="SRC", args=(lambda:self.Controle.servicos.SRC.stop,))
		self.job_servico_de_validacao	= threading.Thread(target=self.servicoDeValidacao.start, name="SVC")
		self.job_dataupdate 			= threading.Thread(target=self.DataUpdate.start, name="SDU")
		self.job_watch 					= threading.Thread(target=self.Watch.start, name="WATCH")
		# Inicializando

	def __cfg(self):
		
		DIR							= os.getcwd()
		USER						= getpass.getuser()
		betas						= ["237.29", "10.8.0"]
		prods						= ["10.255.242","242.52"]
		
		cenv_editado				= False
		self.Config					= configparser.ConfigParser()
		self.Config_ENV				= configparser.ConfigParser()
		self.Config._interpolation	= configparser.ExtendedInterpolation()
		
		try:
			self.Config.read("{0}/config/DEFAULT.ini".format(DIR))
		except:# CRIA O ARQUIVO DEFAULT
			try:
				os.system(" cp {0}/config/DEFAULT.ini.sample {0}/config/DEFAULT.ini".format(DIR))
			except Exception as e:
				print("Não foi possivel Criar um arquivo a partir da amostra DEFAULT.ini.sample")
				print(type(e))
				print(e)
			
			try:
				self.Config.read("{0}/config/DEFAULT.ini".format(DIR))
			except Exception as e:
				print("Verifique o arquivo {0}/config/DEFAULT.ini".format(DIR))
				print(type(e))
				print(e)



		try:
			self.Config.set("KEY", "root", DIR)
			self.Config.set("KEY", "user",USER)
			with open("{0}/config/DEFAULT.ini".format(DIR), "w+") as configfile:		
				self.Config.write(configfile)
		except Exception as e:
			print(type(e))
			print(e)
		
		try:
			s	= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.connect(("8.8.8.8", 80))
			IP	= s.getsockname()[0]
			s.close()
		except Exception as e:

			print(type(e))
			print(e)
	
		#DEFINE ENV
		
		try:	

			if any(beta in IP for beta in betas):
				self.Config.set("KEY", "env", "BETA")

			elif any(prod in IP for prod in prods):
				self.Config.set("KEY", "env", "PROD")
			else:
				self.Config.set("KEY", "env", "LOCAL")
			""" else:
				print("Não foi Possivel identivicar o ambiente!")
				try:
					print("Defina o tipo de Ambiente:")
					print("(1) BETA\n(2) PRODUCAO\n")
					env = input()
					
					if env == '1':
						self.Config.set("KEY", "env", "BETA")
					elif env == '2':
						self.Config.set("KEY", "env", "PROD")
					else:
						sys.exit("Opção invalida!")
				except Exception as e:
					print(type(e))
					print(e)
					raise Exception("Não foi Possivel identivicar o ambiente!")
					print(sys.exc_info()[0])
					sys.exit("Erro ao definir env")
				 """
			with open("{0}/config/DEFAULT.ini".format(DIR), "w+") as configfile:		
				self.Config.write(configfile)

		except Exception as e:
			print(type(e))
			print(e)
		try:
			self.Config_ENV.read("config/{0}.ini".format(self.Config.get("KEY", "env")))
		except:
			print("O ARQUIVO config/{0}.ini não existe.".format(self.Config.get("KEY", "env")))
			print("Iremos cria-lo")
			try: #TENTA CRIAR
				os.system(" cp {0}/config/BETA_PROD.ini.sample {0}/config/{1}.ini".format(DIR, self.Config.get("KEY", "env")))
			except Exception as e: #CASO DE ERRO
				print("Não foi possivel Criar um arquivo a partir da amostra BETA_PROD.ini.sample")
				print(type(e))
				print(e)
			else: #CASO NÂO
				try:#TENTA LÊ
					self.Config_ENV.read("config/{0}.ini".format(self.Config.get("KEY", "env")))
				except:#CASO FALHE
					print("Verifique o arquivo {0}/config/{1}.ini".format(DIR, self.Config.get("KEY", "env")))
					print(type(e))
					print(e)
				else:
					pass 
		# SE NÂO VERIFICA OS CAMPOS...
		try:
			for each_section in self.Config_ENV.sections():
				for(each_key, each_val) in self.Config_ENV.items(each_section):
					if each_val is None or "" :
						print("Os valores de {0}, da sessão {1} não foram definidos!".format(each_key,each_section))
						print("Insira os valores para{0}->{1}: ".format(each_section,each_key))
						val = input()
						self.Config_ENV.set(each_section, each_key, val)
						cenv_editado = True
						pass
			if(cenv_editado):
				with open("config/{0}.ini".format(self.Config.get("KEY", "env")), "w+") as configfile:
					self.Config.write(configfile)
		except:
			pass
		
		return

	def todict(self,obj, classkey=None):
		if isinstance(obj, dict):
			data = {}
			for (k, v) in obj.items():
				data[k] = self.todict(v, classkey)
			return data
		elif hasattr(obj, "_ast"):
			return self.todict(obj._ast())
		elif hasattr(obj, "__iter__") and not isinstance(obj, str):
			return [self.todict(v, classkey) for v in obj]
		elif hasattr(obj, "__dict__"):
			data = dict([(key, self.todict(value, classkey)) 
			for key, value in obj.__dict__.items() 
				if not callable(value) and not key.startswith('_')])
			if classkey is not None and hasattr(obj, "__class__"):
				data[classkey] = obj.__class__.__name__
			return data
		else:
			return obj

	def Jobs(self):
		jobs = {
			'SMS': self.job_sms,
			'SVC': self.job_servico_de_validacao,
			'SDU': self.job_dataupdate,
			'WATCH':self.job_watch,
			'SRC':self.job_src
		}
		return jobs
	
	def ExportControle(self):
		Result = self.todict(self.Controle)
		with open("{0}/config/DEFAULT.ini".format(self.Controle.Controle.logs.controle_log), "w+") as controlefile:
			controlefile.write(Result)
		controlefile.close()

	def SVC_f(self):
		if (not self.Jobs['SVC'].isAlive()) and (self.SVC_info['keepAlive'] is True):
			self.Jobs['SVC'] = threading.Thread(target=self.servicoDeValidacao.start, name="SVC")
			self.Jobs['SVC'].start()
		else:
			return

	def SRC_f(self):
		if (not self.Jobs['SRC'].isAlive()) and (self.SRC_info['keepAlive'] is True):

			self.Jobs['SRC'] = threading.Thread(target=self.recuperacaoDeCarrinhos.start, name="SRC",args=(lambda:self.SRC_info['stop'],))
			self.Jobs['SRC'].start()
		else:
			return

	def SMS_f(self):
		if (not self.Jobs['SMS'].isAlive()) and (self.SMS_info['keepAlive'] is True):

			self.Jobs['SMS'] = threading.Thread(target=self.SMS.start, name="SMS",args=(lambda:self.SMS_info['stop'],))
			self.Jobs['SMS'].start()
		else:
			return
	
	