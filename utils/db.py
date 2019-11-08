#!/usr/bin/python3
# coding: utf-8
import sys
import os
import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling
import logging

class DB(object):
	def __init__(self):
		self.log = logging.getLogger('Banco de Dados')
		self.log.info('iniciando conexão com Banco de Dados.')
		dbconfig1 ={ 
					"host":"10.255.237.4",
					"user":"bwadmin",
					"passwd":"8bNmFLiIPhVRrM",
					"database":"megasorte"
					}
		dbconfig2 ={ 
					"host":"megasorte-homol-read.cwixh7j3qfsl.us-east-1.rds.amazonaws.com",
					"user":"bwadmin",
					"passwd":"8bNmFLiIPhVRrM",
					"database":"megasorte"
					
					}
		try:
		
			self.connection_pool={}
			self.connection_pool['W'] = mysql.connector.pooling.MySQLConnectionPool(pool_name="W", pool_size=5, **dbconfig1)
			self.connection_pool['R'] = mysql.connector.pooling.MySQLConnectionPool(pool_name="R", pool_size=5, **dbconfig2)
			#self.connection_pool['W'].autocommit = True
			self.log.info('Conexões esstabelecida com Sucesso!')
		
			self.Conns={}
			self.Conns["W"]	= self.getConn("W")
			self.Conns["R"] = self.getConn("R")
		except mysql.connector.Error as err:
			self.log.info('Erro ao conecar com o Banco de Dados.')
			sys.exit("[!]Não foi possivel conectar a base de dados! Erro {}".format(err))  

			
		
	
		
	def getConn(self, mode):
		try:
			A = self.Conns[mode]
			return self.Conns[mode]
		except:
			self.Conns[mode] = self.connection_pool[mode].get_connection()
			return self.Conns[mode]
	
	def closeConn(self,mode):
		try:
			A = self.Conns[mode]
			self.Conns[mode].close()
			
			return False
		except mysql.connector.Error as err:
			self.log.info('Erro ao conecar com o Banco de Dados.')
			sys.exit("[!]Não foi possivel conectar a base de dados! Erro {}".format(err))  

	def getCursor(self, mode):
		try:
			A = self.Conns[mode]
			return self.Conns[mode].cursor()
		except:	
			self.Conns[mode] =  self.connection_pool[mode].get_connection()
			return self.Conns[mode].cursor()