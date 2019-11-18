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




class SMS(object):
	
	def __init__(self, M):
		self.Manager = M
		self._stop_event = threading.Event()
		self._lock = threading.Lock()
		self.USER = getpass.getuser()
		self.database = self.Manager.database
	

	def start(self):
		
		
		
		try:
			message = []
			message.append( "Inicializando SMS")
			self.feedback(metodo="start", status =-1, message = message, erro = False )
			message = None
			self.db_monitor()
		except:
			#O metodo é o start, mas o pau veio de dentro do db_monitor
		#	print("Oops!{0} occured.".format(sys.exc_info()[0]))
			message = []
			message.append( "{0}".format(sys.exc_info()))
			self.feedback(metodo="start", status =4, message = message, erro = True, comments = "Algo não panejado" )
			message = None

	def db_monitor(self):

	
		message = []
		message.append( "[INFO]:Inicializando o Monitoramento do Banco de Dados")
		self.feedback(metodo="Monitor", status =5, message = message, erro = False )
		message = None
		escreveu = False
		#quem sabe botar isso dentro de um try
		
		
		
		while True:
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
			except: 
				message = []
				message.append( sys.exc_info())
				self.feedback(metodo="Monitor", status =5, message = message, erro = False, comments ="Tentaremos novamente em Breve!"  )
				message = None
			finally:
				pass


	def send(self,cliente):

		
		message = []
		message.append( 'Enviando SMS a:{0}'.format(cliente[2]))
		self.feedback(metodo="send", status =5, message = message, erro = False, comments = "send" )
		message = None
		
		__api_key = '3aa20522-7c0a-4562-b25d-70ffc3f27f8e'
		textmessage_service = TextMessageService(__api_key)
		Receivers = []
		Receivers.append(str(cliente[2]))
		try:
			result = textmessage_service.send('MS_.{}'.format(cliente[3]), cliente[4], Receivers)
		except :
			
			
			message = []
			message.append( "[!!!]:Oops!{0}occured.".format(sys.exc_info()[0]))
			self.feedback(metodo="send", status =4, message = message, erro = True, comments = "Algo não panejado" )
			message = None
			
			return
		else:
			message = []
			message.append( "[INFO]:SMS:{0}".format(result['Message']))
			self.feedback(metodo="send", status =5, message = message, erro = False)
			message = None
			self.update(result, cliente)
			return

	def update(self,result, cliente):
		
		
		
		message = []
		message.append( "Atualizando infromações na base de dados.")
		self.feedback(metodo="update", status =5, message = message, erro = False)
		message = None
		try:
			with open("/home/"+self.USER+"/PythonServer/responses/response_sms.json","a+") as f: #Analizar Resposatas e Gerar Querys 
				agora = datetime.datetime.now()
				f.write("{0}:{1}\n".format(agora ,result))

			
			agora = datetime.datetime.now()
			""" handler_w = self.database.getConn("W")
			cursor_w = self.database.getCursor("W") """
			query = "UPDATE sms SET sent_at = '{0}' WHERE id = {1} ".format(agora, cliente[0])
			try:
				""" with self._lock: """
				self.database.execute("W",query, commit=True)
				""" handler_w.commit() """
				return
			except :
				message = []
				message.append( "{0}".format(sys.exc_info()[0]))
				self.feedback(metodo="update", status =1, message = message, erro = True)
				message = None
				#sys.exit() Nao matar o sistema!!
		except:
			#Se não tem arquivo de log ainda da pra trabalhar...
			message = []
			message.append( "[!]:Arquivo não encontrado")
			self.feedback(metodo="update", status =2, message = message, erro = True)
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
		#with self._lock:
		self.Manager.callback(feedback)

	

	