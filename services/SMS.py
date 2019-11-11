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
from utils.Manager import Manager
from utils.db import DB
from comtele_sdk.textmessage_service import TextMessageService
import threading




class SMS(Manager):
	
	def __init__(self, *args, **kwargs):
		self.feedback = {
			"class":"SMS",
			"metodo":"__init__",
			"status":None,
			"message":"",
			"erro":False,
			"comments":""
		}
		self._lock = threading.Lock()
		self.USER = getpass.getuser()
		self.database = DB()
		""" TODO FIXME
			! Não Preciso iniciar uma conexão com o DB toda vez ja existem prontas!


		 """
		
		
		
	def start(self):
		feedback = self.feedback
		feedback['metodo'] = 'start'
		
		try:
			self.db_monitor()
		except:
			print("Oops!{0} occured.".format(sys.exc_info()[0]))
			feedback["status"] = 4
			feedback["message"] = "Oops!{0}occured.".format(sys.exc_info()[0])
			feedback["erro"] = True
			feedback["comments"] = "Algo não panejado"
			with self._lock:
				super().callback(feedback)

	def db_monitor(self):
		feedback = self.feedback
		feedback['metodo'] = 'Monitor'
		feedback["status"] = 5
		feedback["message"] = "Inicializando o Monitoramento do Banco de Dados"
		feedback["comments"] = ""
		escreveu = False
		#TODO Reportar Step
		with self._lock:
				super().callback(feedback)
		
		handler_r=self.database.getConn("R")
		
		
		while True:
			result = None
			
			cursor_r =self.database.getCursor("R")
			cursor_r.execute("SELECT * FROM sms WHERE sent_at is NULL")
			result = cursor_r.fetchall()
			handler_r.commit()
			
			if len(result)>0:

				""" 	log.info("{0} -> {1} sms's a serem enviados!".format(datetime.datetime.now(),len(result))) """
				
				for x in result:
					self.send(x)
				
				
			else: 
				if(escreveu == False):
					
					""" log.info("Nenhum sms pendete, tentaremos novamente em 5 segundos!") """
					escreveu= True
				else:
					pass
				time.sleep(5)
			
			
	def send(self,cliente):
		feedback = self.feedback
		feedback['metodo']='send'
		#log = logging.getLogger('Envio de SMS')
		#log.info("Enviando sms à:{0}".format(cliente[2]))
		__api_key = '3aa20522-7c0a-4562-b25d-70ffc3f27f8e'
		textmessage_service = TextMessageService(__api_key)
		Receivers = []
		Receivers.append(str(cliente[2]))
		try:

			result = textmessage_service.send('MS_.{}'.format(cliente[3]), cliente[4], Receivers)
		except :
			print("Oops!{0} occured.".format(sys.exc_info()[0]))
			feedback["status"] = 4
			feedback["message"] = "Oops!{0}occured.".format(sys.exc_info()[0])
			feedback["erro"] = True
			feedback["comments"] = "Algo não panejado"
			with self._lock:
				super().Exceptions(feedback)
				""" log.info("Oops!{0}occured.".format(sys.exc_info()[0])) """
			return
		""" log.info("SMS:{0}".format(result['Message'])) """
		self.update(result, cliente)
		return



	def update(self,result, cliente):
		feedback = self.feedback
		feedback["metodo"] = 'update'
		with open("/home/"+self.USER+"/PythonServer/responses/response_sms.json","a+") as f: #Analizar Resposatas e Gerar Querys 
			agora = datetime.datetime.now()
			f.write("{0}:{1}\n".format(agora ,result))
		""" log = logging.getLogger('UPDATE') """
		""" log.info("Atualizando infromações na base de dados.") """
		agora = datetime.datetime.now()
		handler_w = self.database.getConn("W")
		cursor_w = self.database.getCursor("W")
		query = "UPDATE sms SET sent_at = '{0}' WHERE id = {1} ".format(agora, cliente[0])
		try:
			cursor_w.execute(query)
			handler_w.commit()
			
			return
		except :
			""" log.info("Oops!",sys.exc_info()[0],"occured.") """
			""" log.info('#######') """
			feedback["status"] = 1
			feedback["message"] = "Arquivo não encontrado!"
			feedback["erro"] = True
			with self._lock:
				super().Exceptions(feedback)
			sys.exit()


