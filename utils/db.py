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
	def __init__(self, M):
		self.Manager = M
		message = []
		message.append("Iniciando conexões com o Banco de Dados!")
		self.feedback(metodo="__init__", status =5, message = message, erro = False)
		message = None
		self.feedback()
		db_conf = self.Manager.getControle("db")
		
		db_w= db_conf.MYSQL_W.__dict__
		db_w["raise_on_warnings"] = bool(db_w["raise_on_warnings"] )
		db_r=db_conf.MYSQL_R.__dict__
		db_r["raise_on_warnings"] = bool(db_w["raise_on_warnings"] )
	
	
	
		
		
		try:
			self.connection_pool={}
			self.connection_pool['W'] = mysql.connector.pooling.MySQLConnectionPool(pool_name="W", pool_size=10, **db_w)
			self.connection_pool['R'] = mysql.connector.pooling.MySQLConnectionPool(pool_name="R", pool_size=10, **db_r)
			message = []
			message.append("Conexões estabelecidas com Sucesso!")
			
			self.feedback(metodo="__init__", status =5, message = message, erro = False)
			message = None
		
			
		except mysql.connector.Error as err:
			
			message = []
			message.append(err)
			message.append("FALHA NO BANCO DE DADOS, TODAS AS TAREFAS SERÂO ENCERRADAS!")
			self.feedback(metodo="__init__", status =3, message = message, erro = True, comments="")
			message = None
			raise Exception("DB ERRO KILL_ALL")
			sys.exit()
		except Exception as e:
			message = []
			message.append(type(e))
			message.append(e)
			self.feedback(metodo="__init__", status =3, message = message, erro = True, comments="")
			message = None
			raise Exception("DB ERRO KILL_ALL")
			sys.exit()

		
	def getConn(self, mode):
		try:
			conn = self.connection_pool[mode].get_connection()
			return conn
		except Exception as e:
			message = []
			message.append(type(e))
			message.append(e)
			self.feedback(metodo="getConn", status =3, message = message, erro = True, comments="")
			message = None

	def closeConn(self,mode):
		try:
			A = self.Conns[mode]
			self.Conns[mode].close()
			
			return False
		except Exception as e:
			message = []
			message.append(type(e))
			message.append(e)
			self.feedback(metodo="closeConn", status =3, message = message, erro = True, comments="")
			message = None

	def getCursor(self, mode):
		try:
			conn =  self.connection_pool[mode].get_connection()
			return conn.cursor()
	
		except Exception as e:
			message = []
			message.append(type(e))
			message.append(e)
			self.feedback(metodo="getCursor", status =3, message = message, erro = True, comments="")
			message = None
		



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
				message = []
				message.append(err)
				self.feedback(metodo="execute", status =3, message = message, erro = True, comments="")
				message = None
		
			
		if args:
			cursor.execute(sql, args)
		else:
			try:
				cursor.execute(sql)
			except mysql.connector.Error as err:
				message = []
				message.append(err)
				self.feedback(metodo="execute", status =3, message = message, erro = True, comments="")
				message = None
		
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
		
		feedback['time'] =str( datetime.datetime.now())
		#with self._lock:
		self.Manager.callback(feedback)
