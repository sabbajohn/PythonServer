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
from utils.Manager import Manager

class DataUpdate(Manager):
	
	

	def QueryRunner(self, database):
		n_updates = 0
		rest = 0
		log = logging.getLogger('QueryRunner')
		log.info("Procurando Por Arquivo de Querys.")
		fname = "/home/{0}/PythonServer/queries/query.txt".format(self.USER)
		H = database.getConn("W")
		executor= database.getCursor("W")
		if os.path.isfile(fname):
			infile = open(fname, 'r').readlines()
			if ( not len(infile)>0):
				log.info("Não há registros a serem atualizados.")
				log.info("Encerrando Serviço de Atuliazação.")
			for line in infile:
				line = line.replace('\n','')
				try:
					if(rest == 30):
						rest = 0
						log.info("Standy by 1s")
						sleep(1)
					executor.execute(line)
					H.commit()
					executor.rowcount
					n_updates = n_updates +1
					rest = rest +1

					log.info("Executando Querys n°{0}".format(n_updates))
				except database.connector.Error as err:
					log.info('Erro ao Atualiza o Banco de Dados! Erro {0}'.format(err))
					log.info('#######')
					sys.exit("[!]Não foi possivel Atualiza a base de dados! Erro {0}".format(err))

			database.closeConn("W")
			return n_updates


		else:
			self.log.info("Arquivo não encontrado!")
			return 0




	def start(self):
		self.USER =getpass.getuser()
		logging.basicConfig(
			filename='/home/{0}/PythonServer/logs/Databaseupdate.log'.format(self.USER),
			filemode='a+',
			level=logging.INFO,
			format='PID %(process)5s %(name)18s: %(message)s',
			#stream=sys.stderr,
	 	)
		log = logging.getLogger('Serviço de Atualização da Base de Dados')
		self.database = DB()
		start_time = time.time()
		log = logging.getLogger('Serviço de Atualização da Base de Dados')
		log.info('*******')
		log.info('Inicializando serviço  de Atualização da Base de Dados')
		log.info(datetime.datetime.now())
		result = self.QueryRunner(self.database)
		log.info('Serviço de Atualização da Base de Dados Concluido')
		duration = time.time() - start_time
		log.info('{0} registros foram Atualizados em {1} segundos'.format(result,duration))

		agora = datetime.datetime.now()
		if result > 0:
			os.system("mv  /home/"+self.USER+"/PythonServer/queries/query.txt /home/"+self.USER+"/PythonServer/queries/query_old-"+str(agora.hour)+":"+str(agora.minute)+".txt ")
			os.system("touch /home/{0}/PythonServer/queries/query.txt".format(self.USER))
		log.info("Encerrando Serviço de Atuliazação.")
		log.info('#######')

	