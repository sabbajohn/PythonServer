#!/usr/bin/python3
# coding: utf-8
import os
import sys
import time
from time import sleep
import datetime
from datetime import date
import logging
import getpass
import subprocess

class Startup(object):
	def __init__(self, *args, **kwargs):
		self.USER = getpass.getuser()
		logging.basicConfig(
			filename='/home/{0}/PythonServer/logs/StartUp.log'.format(self.USER),
			filemode='a+',
			level=logging.INFO,
			format='PID %(process)5s %(name)18s: %(message)s',
			#stream=sys.stderr,
 		)
		log = logging.getLogger('Serviço de Inicilização ')
		self.procs = ['sms.py','uwsgi','servico_de_validacao.py','Databaseupdate.py']
		self.delays={'validacao':200}
		self.start_time = 0
		self.i()
	
	def i(self):

		log = logging.getLogger('Serviço de Inicilização ')
		while True:
			""" log.info('{0} . Verificando SMS'.format(datetime.datetime.now()))
			
			if not self.checkIfProcessRunning(self.procs[0]):
					log.info('{0} . Inicializando serviço de SMS'.format(datetime.datetime.now()))
					os.system('nohup python3 sms.py &') """
			""" 	
			log.info('{0} . Verificando API'.format(datetime.datetime.now()))
			if not self.checkIfProcessRunning(self.procs[1]):
					log.info('{0} . Inicializando Servidor API'.format(datetime.datetime.now()))
					os.system('uwsgi --http 10.255.237.29:5000 --wsgi-file /home/{0}/PythonServer/Server/server.py --callable app --processes 4 --threads 2 --stats 10.255.237.29:9191 &'.format(self.USER)) """
			
			log.info('{0} . Verificando SVC'.format(datetime.datetime.now()))
			if (not self.checkIfProcessRunning(self.procs[2]) ) and (not self.checkIfProcessRunning(self.procs[3])):
				
				if self.start_time ==0:
					self.start_time = time.time()
					log.info('{0} . Inicializando serviço de Validação de Cadastros'.format(datetime.datetime.now()))
					os.system('python3 servico_de_validacao.py &')
					sleep(60)
				elif (time.time() - self.start_time) > self.delays['validacao']:

					log.info('{0} . Inicializando serviço de Validação de Cadastros'.format(datetime.datetime.now()))
					self.start_time = time.time()
					os.system('python3 servico_de_validacao.py &')
				
				
				elif (self.delays['validacao'] - (time.time() - self.start_time)) > 0 : 
			
					log.info(' Serviço de Validação de Cadastro em stand by... por {0}s'.format((self.delays['validacao'] - (time.time() - self.start_time))))
					log.info('{0} . Verificando SDU'.format(datetime.datetime.now()))
					
					modtime =os.path.getmtime("/home/"+self.USER+"/PythonServer/queries/query.txt")
					
					if modtime < self.start_time:
						log.info('{0} . Inicializando serviço de Atualização de Dados'.format(datetime.datetime.now()))
						os.system('python3 Databaseupdate.py &')
					else:
							log.info('{0} . Não há novos registros a serem atualizados!'.format(datetime.datetime.now()))
					pass
			else:
				sleep(2)
			
			sleep(5)

			
			

	def checkIfProcessRunning(self,processName):
		'''
		Check if there is any running process that contains the given name processName.
		'''
		#Iterate over the all the running process

		ps = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE).communicate()[0]
		processes = ps.decode().split('\n')
		# this specifies the number of splits, so the splitted lines
		# will have (nfields+1) elements
		nfields = len(processes[0].split()) - 1
		
		for row in processes[1:]:
			try:
				proc = row.split(None, nfields)
				if len(proc)>0:

					# Check if process name contains the given name string.
					if processName.lower() in proc[10].lower():
						return True
				else: 
					pass
			except:
				pass
		return False 

		
	

	
Startup()
