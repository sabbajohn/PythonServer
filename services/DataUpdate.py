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
from Class import db
try:
	import mysql.connector
except:
	try:
		comando = os.system
		comando('sudo pip3 install mysql')
		print('[!] Tentando Instalar as Dependencias')
	except:
		if IOError:	
			sys.exit("[!] Please install the mysql library: sudo pip3 install mysql")	
		
		else:
			sleep(10)   
			comando('python3 Databaseupdate.py')



class DataUpdate(object):
	

	def __init__(self, *args, **kwargs):
		
		self.USER =getpass.getuser()
		self.database = db()
		logging.basicConfig(
		filename='/home/{0}/PythonServer/logs/Databaseupdate.log'.format(self.USER),
		filemode='a+',
		level=logging.INFO,
		format='PID %(process)5s %(name)18s: %(message)s',
		#stream=sys.stderr,
 		)
		
		
	def start(self):
		start_time = time.time()
		log = logging.getLogger('DataUpdate')
		result = self.QueryRunner(self.database)
		log.info('Serviço de Atualização da Base de Dados Concluido')
		duration = time.time() - start_time
		log.info('{0} registros foram Atualizados em {1} segundos'.format(result,duration))
	
		agora = datetime.datetime.now()
		if result['cont'] > 0:
			os.system("mv  /home/"+self.USER+"/PythonServer/queries/query.txt /home/"+self.USER+"/PythonServer/queries/query_old-"+str(agora.hour)+":"+str(agora.minute)+".txt ")
			os.system("touch /home/{0}/PythonServer/queries/query.txt".format(self.USER))
		log.info("Encerrando Serviço de Atuliazação.")
		log.info('#######')
		return result
		
	def QueryRunner(self):
		n_updates = 0
		rest = 0
		log = logging.getLogger('QueryRunner')
		log.info("Procurando Por Arquivo de Querys.")
		fname = "/home/{0}/PythonServer/queries/query.txt".format(self.USER)
		executor= database.getCursor()
		
		if os.path.isfile(fname):
			infile = open(fname, 'r').readlines()
			if ( not len(infile)>0):
				log.info("Não há registros a serem atualizados.")
				log.info("Encerrando Serviço de Atuliazação.")
				return {"erro":False,"message":"Não há registros a serem atualizados."}
			try:
				for line in infile:
					line = line.replace('\n','')
				
					

					executor.execute(line)		
					n_updates +=  1


					log.info("Executando Querys n°{0}".format(n_updates))
				database.mysql.commit()
			except mysql.connector.Error as err:
					log.info('Erro ao Atualiza o Banco de Dados! Erro {0}'.format(err))
					database.rollback()
					log.info('#######')
					return {"erro":True,"message":"Erro ao Atualiza o Banco de Dados! Erro {0}".format(err)}
			return {"erro":False,"cont":n_updates} 

		else:
			log.info("Arquivo não encontrado!")
			return {"erro":True,"message":"Arquivo não encontrado!"}

		pass



