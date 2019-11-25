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
from services.servicodevalidacao import servicoDeValidacao
from services.DataUpdate import DataUpdate
from services.SMS import SMS
from services.watch import Watch
from services.recupecaoDeCarrinhos import recuperacaoDeCarrinhos
from utils.db import DB
from controle import Controle


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
		self.Modulos = self.Controle.modulos
		self.database = DB(self)

		self.SMS = SMS(M)
		self.recuperacaoDeCarrinhos = recuperacaoDeCarrinhos(M)
		self.DataUpdate = DataUpdate(M)
		self.servicoDeValidacao = servicoDeValidacao(M)
		self.Watch = Watch(M)

		#Definindo objeto das API's
		
		self.job_sms = threading.Thread(target=self.SMS.start, name="SMS", args=(lambda:self.Controle.modulos.SMS.stop,))
		self.job_src = threading.Thread(target=self.recuperacaoDeCarrinhos.start, name="SRC", args=(lambda:lambda:self.Controle.modulos.SRC.stop,))
		self.job_servico_de_validacao = threading.Thread(target=self.servicoDeValidacao.start, name="SVC")
		self.job_dataupdate = threading.Thread(target=self.DataUpdate.start, name="SDU")
		self.job_watch = threading.Thread(target=self.Watch.start, name="WATCH")
		# Inicializando
	
	
	def __cfg(self):
		DIR							= os.getcwd()
		USER						= getpass.getuser()
		self.Config					= configparser.ConfigParser()
		self.Config_ENV				= configparser.ConfigParser()
		self.Config._interpolation	= configparser.ExtendedInterpolation()
		try:
			self.Config.read("{0}/config/DEFAULT.ini".format(DIR))
		except Exception as e:
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
			if "237.29" in IP or "192.168." in IP :
				self.Config.set("KEY", "env", "BETA")

			elif "242.11" in IP or "242.52" in IP:
				self.Config.set("KEY", "env", "PROD")
			else:
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
				
				with open("{0}/config/DEFAULT.ini".format(DIR), "w+") as configfile:		
					self.Config.write(configfile)
	
		except Exception as e:
			print(type(e))
			print(e)
		try:
			 self.Config_ENV.read("config/{0}.ini".format(self.Config.get("KEY", "env")))
		except  Exception as e:
				print(type(e))
				print(e)
		
	
	#Em desuso...
	def __loadvariaveisDeControle(self):
		
		Variaveis_de_controle = {
			"key":{
				"env":	self.Config.get("KEY","env"),
				"root":	self.Config.get("KEY","root"),
				"user":	self.Config.get("KEY","user")
			},
			"env":{
				"DB":{
						"MSQL_R":{
							"host":self.Config_ENV.get("MYSQL_R","host"),
							"user":self.Config_ENV.get("MYSQL_R","user"),
							"passwd":self.Config_ENV.get("MYSQL_R","passwd"),
							"database":self.Config_ENV.get("MYSQL_R","database"),
							"raise_on_warnings":self.Config_ENV.get("MYSQL_R","raise_on_warnings")
						},
						"MSQL_W":{

							"host":self.Config_ENV.get("MYSQL_W","host"),
							"user":self.Config_ENV.get("MYSQL_W","user"),
							"passwd":self.Config_ENV.get("MYSQL_W","passwd"),
							"database":self.Config_ENV.get("MYSQL_W","database"),
							"raise_on_warnings":self.Config_ENV.get("MYSQL_W","raise_on_warnings")
						}
				},
				
				"API":{
					"mandrill":{
						"api_key":self.Config_ENV.get("MANDRILL","api_key")
					},
					"hubd":{
						"url":self.Config_ENV.get("HUBD","url"),
						"api_key":self.Config_ENV.get("HUBD","api_key")
					},
					"soa":{
						"url":self.Config_ENV.get("SOA","url"),
						"user":self.Config_ENV.get("SOA","user"),
						"key":self.Config_ENV.get("SOA","key")
					},
					"comtele":{
						"api_key":self.Config_ENV.get("COMTELE","api_key")
					},
	
				},
				"LINK":{
					"link_site":self.Config_ENV.get("LINK","link_site"),
					"link_de_compra":self.Config_ENV.get("LINK","link_de_compra"),
					"contact_mail":self.Config_ENV.get("LINK","contact_mail")
				}
			},
			"logs":{
				"manager_log":self.Config.get("LOGS","manager_log"),
				"sdu_log":self.Config.get("LOGS","sdu_log"),
				"svc_log":self.Config.get("LOGS","svc_log"),
				"sms_log":self.Config.get("LOGS","sms_log"),
				"api_log":self.Config.get("LOGS","api_log"),
				"startup_log":self.Config.get("LOGS","startup_log"),
				"watch_log":self.Config.get("LOGS","watch_log")
			},
			"files":{
				"query":self.Config.get("FILES","query"),
				"responses":self.Config.get("FILES","responses"),
				"responses_api":self.Config.get("FILES","responses_api"),
				"responses_sms":self.Config.get("FILES","responses_sms"),
			},
			"modulos":{
				"SMS":{
					"init": self.Config.getboolean("SMS","sms_init"),
					"init_time":None,
					"delay":None,
					"keepAlive": True,
					"lasttimerunning":None,
					"nextrun":None,
					"firstTime":True,
					"stop":False
					},
				"SVC":{
					"init": self.Config.getboolean("SVC","svc_init"),
					"delay":float(self.Config.get("SVC","delay")),
					"init_time":None,
					"keepAlive": True,
					"lasttimerunning":None,
					"nextrun":None,
					"firstTime":True,
					"stop":False	
				},
				"SDU":{

					"init": self.Config.getboolean("SDU","sdu_init"),
					"init_time":None,
					"delay":None,
					"keepAlive": True,
					"lasttimerunning":None,
					"nextrun":None,
					"firstTime":True,
					"stop":False
				},
				"SRC":{

					"init": self.Config.getboolean("SRC","src_init"),
					"init_time":None,
					"delay":float(self.Config.get("SRC","delay")),
					"keepAlive": True,
					"lasttimerunning":None,
					"nextrun":None,
					"firstTime":True,
					"stop":False
				}
			}
		}
		return Variaveis_de_controle
	#TODO, metodo para atualizar configurações
	""" def setMyself(self, module):
		modulo = self.getControle(module)

		api_dict = modulo.__dict__
		for x in api_dict:

			self.Config_ENV.set(api_dict[x].tag, api_dict[x].__dict__)
		
		with open("{0}/config/BETA.ini".format(self.Controle.Key.root), "w+") as configfile:		
			self.Config_ENV.write(configfile)	
 """
	def Jobs(self):
		jobs = {
			'SMS': self.job_sms,
			'SVC': self.job_servico_de_validacao,
			'SDU': self.job_dataupdate,
			'WATCH':self.job_watch,
			'SRC':self.job_src
		}
		return jobs
	
	def getControle(self, module):
		if "db" in module.casefold():
			return self.Controle.DB
		elif 'files' in module.casefold():
			return self.Controle.files
		elif 'api' in module.casefold():
			return self.Controle.API
		elif 'modulos' in module.casefold():
			return self.Controle.modulos
		elif 'sms' in module.casefold():
			return self.Controle.modulos.SMS
		elif 'svc' in module.casefold():
			return self.Controle.modulos.SVC
		elif 'SRC' in module.casefold():
			return self.Controle.modulos.SRC
		elif 'sdu' in module.casefold():
			return self.Controle.modulos.SDU
	
			
		self.controle	
	

	def setConfigFile(self, conf):
		
		if "DEFAULT".casefold() in conf.casefold():
			try:
				with open("{0}/config/DEFAULT.ini".format(self.Config.get("KEY", "root")), "w+") as configfile:		
					self.Config.write(configfile)
					return True
			except Exception as e:
				print(type(e))
				print(e)
				return False
		
		if "BETA".casefold() in conf.casefold():
			try:
				with open("{0}/config/BETA.ini".format(self.Config.get("KEY", "root")), "w+") as configfile:		
					self.Config_ENV.write(configfile)
					return True
			except Exception as e:
				print(type(e))
				print(e)
				return False

		elif "PROD".casefold() in conf.casefold():
			try:
				
				with open("{0}/config/PROD.ini".format(self.Config.get("KEY", "root")), "w+") as configfile:		
					self.Config_ENV.write(configfile)
				return True
			except Exception as e:
				print(type(e))
				print(e)
				return False
		
