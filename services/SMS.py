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
from comtele_sdk.textmessage_service import TextMessageService
import threading
import asyncio




class SMS(object):
	
	def __init__(self, M):
		self.Manager = M
		
		self.USER = getpass.getuser()
		self.database = self.Manager.database
		self.sms_api = self.Manager.getControle("api")
		self.sms_files = self.Manager.getControle("files") 

	def start(self, stop):
		
		
		
		try:
			message = []
			message.append( "Inicializando SMS")
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
		
	async def runNow(self):

	
		message = []
		message.append( "Inicializando o Monitoramento do Banco de Dados")
		self.feedback(metodo="Monitor", status =5, message = message, erro = False )
		message = None
		escreveu = False
		#quem sabe botar isso dentro de um try
		
		
	
		try:
			result = None
			query = "SELECT * FROM sms WHERE sent_at is NULL"
		
			result = self.database.execute("R",query)
		
			if len(result)>0:
				if(escreveu == True):
					message = []
					message.append( "Novo sms encontrado!")
					self.feedback(metodo="Monitor", status =5, message = message, erro = False )
					message = None

				message = []
				message.append( "{0} sms's a serem enviados!".format(len(result)))
				self.feedback(metodo="Monitor", status =5, message = message, erro = False )
				message = None
				
				
				
				for x in result:
					self.send(x)
				
				return True
			else: 
			
				message = []
				message.append( "Nenhum SMS Pendente no momento!")
				self.feedback(metodo="Monitor", status =5, message = message, erro = False, comments ="Tentaremos novamente em Breve!"  )
				message = None
				escreveu= True
				return False
		
				
		except: 
			message = []
			message.append( sys.exc_info())
			self.feedback(metodo="Monitor", status =5, message = message, erro = False, comments ="Tentaremos novamente em Breve!"  )
			message = None
		finally:
			return False
	
	def db_monitor(self,stop):

	
		message = []
		message.append( "Inicializando o Monitoramento do Banco de Dados")
		self.feedback(metodo="Monitor", status =5, message = message, erro = False )
		message = None
		escreveu = False
		#quem sabe botar isso dentro de um try
		
		
		
		while True:
			if stop():
				break
			
			try:
				result = None
				query = "SELECT * FROM sms WHERE sent_at is NULL"
			
				result = self.database.execute("R",query)
			
				if len(result)>0:
					if(escreveu == True):
						message = []
						message.append( "Novo sms encontrado!")
						self.feedback(metodo="Monitor", status =5, message = message, erro = False )
						message = None

					message = []
					message.append( "{0} sms's a serem enviados!".format(len(result)))
					self.feedback(metodo="Monitor", status =5, message = message, erro = False )
					message = None
					
					
					
					for x in result:
						self.send(x)
					
					
				else: 
					if(escreveu == False):
						message = []
						message.append( "Nenhum SMS Pendente no momento!")
						self.feedback(metodo="Monitor", status =5, message = message, erro = False, comments ="Tentaremos novamente em Breve!"  )
						message = None
						escreveu= True
					else:
						pass
					time.sleep(5)
			except Exception as e:

				message = []
				message.append(type(e))
				message.append(e)
				self.feedback(metodo="Monitor", status =1, message = message, erro = False, comments ="2"  )
				message = None
			finally:
				pass
		sys.exit()

	def send(self,cliente):

		
		message = []
		message.append( 'Enviando SMS a:{0}'.format(cliente[2]))
		self.feedback(metodo="send", status =5, message = message, erro = False, comments = "send" )
		message = None
		
	
		textmessage_service = TextMessageService(self.sms_api.comtele.api_key)
		Receivers = []
		Receivers.append(str(cliente[2]))
		try:		
			result = textmessage_service.send('MS_.{}'.format(cliente[3]), cliente[4], Receivers)
		except Exception as e :
			
			
			message = []
			message.append(type(e))
			message.append(e)
			
			self.feedback(metodo="send", status =1, message = message, erro = True, comments = "Erro ao enviar SMS" )
			message = None
			
			return True
		else:
			message = []
			message.append( "SMS:{0}".format(result['Message']))
			self.feedback(metodo="send", status =5, message = message, erro = False)
			message = None
			self.sms_api.comtele.enviados +=1
			self.Manager.configFile()

			self.update(result, cliente)
			return

	def update(self,result, cliente, tentativa=0):
				
		
		message = []
		message.append( "Atualizando infromações na base de dados.")
		self.feedback(metodo="update", status =5, message = message, erro = False)
		message = None
		try:
			with open(self.sms_files.responses_sms, "+a") as f: #Registra solicitações
				agora = datetime.datetime.now()
				f.write("{0}:{1}\n".format(agora ,result))
		except FileNotFoundError:
			#Se não tem arquivo de log ainda da pra trabalhar... status 2
			message = []
			message.append( "[!]:Arquivo não encontrado")
			message.append( "[!]:Criaremos um novo arquivo...")
			self.feedback(metodo="update", status =2, message = message, erro = True)
			message = None
			
			try:
				os.system("sudo touch {0}".format(self.sms_files.responses_sms) )
				return True 
			except Exception as e: #tenta criar se não der tudo bem ainda da pra trabalhar status 2
				message = []
				message.append(type(e))
				message.append(e)							
				self.feedback(metodo="update", status =2, message = message, erro = True, comments="Falha ao encontrar arquivo você deve gera-lo manualmente!")
				message = None
				pass 

		agora = datetime.datetime.now()
		query = "UPDATE sms SET sent_at = '{0}' WHERE id = {1} ".format(agora, cliente[0])
		try:
		
			self.database.execute("W",query, commit=True)
		
			return True
		except Exception as e :
			message = []
			message.append(type(e))
			message.append(e)
			self.feedback(metodo="update", status =3, message = message, erro = True, comments="Falha ao atualizar base de dados:\n{0}".format(query))
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
			"class":"SMS",
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
		
		feedback['time'] = datetime.datetime.now()
		#with self._lock:
		self.Manager.callback(feedback)

	

	