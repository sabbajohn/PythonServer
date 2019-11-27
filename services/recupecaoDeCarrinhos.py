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
import asyncio
class recuperacaoDeCarrinhos(object):
	def __init__(self, M):
	
		self.Manager = M
		self.database = self.Manager.database
		self.mandrill_client = None
		self.src_api =self.Manager.getControle('api')
		self.src_service =self.Manager.getControle('src')
		self.query = 	self.src_service.querys
		self.delay = self.src_service.delay
		self.mandrill_key = self.src_api.mandrill.api_key
		self.cont = self.src_api.mandrill.enviados

	def start(self, stop):
		try:
			message = []
			message.append( "Inicializando Servico de Recuperação de Carrinhos")
			self.feedback(metodo="start", status =-1, message = message, erro = False )
			message = None

			self.db_monitor(stop)
		except SystemExit:
			message = []
			message.append( "Serviço finalizado via Watcher")
			self.feedback(metodo="start", status =5, message = message, erro = False, comments = "Finalizado via Watcher" )
			message = None
			sys.exit()
		else:
			
			message = []
			message.append( "{0}".format(sys.exc_info()))
			self.feedback(metodo="start", status =4, message = message, erro = True, comments = "Algo não panejado" )
			message = None
		

		pass
	
	async def runNow(self):
		message = []
		message.append( "Icializando Consulta não agendada")
		self.feedback(metodo="Monitor", status =5, message = message, erro = False )
		message = None
		escreveu = False
		try:
				result = None
				
			
				result = self.database.execute("R",self.query)
			
				if len(result)>0:
					self.Manager.Variaveis_de_controle["SRC"]['lasttimerunning'] =str( datetime.datetime.now())
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

	def db_monitor(self,stop):
		message = []
		message.append( "Inicializando o Monitoramento do Banco de Dados")
		self.feedback(metodo="Monitor", status =5, message = message, erro = False )
		message = None
		escreveu = False
	
		while True:
			if stop():
				break
			
			try:
				result = None
				
			
				result = self.database.execute("R",self.query)
			
				if len(result)>0:
					self.Manager.Variaveis_de_controle["SRC"]['lasttimerunning'] =str( datetime.datetime.now())
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
					self.send(params)
					time.sleep(self.delay)
					
				else: 
					if(escreveu == False):
						message = []
						message.append( "Nenhum carrinho abandonado no momento!")
						self.feedback(metodo="Monitor", status =5, message = message, erro = False, comments ="Tentaremos novamente em Breve!"  )
						message = None
						escreveu= True
					else:
						pass
					time.sleep(self.delay)
			except: 
				message = []
				message.append( sys.exc_info())
				self.feedback(metodo="Monitor", status =5, message = message, erro = False, comments ="Tentaremos novamente em Breve!"  )
				message = None
			finally:
				pass
		sys.exit()

	def checkAPI(self):
		if self.mandrill_client is None:
			try:
				self.mandrill_client = mandrill.Mandrill(self.mandrill_key)
				return True
			except:
				message = []
				message.append( sys.exc_info())
				self.feedback(metodo="Monitor", status =2, message = message, erro = True )
				message = None
				
		else:
			try:
				valida= self.mandrill_client.users.ping()
				if "PONG" in valida:
					return True
			except:
				try:
					self.mandrill_client = mandrill.Mandrill(self.mandrill_key)
					return True
				except :
					message = []
					message.append( sys.exc_info())
					self.feedback(metodo="Monitor", status =2, message = message, erro = True )
					message = None
					return False

	def emailParams(self, result):
		cont = 0
		to = []
		merge_vars = []
		keys_to = [ "email","name"]
		template_content =  [{'content': 'example content', 'name': 'example name'}]# faço nem ideia do que seja isso
		global_merge_vars=  [{'content':  self.Config_ENV.get("LINKS","link_site"), 'name': 'link_site'},{'content':  self.Config_ENV.get("LINKS","contact_mail"), 'name': 'CONTACT_MAIL'},{'content':  self.Config_ENV.get("LINKS","link_de_compra"), 'name': 'link_de_compra'}]
		for x in result:
			merge_vars.append({'rcpt':x[0],'vars': [{'content': x[1], 'name':'Nome'}]})
			to.append(dict(zip(keys_to, x)))
			cont +=1

		
		message = {
			'global_merge_vars':global_merge_vars,
			'to': to,
			'merge_vars':merge_vars,
			'track_clicks': True,
			'track_opens': True
			
			
		}
		return {
			"template_content":template_content,
			"message":message,
			"cont":cont
		}

	def send(self, p):
		
		if(self.checkAPI()):


			try:
				result = self.mandrill_client.messages.send_template(template_name='carrinhos-recuperados', template_content=p['template_content'], message=p['message'], asy=True, ip_pool='Main Pool')
				if 'queued' in result[0]["status"] or 'sent' in result[0]["status"] :
					self.cont = p['cont'] 
					self.Manager.configFile()
					self.Manager.Variaveis_de_controle["SRC"]['nextrun'] = str(datetime.datetime.fromtimestamp(time.time()+float(self.delay)))
					return True
			except mandrill.Error as e:
				
				
				message = []
				message.append( "Oops!{0}occured.".format(e))
				self.feedback(metodo="send", status =4, message = message, erro = True, comments = "Algo não panejado" )
				message = None
				
				return False
			except not mandrill.Error:
				message = []
				message.append( "SMS:{0}".format(['Message']))
				self.feedback(metodo="send", status =5, message = message, erro = False)
				message = None

				return False
			except Exception as e:
				message.append( type(e))
				message.append(e)
				self.feedback(metodo="send", status =5, message = message, erro = False)
				message = None
		else:
				message = []
				message.append( "Não foi Possivel validara a Chave API")
				self.feedback(metodo="send", status =5, message = message, erro = False, comments = "Algo não panejado" )
				message = None
				return False

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
				feedback["message"].append( '[DIE]:{0}'.format(msg))
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
		
		feedback['time'] = datetime.datetime.now()
	
		self.Manager.callback(feedback)

	

	