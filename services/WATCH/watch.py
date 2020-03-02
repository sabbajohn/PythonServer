#!/usr/bin/python3
# coding: utf-8
import sys
import os
import logging
import time
import datetime
import requests
import socket
import getopt
import threading
import subprocess
import logging
import json

class Watch(object):
	def __init__(self, M):

		self.Manager 		= M
		""" self.controle 		= self.Manager.getControle('modulos')
		self.controle_api	= self.Manager.getControle('api')
		self.watch_vars		= self.Manager.getControle('watch') """
		self.services=['sms','svc','src','sdu','api','SELFDESTROY', 'reload']

		try:
			self.target				= self.watch_vars.addr
		except:
			self.target = '0.0.0.0'
		try:
			self.port				= self.watch_vars.port
		except:
			self.port = 5000


		# read in the buffer from the commandline
		# # this will block, so send CTRL-D if not sending input
		# to stdin

	def start(self):
		message = []
		message.append("Inicializando Watcher")
		self.feedback(metodo="__init__", status =5, message = message, erro = False)
		message = None
		
		self.server_loop()

	def server_loop(self):

		#TODO: RESTART Watch caso de falha de endereço em uso
		# if no target is defined we listen on all interfaces
		if not len(self.target):
			self.target = "0.0.0.0"

		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.bind((self.target,self.port))
				
		server.listen(5)
				
		while True:
			client_socket, addr = server.accept()
			client_socket.settimeout(600)
			# spin off a thread to handle our new client
			message = []
			message.append("Iniciando nova conexão")
			self.feedback(metodo="server_loop", status =5, message = message, erro = False)
			message = None
			client_thread = threading.Thread(target=self.client_handler,args=(client_socket,),name="Watcher client")
			client_thread.start()

	def client_handler(self,client_socket):
		while True:
				
			# show a simple prompt
			""" try:	
				#client_socket.send(bytes('SERVICES:#> ','utf-8'))
			except BrokenPipeError:
				return
 """
			# now we receive until we see a linefeed (enter key)
			cmd_buffer = ""
			while "\n" not in cmd_buffer:
				try:
					cmd_buffer += str(client_socket.recv(4096),encoding="utf-8").rstrip()
					if len(cmd_buffer):
						
						if 'exit' in cmd_buffer or  cmd_buffer == '0':
						return
						else:
							buffer = json.loads(cmd_buffer)
							r = self.buffer_recv(buffer,client_socket)
						if(r):
							client_socket.send(bytes(json.dumps(r).encode()))
							cmd_buffer = ''
						else:
							continue
					break
					
				except TimeoutError:
					message = []
					message.append("Didn't receive data! [Timeout]")
					self.feedback(metodo="client_handler", status =5, message = message, erro = False)
					message = None
					
					return
				except ConnectionResetError:
					return

				except Exception as e:
					message = []
					message.append(type(e))
					message.append(e)

					self.feedback(metodo="client_handler", status =5, message = message, erro = False, comments="Era para ser code 4 mas ainda preciso remodelar os erros")
					message = None
					break
				continue

	def buffer_recv(self, buffer,client_socket):
		servico = buffer['servico']
		action = buffer['action']
		if "parar" in action:
			try:
				self.Manager.finaliza(servico)
			except:
				return {"erro":True,"message":"Não Foi possvel Finalizar a Tarefa"}
			else:
				return {"message":"Serviço {} finalizado com Sucesso!".format(servico), "success":True}
			
		elif "up" in action:
			try:
				self.Manager.inicia(servico)
			except Exception as e:
				return {"erro":True,"message":"Não Foi possvel agendar o inicio desta Tarefa"}
			else:
				return {"message":"Serviço {} será iniado de acordo com seu agendamento padrão!".format(servico), "success":True}
			
		elif "executar_agora" in action:
			try:
				self.Manager.run(servico)
			except:
				return {"erro":True,"message":"Não Foi possvel Executa esta Tarefa"}
			else:
				return {"message":"Serviço {} está sendo Executado!".format(servico), "success":True}
			self.Manager.run(servico)
		elif "info" in action:
			if 'SMS' in servico:	
				return self.Manager.SMS_info
			elif 'SRC' in servico:
				return self.Manager.SRC_info
			elif 'SVC' in servico:
				return self.Manager.SVC_info
			elif 'SDU' in servico:
				return self.Manager.SDU_info
		elif "query" in action:
			data = {}
			data['query_set']= self.Manager.SVC_info['query_set']
			data['query']= self.Manager.SVC_info['query']
			client_socket.send(bytes(json.dumps(data).encode()))
			
			while recv_len:
				data	 = str(client_socket.recv(4096),encoding="utf-8").rstrip()
				recv_len = len(data)
				response+= data
		
				if recv_len < 4096:
					break
			if len(response):
				response = json.loads(response)
				if "query_set" in response['action']:
					if len(response['value']):
						self.Manager.SVC_info['query_set'] = response["value"].split(",")
					data = self.Manager.SVC_info
					data['init_time'] = str(data['init_time'])
					data['next_run'] = str(data['next_run'])
					if data['next_run']:
						data['next_run'] = str(data['next_run'])
					client_socket.send(bytes(json.dumps(data).encode()))
				elif 'query' in response['action']:
					if len (response['value']):
						self.Manager.SVC_info['query_set'].append(response["value"])
					data = self.Manager.SVC_info
					data['init_time'] = str(data['init_time'])
					data['next_run'] = str(data['next_run'])
					if data['next_run']:
						data['next_run'] = str(data['next_run'])
					client_socket.send(bytes(json.dumps(data).encode()))
				else:
					return False
			
			

			

	def job_info(self, service,client_socket ):
		if 'sms' in service :
			pass
		elif 'svc' in service :
			pass
		elif 'sdu' in service:
			pass
		elif 'src' in service :
			pass
		elif 'api' in service:
			pass
		elif 'SELFDESTROY' in service :
			message = []
			message.append("!!! Comando de Autodestruição recebido!")
			self.feedback(metodo="job_info", status =5, message = message, erro = False)
			message = None
			
			os.system("sudo pkill python3")
		elif service == '' or len(service)<3:
			return ''
		else:
			return bytes("help",'utf-8')

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
			"class":"Watch",
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

		self.Manager.callback(feedback)

	def reload(self,service = "all"):
		message = []
		message.append("Recarregando configurações e parametros. Modulo:{0}".format(service))
		self.feedback(metodo="reload", status =5, message = message, erro = False)
		message = None
		try:
			# Registrar Logs
			# Pausa todo mundo, recarrega a classe Controle e re-atribui os valores
			# para os serviços
			self.Manager.finaliza(service)
			self.Manager.Controle(self.Manager,service)
			self.Manager.inicia(service)
			message = []
			message.append("Configurações e Parametros Recarregados:{0}".format(service))
			self.feedback(metodo="reload", status =5, message = message, erro = False)
			message = None
			return True
		except Exception as e:
			message = []
			message.append(type(e))
			message.append(e)
			self.feedback(metodo="reload", status =5, message = message, erro = False)
			message = None
			
			return False
	

	