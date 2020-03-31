#!/usr/bin/python3
# coding: utf-8
import sys
import os
import logging
import time
import datetime
from datetime import date
import json
import getpass
import threading
import mandrill
import configparser	
import requests
import random
from utils.Gateways.Digimais import Digimais
from utils.Gateways.MercadoPago import MercadoPago
from utils.Mandrill.Mandrill import Mandrill
from utils import funcoes
class recuperacaoDeCarrinhos(object):
	def __init__(self, M):
		
		self.Manager 			= M
		self.database 			= self.Manager.database
		self.mandrill_client 	= None
		

	def start(self, stop):
	
		try:
			message = []
			message.append( "Inicializando Servico de Recuperação de Carrinhos")
			self.feedback(metodo="start", status =-1, message = message, erro = False )
			message = None
			if stop():
				return
			
			self.db_monitor_src()
			self.recCarrinho2()
			self.Manager.SRC_info['last_run'] = str(self.Manager.Agenda['SRC'].last_run)
		
			time.sleep(1)
			return
		except SystemExit:
			message = []
			message.append( "Serviço finalizado via Watcher")
			self.feedback(metodo="start", status =5, message = message, erro = False, comments = "Finalizado via Watcher" )
			message = None
			sys.exit()
		except Exception as e:
			
			message = []
			message.append( type(e))
			message.append(e)
			self.feedback(metodo="start", status =4, message = message, erro = True, comments = "Algo não panejado" )
			message = None
		return

	async def runNow(self):
		message = []
		message.append( "Inicializando Consulta não agendada")
		self.feedback(metodo="Monitor", status =5, message = message, erro = False )
		message = None
		escreveu = False
		try:
				result = None
				
			
				result = self.database.execute("R",self.Manager.SRC_info['query'])
			
				if len(result)>0:
					
					if(escreveu == True):
						message = []
						message.append( "Novos carrinhos encontrados!")
						self.feedback(metodo="Monitor", status =5, message = message, erro = False )
						message = None

					message = []
					message.append( "{0} Carrinhos a serem Resgatados!".format(len(result)))
					self.feedback(metodo="Monitor", status =5, message = message, erro = False )
					message = None
	
					params = self.emailParams(result)
					return self.send(params)
					
					
				else: 
					if(escreveu == False):
						message = []
						message.append( "Nenhum carrinho abandonado no momento!")
						self.feedback(metodo="runNow", status =5, message = message, erro = False, comments ="Nenhum Carrinho!"  )
						message = None
						escreveu= True
						return False
		except Exception as e: 

			message = []
			message.append(type(e))
			message.append(e)

			self.feedback(metodo="Monitor", status =5, message = message, erro = False, comments ="Exceção não tratada "  )
			message = None
			return False

	def db_monitor_src(self):
		message = []
		message.append( "Inicializando o Monitoramento do Banco de Dados")
		self.feedback(metodo="Monitor", status =5, message = message, erro = False )
		message = None
		escreveu = False
	
		
			
		try:
			result = None
			
			
			result = self.database.execute("R",self.Manager.SRC_info['query'][0],serialized = True)
		
			if len(result)>0:
				Mandrill = Mandrill(self.Manager)
				if(escreveu == True):
					message = []
					message.append( "Novos carrinhos encontrados!")
					self.feedback(metodo="Monitor", status =5, message = message, erro = False )
					message = None

				message = []
				message.append( "{0} Carrinhos a serem Resgatados!".format(len(result)))
				self.feedback(metodo="Monitor", status =5, message = message, erro = False )
				message = None
				Mandrill.send(result)
				Mandrill = None
				return
				
			else: 
				if(escreveu == False):
					message = []
					message.append( "Nenhum carrinho abandonado no momento!")
					self.feedback(metodo="Monitor", status =5, message = message, erro = False, comments ="Tentaremos novamente em Breve! L144"  )
					message = None
					escreveu= True
				
				return
				#time.sleep(self.delay)
		except Exception as e :
			message = []
			message.append(type(e))
			message.append(e)
			self.feedback(metodo="Monitor", status =2, message = message, erro = False, comments ="L154"  )
			message = None
		finally:
			return

	def recCarrinho2(self,*args, **kwargst):
		message = []
		message.append( "Inicializando o Recuperação de Carrinhos II")
		self.feedback(metodo="recCarrinho2", status =5, message = message, erro = False )
		message = None
		escreveu = False
	
		try:
			query = self.Manager.SRC_info['query'][1]
			# Se não estiver definida sai da função
		except:
			pass 
		
		try:
			carrinhos = None
			carrinhos = self.database.execute("R",self.Manager.SRC_info['query'][1],serialized=True)

			if len(carrinhos)>0:
			
				if(escreveu == True):
					message = []
					message.append( "Novos carrinhos encontrados!")
					self.feedback(metodo="recCarrinho2", status =5, message = message, erro = False )
					message = None

				message = []
				message.append( "{0} Carrinhos a serem Resgatados!".format(len(carrinhos)))
				self.feedback(metodo="recCarrinho2", status =5, message = message, erro = False )
				message = None
				emails = []
				message = []
				message.append('Gerando Boletos via {}'.format(self.Manager.Controle.Key.gateway))
				self.feedback(metodo="recCarrinho2", status =5, message = message )
				message = None
				
				for i, carrinho in enumerate(carrinhos):
					
					
					
					nome =  carrinho['Nome'].split(" ")
					if not nome[len(nome)-1] == "":
						sobrenome = nome[len(nome)-1]
					else:
						sobrenome = nome[len(nome)-2]
					carrinho['Nome'] = nome[0]
					carrinho['Sobrenome'] =  sobrenome
					total = float(carrinho['Quantidade']*carrinho['VlBilhete'])
					if total < 10:	
						carrinho['ValorBoleto'] = float(10)
					else:
						
						carrinho['ValorBoleto'] = funcoes.formataValor(total)
					
					if 'Digimais' in self.Manager.Controle.Key.gateway:
						Gate = Digimais(self.Manager)
						boleto = Gate.boleto(carrinho)
						if boleto:
							carrinho['boleto'] = boleto
							carrinhos[i] = carrinho
							funcoes.saveGoogleLog(carrinho)
					else:
						Gate = MercadoPago(self.Manager)
						boleto = Gate.boleto(carrinho)
						if boleto:
							carrinho['boleto'] = boleto
							carrinhos[i] = carrinho
							funcoes.saveGoogleLog(carrinho)

				Mandrill = Mandrill(self.Manager)
				Mandrill.send('boleto', carrinhos)
				Mandrill = None
				return 
		except Exception as e:
			message = []
			message.append( "{0} ".format(len(e)))
			self.feedback(metodo="recCarrinho2", status =2, message = message, erro = False )
			message = None

	def feedback(self,*args, **kwargst):
		message = kwargst.get('message')
		comments = kwargst.get('comments')
		metodo =kwargst.get('metodo')
		status =kwargst.get('status')
		try:
			erro =kwargst.get('erro')
		except:
			erro = False
		feedback = {
			"class":"recuperacaoDeCarrinhos",
			"metodo":kwargst.get('metodo'),
			"status":kwargst.get('status'),
			"message":[],
			"erro":False,
			"comments":"",
			"time":None
		}
		feedback["metodo"] = metodo
		feedback["status"] = status
		feedback["erro"]=erro
		if feedback['status']== 0:
			for msg in message:
				feedback["message"].append( '[OK]:{0}'.format(msg)) 
			
		elif feedback['status']== 1:
			for msg in message:
				feedback["message"].append('[X]:{0}'.format(msg))
		elif feedback['status']== 2:
			for msg in message:
				feedback["message"].append('[!]:{0}'.format(msg))
		elif feedback['status']== 3:
			for msg in message:
				feedback["message"].append( '[SQL_ERRO]:{0}'.format(msg))
		elif feedback['status']== 4:
			for msg in message:
				feedback["message"].append('[!!!]:{0}'.format(msg))
		elif feedback['status']== 5:
			for msg in message:
				feedback["message"].append('[INFO]:{0}'.format(msg)) 
		
		try: 
			feedback["comments"] = comments
		except:
			feedback["comments"] = ""
		
		feedback['time'] = str(datetime.datetime.now())
	
		self.Manager.callback(feedback)

