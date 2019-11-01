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
from itertools import islice
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

USER =getpass.getuser()
sys.path.insert(1,'/home/{0}/PythonServer/Class'.format(USER))
def QueryRunner(database):
	n_updates = 0
	rest = 0
	log = logging.getLogger('QueryRunner')
	log.info("Procurando Por Arquivo de Querys.")
	fname = "/home/{0}/PythonServer/query.txt".format(USER)
	executor= database.cursor()
	if os.path.isfile(fname):
		infile = open(fname, 'r').readlines()
		if ( not len(infile)>0):
			log.info("Não há registros a serem atualizados.")
			sys.exit("Encerrando Serviço de Atuliazação.")
		for line in infile:
		
			try:
				if(rest == 5):
					rest = 0
					log.info("Standy by por 5s")
					sleep(2)

				executor.execute(line, multi=True)
				n_updates = n_updates +1
				rest = rest +1
				sleep(0.5)
				log.info("Executando Querys n°{0}".format(n_updates))
			except mysql.connector.Error as err:
				log.info('Erro ao Atualiza o Banco de Dados! Erro {0}'.format(err))
				sys.exit("[!]Não foi possivel Atualiza a base de dados! Erro {0}".format(err))
		return n_updates
	
	else:
		log.info("Arquivo não encontrado!")
		return 0
	


def db_handler():
	log = logging.getLogger('db_handler')
	log.info('iniciando conexão com Banco de Dados.')
	try:
		mydb = mysql.connector.connect(
			host="10.255.237.4",
			user="bwadmin",
			passwd="8bNmFLiIPhVRrM",
			database="megasorte"

		)
		log.info('Conexão estabelecida com Sucesso!')
		return mydb
	except mysql.connector.Error as err:
		log.info('Erro ao conecar com o Banco de Dados:{0}'.format(err))
		sys.exit("[!]Não foi possivel conectar a base de dados! Erro {0}".format(err))  


if __name__ == "__main__":
	start_time = time.time()
	logging.basicConfig(
		filename='/home/{0}/PythonServer/logs/Databaseupdate.log'.format(USER),
		filemode='a+',
		level=logging.INFO,
		format='PID %(process)5s %(name)18s: %(message)s',
		#stream=sys.stderr,
 	)
	log = logging.getLogger('Serviço de Atualização da Base de Dados')
	log.info('*******')
	log.info('Inicializando serviço  de Atualização da Base de Dados')
	log.info(datetime.datetime.now())
	db = db_handler()
	result = QueryRunner(db)
	log.info('Serviço de Atualização da Base de Dados Concluido')
	log.info('{0} registros foram Atualizados'.format(result))
	
	agora = datetime.datetime.now()
	

	if result > 0:

		os.system("mv  /home/"+USER+"/PythonServer/query.txt query_old-"+str(agora.hour)+":"+str(agora.minute)+".txt ")
		os.system("touch /home/{0}/PythonServer/query.txt".format(USER))
	log.info("Encerrando Serviço de Atuliazação.")
	log.info('*******')
	
