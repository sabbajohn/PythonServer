#!/usr/bin/python3
# coding: utf-8
import sys
import os
import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling
import logging

class DB(object):
	""" TODO: Definir execute e commit dentro desta classe """
	def __init__(self):
		self.log = logging.getLogger('Banco de Dados')
		self.log.info('iniciando conexão com Banco de Dados.')
		db_W ={ 
					"host":"10.255.237.4",
					"user":"bwadmin",
					"passwd":"8bNmFLiIPhVRrM",
					"database":"megasorte",
					'raise_on_warnings': True
					}
		db_R ={ 
					"host":"megasorte-homol-read.cwixh7j3qfsl.us-east-1.rds.amazonaws.com",
					"user":"bwadmin",
					"passwd":"8bNmFLiIPhVRrM",
					"database":"megasorte",
					'raise_on_warnings': True
					
					}
		try:
		
			self.connection_pool={}
			self.connection_pool['W'] = mysql.connector.pooling.MySQLConnectionPool(pool_name="W", pool_size=10, **db_W)
			self.connection_pool['R'] = mysql.connector.pooling.MySQLConnectionPool(pool_name="R", pool_size=10, **db_R)
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



	def close(self, conn, cursor):
		"""
		A method used to close connection of mysql.
		:param conn: 
		:param cursor: 
		:return: 
		"""
		cursor.close()
		conn.close()

	def execute(self, sql, args=None, commit=False):
		"""
		Execute a sql, it could be with args and with out args. The usage is 
		similar with execute() function in module pymysql.
		:param sql: sql clause
		:param args: args need by sql clause
		:param commit: whether to commit
		:return: if commit, return None, else, return result
		"""
		# get connection form connection pool instead of create one.
		conn = self.pool.get_connection()
		cursor = conn.cursor()
		if args:
			cursor.execute(sql, args)
		else:
			cursor.execute(sql)
		if commit is True:
			conn.commit()
			self.close(conn, cursor)
			return None
		else:
			res = cursor.fetchall()
			self.close(conn, cursor)
			return res

	def executemany(self, sql, args, commit=False):
		"""
		Execute with many args. Similar with executemany() function in pymysql.
		args should be a sequence.
		:param sql: sql clause
		:param args: args
		:param commit: commit or not.
		:return: if commit, return None, else, return result
		"""
		# get connection form connection pool instead of create one.
		conn = self.pool.get_connection()
		cursor = conn.cursor()
		cursor.executemany(sql, args)
		if commit is True:
			conn.commit()
			self.close(conn, cursor)
			return None
		else:
			res = cursor.fetchall()
			self.close(conn, cursor)
			return res
