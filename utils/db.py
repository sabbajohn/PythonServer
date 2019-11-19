#!/usr/bin/python3
# coding: utf-8
import sys
import os
import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling
import logging
import configparser
import config
import datetime

class DB:
	""" TODO: Definir execute e commit dentro desta classe """
	def __init__(self, M):
		self.Manager = M
		self.log = logging.getLogger('Banco de Dados')
		self.log.info('iniciando conexão com Banco de Dados.')
		self.Config =   configparser.ConfigParser()
		self.Config.read("config/DEFAULT.ini")
		self.Config_ENV =   configparser.ConfigParser()
		self.Config_ENV.read("config/{0}.ini".format(self.Config.get("KEY", "env")))

		
	
	
	
		db_W ={ 
			"host":self.Config_ENV.get("MYSQL_W","host"),
			"user":self.Config_ENV.get("MYSQL_W","user"),
			"passwd":self.Config_ENV.get("MYSQL_W","passwd"),
			"database":self.Config_ENV.get("MYSQL_W","database"),
			'raise_on_warnings': self.Config_ENV.getboolean("MYSQL_W", "raise_on_warnings")
		}
		db_R ={
			"host":self.Config_ENV.get("MYSQL_R","host"),
			"user":self.Config_ENV.get("MYSQL_R","user"),
			"passwd":self.Config_ENV.get("MYSQL_R","passwd"),
			"database":self.Config_ENV.get("MYSQL_R","database"),
			'raise_on_warnings': self.Config_ENV.getboolean("MYSQL_R", "raise_on_warnings")
					
		}
		try:
			self.connection_pool={}
			self.connection_pool['W'] = mysql.connector.pooling.MySQLConnectionPool(pool_name="W", pool_size=10, **db_W)
			self.connection_pool['R'] = mysql.connector.pooling.MySQLConnectionPool(pool_name="R", pool_size=10, **db_R)
			self.log.info('Conexões esstabelecida com Sucesso!')
		
			
		except mysql.connector.Error as err:
			self.log.info('Erro ao conecar com o Banco de Dados.')
			message = []
			message.append( "{0}".format(sys.exc_info()[0]))
			message.append("FALHA NO BANCO DE DADOS, TODAS AS TAREFAS SERÂO ENCERRADAS!")
			self.feedback(metodo="__init__", status =4, message = message, erro = True, comments="KILL_ALL")
			message = None
			raise Exception("DB ERRO KILL_ALL")
			sys.exit()
	
		
	def getConn(self, mode):
		try:
			conn = self.connection_pool[mode].get_connection()
			return conn
		except:
			print('erro ao obter conexao')
		
	
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
			conn =  self.connection_pool[mode].get_connection()
			return conn.cursor()
		except:	
			message = []
			message.append( "{0}".format(sys.exc_info()[0]))
			message.append("FALHA NO BANCO DE DADOS, TODAS AS TAREFAS SERÂO ENCERRADAS!")
			self.feedback(metodo="getCursor", status =4, message = message, erro = True)
			message = None
			self.feedback()
			raise Exception("DB ERRO KILL_ALL")
			sys.exit()
		



	def close(self, conn, cursor):
		"""
		A method used to close connection of mysql.
		:param conn: 
		:param cursor: 
		:return: 
		"""
		cursor.close()
		conn.close()

	def execute(self,mode, sql, args=None, commit=False):
		"""
		Execute a sql, it could be with args and with out args. The usage is 
		similar with execute() function in module pymysql.
		:param sql: sql clause
		:param args: args need by sql clause
		:param commit: whether to commit
		:return: if commit, return None, else, return result
		"""
		# get connection form connection pool instead of create one.
		
		try:
			conn = self.getConn(mode)
			cursor = conn.cursor()
			
		except:
			try:
				cursor = self.getCursor(mode)
			except mysql.connector.Error as err:
				print(err)
			
		if args:
			cursor.execute(sql, args)
		else:
			try:
				cursor.execute(sql)
			except mysql.connector.Error as err:
				print(err)
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
	
	#Se o banco der pau tem que parar tudo!
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
			"class":"DB",
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
		
		feedback['time'] =str( datetime.datetime.now())
		#with self._lock:
		self.Manager.callback(feedback)
