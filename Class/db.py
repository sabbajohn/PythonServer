#!/usr/bin/python3
# coding: utf-8
import sys
import os
import mysql.connector
import logging
class DB(object):
	def __init__(self):
		try:
			log = logging.getLogger('Banco de Dados')
			log.info('iniciando conexão com Banco de Dados.')
			self.mydb = mysql.connector.connect(
			host="10.255.237.4",
			user="bwadmin",
			passwd="8bNmFLiIPhVRrM",
			database="megasorte"
    	    )
			log.info('Conexão esstabelecida com Sucesso!')
			self.mydb.autocommit = False
		except mysql.connector.Error as err:
			log.info('Erro ao conecar com o Banco de Dados.')
			sys.exit("[!]Não foi possivel conectar a base de dados! Erro {}".format(err))  
		
	def handler(self):
		return self.mydb

	def getCursor(self):
		return self.mydb.cursor
	
	



		