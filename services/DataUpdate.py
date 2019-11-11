#!/usr/bin/python3
# coding: utf-8
import sys
import os
import os.path
import getpass
import logging
import time
import datetime
from datetime import date
from time import sleep
from utils.db import DB
from Manager import Manager
import threading
class DataUpdate(Manager):
	
	

	def QueryRunner(self, database):
		n_updates = 0
		rest = 0
		log = logging.getLogger('QueryRunner')
		message = []
		message.append("Procurando Por Arquivo de Querys.")
		self.feedback(metodo ='start', status =5, message=message, erro = False)
		message = None
		fname = "/home/{0}/PythonServer/queries/query.txt".format(self.USER)
		H = database.getConn("W")
		executor= database.getCursor("W")
		if os.path.isfile(fname):
			infile = open(fname, 'r').readlines()
			if ( not len(infile)>0):
				message = []
				message.append("Não há registros a serem atualizados.")
				message.append("Encerrando Serviço de Atuliazação.")
				self.feedback(metodo ='start', status =5, message=message, erro = False)
				message = None
			for line in infile:
				line = line.replace('\n','')
				try:
					if(rest == 30):
						rest = 0
						message.append("Standy by 1s")
						self.feedback(metodo ='start', status =5, message=message, erro = False)
						message = None
						sleep(1)
					executor.execute(line)
					H.commit()
					executor.rowcount
					n_updates = n_updates +1
					rest = rest +1
					message = []
					message.append("Executando Querys n°{0}".format(n_updates))
					self.feedback(metodo ='start', status =5, message=message, erro = False)
					message = None
				except database.connector.Error as err:
					message = []
					message.append('Erro ao Atualiza o Banco de Dados! Erro {0}'.format(err))
					#sys.exit("[!]Não foi possivel Atualiza a base de dados! Erro {0}".format(err)) Não matar
					self.feedback(metodo ='start', status =3, message=message, erro = True)
					message = None
			database.closeConn("W")
			return n_updates


		else:
			message = []
			message.append("Arquivo não encontrado!")
			self.feedback(metodo ='start', status =3, message=message, erro = True)
			message = None
			return 0




	def start(self):
		self._lock =threading.Lock()
		self._stop_event = threading.Event()
		self.USER =getpass.getuser()
		message = []
		message.append("Inicializando serviço  de Atualização da Base de Dados")
		self.feedback(metodo ='start', status =-1, message=message, erro = False)
		message = None
		
		self.database = DB()
		start_time = time.time()
		
		
		
	
		result = self.QueryRunner(self.database)
		duration = time.time() - start_time
		message = []
		message.append("Serviço de Atualização da Base de Dados Concluido")
		message.append('{0} registros foram Atualizados em {1} segundos'.format(result,duration))
		message.append("Encerrando Serviço de Atuliazação.")
		self.feedback(metodo ='list_generator', status =0, message=message, erro = False)
		message = None
		
	
	

		agora = datetime.datetime.now()
		if result > 0:
			os.system("mv  /home/"+self.USER+"/PythonServer/queries/query.txt /home/"+self.USER+"/PythonServer/queries/query_old-"+str(agora.hour)+":"+str(agora.minute)+".txt ")
			os.system("touch /home/{0}/PythonServer/queries/query.txt".format(self.USER))
		
		
		

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
			"class":"DataUpdate",
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
		super().callback(feedback)

	def end(self):
		raise Exception("kill-me")
	def restart(self):
		raise Exception("restart")



	