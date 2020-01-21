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
import ctypes 

#from Manager import Manager
import threading
class DataUpdate(object):
	def __init__(self, M):
		self.Manager = M
		self.database = self.Manager.database
		self.sdu_files = self.Manager.getControle("files")
		self.sdu_servico = self.Manager.getControle("sdu")

	def QueryRunner(self, database):
		n_updates = 0
		rest = 0
		
		message = []
		message.append("Procurando Por Arquivo de Querys.")
		self.feedback(metodo ='start', status =5, message=message, erro = False)
		message = None
		fname = self.sdu_files.query
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
						message = []
						message.append("Standy by 1s")
						self.feedback(metodo ='start', status =5, message=message, erro = False)
						message = None
						sleep(1)
					database.execute("W", line, commit=True)
					n_updates = n_updates +1
					rest = rest +1
					message = []
					message.append("Executando Querys n°{0}".format(n_updates))
					self.feedback(metodo ='start', status =5, message=message, erro = False)
					message = None
				except Exception as e:
					message = []
				
					message.append('Erro ao Atualiza o Banco de Dados! Erro ')
					message.append(type(e))
					message.append(e)
					
					self.feedback(metodo ='start', status =3, message=message, erro = True)
					message = None
		
			return n_updates


		else:
			message = []
			message.append("Arquivo query não encontrado!")
			message.append("Verificar Diretorio: {0}".format(self.sdu_files.query))
			self.feedback(metodo ='start', status =1, message=message, erro = True) #Arquivo de Query vazio....
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
			try:

				os.system("mv {0} {1}/queries/query_old-".format(self.sdu_files.query, self.Manager.Controle.Key.root)+str(agora.hour)+":"+str(agora.minute)+".txt ")
				os.system("touch {0}".format(self.sdu_files.query))
			except Exception as e:
				message = []
				message.append("Falha ao mover arquivos query")

				self.feedback(metodo ='list_generator', status =4, message=message, erro = False, comments= "Executou as inserções, mas não criou arquivo de query para proximo turno e nem logs")
				message = None
		return 
		
		

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
		
		feedback['time'] =str(datetime.datetime.now())
		#with self._lock:
		self.Manager.callback(feedback)

	def get_id(self): 
		
		# returns id of the respective thread 
		if hasattr(self, '_thread_id'): 
			return self._thread_id 
		for id, thread in threading._active.items(): 
			if thread is self: 
				return id
		
	def raise_exception(self): 
		message = []
		message.append( "Serviço finalizado via Watcher")
		self.feedback(metodo="Watcher", status =5, message = message, erro = False, comments = "Finalizado via Watcher" )
		message = None
		thread_id = self.get_id() 
		res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 
				ctypes.py_object(SystemExit)) 
		if res > 1: 
			ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
			print('Finalizando Serviço')

