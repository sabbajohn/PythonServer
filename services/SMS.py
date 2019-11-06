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
USER = getpass.getuser()
from Class import db



try:
	from comtele_sdk.textmessage_service import TextMessageService
except:
	try:
		comando = os.system
		comando('sudo pip3 install comtele_sdk')
		print('[!] Tentando Instalar as Dependencias')
	except:
		if IOError:	
			sys.exit("[!] Please install the mysql library: sudo pip3 install comtele_sdk")	
		
		else:
			time.sleep(10)   
			comando('python3 sms.py')
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
		logging.basicConfig(
		filename='/home/{0}/PythonServer/logs/sms.log'.format(USER),
		filemode='a+',
		level=logging.INFO,
		format='PID %(process)5s %(name)18s: %(message)s',
		#stream=sys.stderr,
 		)
		self.database = db	
		log = logging.getLogger('Serviço de Envio de SMS')
		log.info("Inicializando")
		log.info( datetime.datetime.now())
		
	def start(self):
		feedback = self.feedback
		feedback["metodo"] = "start"
		try:
			db_monitor()
		except:

			feedback["status"] = 4
			feedback["message"] = "Oops!",sys.exc_info()[0],"occured."
			feedback["erro"] = True
			feedback["comments"] = "Algo não panejado"
			with self._lock:
				super().Exceptions(feedback)
			


	
	def db_monitor(self):
		escreveu = False
		log = logging.getLogger('Monitor')
		log.info("Inicializando monitoramento do Banco de Dados")
		cursor = self.database.getCursor()

		while True:
			result = None
		
			cursor.execute("SELECT * FROM sms WHERE sent_at is NULL")
			result = cursor.fetchall()
			self.database.mydb.commit()
			if len(result)>0:

				log.info("{0} -> {1} sms's a serem enviados!".format(datetime.datetime.now(),len(result)))

				for x in result:
					send(x)


			else: 
				if(escreveu == False):

					log.info("Nenhum sms pendete, tentaremos novamente em 5 segundos!")
					escreveu= True
				else:
					pass
				time.sleep(5)


		def send(cliente):
			log = logging.getLogger('Envio de SMS')
			log.info("Enviando sms à:{0}".format(cliente[2]))
			__api_key = '3aa20522-7c0a-4562-b25d-70ffc3f27f8e'
			textmessage_service = TextMessageService(__api_key)
			Receivers = []
			Receivers.append(str(cliente[2]))
			try:

				result = textmessage_service.send('MS_.{}'.format(cliente[3]), cliente[4], Receivers)
			except :
				log.info("Oops!",sys.exc_info()[0],"occured.")
			
			log.info("SMS:{0}".format(result['Message']))
			update(result, cliente)
			return 
	
	
	
	def update(self,result, cliente):
		feedback = self.feedback
		feedback["metodo"] = 'update'

		with open("/home/"+USER+"/PythonServer/responses/response_sms.json","a+") as f: #Analizar Resposatas e Gerar Querys 
			agora = datetime.datetime.now()
			f.write("{0}:{1}\n".format(agora ,result))
		log = logging.getLogger('UPDATE')
		log.info("Atualizando infromações na base de dados.")
		agora = datetime.datetime.now()
		executor =self.database.getCursor()
		query = "UPDATE sms SET sent_at = '{0}' WHERE id = {1} ".format(agora, cliente[0])
		try:
			executor.execute(query)
			database.mydb.commit()
			return
		except :
			log.info("Oops!",sys.exc_info()[0],"occured.")
			log.info('#######')
			feedback["status"] = 1
			feedback["message"] = "Arquivo não encontrado!"
			feedback["erro"] = True
			with self._lock:
				super().Exceptions(feedback)
			sys.exit()

