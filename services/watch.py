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

class Watch(object):
	def __init__(self, M):
	
		self.Manager = M
		self.services=['sms','svc','src','sdu']
		
		try:
			self.target				= self.Manager.Config.get("WATCH","addr")
		except:
			self.target = '0.0.0.0'
		try:
			self.port				= int(self.Manager.Config.get("WATCH","port"))
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
		self.feedback()
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
			try:	
				client_socket.send(bytes('SERVICES:#> ','utf-8'))
			except BrokenPipeError:
				return

			# now we receive until we see a linefeed (enter key)
			cmd_buffer = ""
			while "\n" not in cmd_buffer:
				try:
					cmd_buffer += client_socket.recv(1024).decode('utf-8')
					if len(cmd_buffer)< 3 or cmd_buffer == "\n" or  cmd_buffer =='':
						cmd_buffer = ""
						break
					elif "exit" in cmd_buffer:
						client_socket.sendall("Finalizando cliente, até mais!".encode(encoding='utf-8'))
						return 
					else:
						break
				except TimeoutError:
					message = []
					message.append("Didn't receive data! [Timeout]")
					self.feedback(metodo="client_handler", status =5, message = message, erro = False)
					message = None
					self.feedback()
					return
				except ConnectionResetError:
					return

				except Exception as e:
					message = []
					message.append(type(e))
					message.append(e)

					self.feedback(metodo="client_handler", status =5, message = message, erro = False, comments="Era para ser code 4 mas ainda preciso remodelar os erros")
					message = None
					self.feedback()
			if len(cmd_buffer)< 3 or cmd_buffer == "\n" or  cmd_buffer =='':
				continue

			if  any(srv in cmd_buffer for srv in self.services ):

				# we have a valid command so execute it and send back the results
				message = []
				message.append("Consulta realizada:{0}".format(cmd_buffer))
				self.feedback(metodo="client_handler", status =5, message = message, erro = False)
				message = None
				self.feedback()

				response = self.job_info(cmd_buffer, client_socket)

				# send back the response
				try:
					len(response)>0 
					message = []
					message.append("Resposta encaminhada:{0}".format(response.decode('utf-8')))
					self.feedback(metodo="client_handler", status =5, message = message, erro = False)
					message = None
					self.feedback()
					client_socket.sendall(response)
					continue
				
				except:
					message = []
					message.append("Exceção não tratada")
					message.append(sys.exc_info())

					self.feedback(metodo="client_handler", status =5, message = message, erro = False, comments="Era para ser code 4 mas ainda preciso remodelar os erros")
					message = None
					self.feedback()
					continue
			else:
				message = []
				message.append("Comando não contem nenhum serviço conhecido:{0}".format(cmd_buffer))
				self.feedback(metodo="client_handler", status =5, message = message, erro = False)
				message = None
				self.feedback()
				client_socket.sendall('help'.encode())
				time.sleep(3)
				continue

	
	def job_info(self, service,client_socket ):
		response = "'status':'{0}', 'init':'{1}', 'init_time':'{2}', 'keepAlive': '{3}',  'lasttimerunning':'{4}',  'nextrun':'{5}',  'firstTime':'{6}', 'stop':'{7}' "
		
		service = service.rstrip()
		if 'sms' in service :
			if "mode" in service:
				if "up" in service:
					self.Manager.Variaveis_de_controle["SMS"]["keepAlive"] = True
					self.Manager.verifica()
				elif "down" in service:
					self.Manager.Variaveis_de_controle["SMS"]["keepAlive"] = False
					self.Manager.Variaveis_de_controle["SMS"]["stop"] = True
					self.Manager.verifica()
				else: pass
			if "start" in service:
				if self.Manager.Jobs['SMS'].isAlive():
					message = "SERVIÇO JA ATIVO"
					return message.encode()
				else:
					self.Manager.inicia("sms")
			if "run" in service:
			
				if self.Manager.run('sms'):

					client_socket.send("Serviço executado".encode())
					time.sleep(2)
				else:
					client_socket.send("Não haviam tarefas a serem executadas ou tivemos um erro, verificar logs".encode())
					time.sleep(2)
				
			return bytearray(response.format(self.Manager.Jobs['SMS'].isAlive(),
			 self.Manager.Variaveis_de_controle["SMS"]["init"],
			 self.Manager.Variaveis_de_controle["SMS"]["init_time"],
			 self.Manager.Variaveis_de_controle["SMS"]["keepAlive"],
			 self.Manager.Variaveis_de_controle["SMS"]["lasttimerunning"],
			 self.Manager.Variaveis_de_controle["SMS"]["nextrun"],
			 self.Manager.Variaveis_de_controle["SMS"]["firstTime"],
			 self.Manager.Variaveis_de_controle["SMS"]["stop"]),'utf-8')
			
			
			
			return
		elif 'svc' in service :
			
			if "mode" in service:
				if "up" in service:
					self.Manager.Variaveis_de_controle["SVC"]["keepAlive"] = True
					self.Manager.verifica()
				elif "down" in service:
					self.Manager.Variaveis_de_controle["SVC"]["keepAlive"] = False
					self.Manager.finaliza('svc')
				else: pass

			if "start" in service:
				if self.Manager.Jobs['SVC'].isAlive():
					message = "SERVIÇO JA ATIVO"
					return message.encode()
				else:
					self.Manager.inicia("svc")
			""" if "set" in service: """
			#TODO: Definir qual query será utilizada no processo!



			return bytearray(response.format(self.Manager.Jobs['SVC'].isAlive(),
			 self.Manager.Variaveis_de_controle["SVC"]["init"],
			 self.Manager.Variaveis_de_controle["SVC"]["init_time"],
			 self.Manager.Variaveis_de_controle["SVC"]["keepAlive"],
			 self.Manager.Variaveis_de_controle["SVC"]["lasttimerunning"],
			 self.Manager.Variaveis_de_controle["SVC"]["nextrun"],
			 self.Manager.Variaveis_de_controle["SVC"]["firstTime"],
			 self.Manager.Variaveis_de_controle["SVC"]["stop"]),'utf-8')
		elif 'sdu' in service:
			if "mode" in service:
				if "up" in service:
					self.Manager.Variaveis_de_controle["SDU"]["keepAlive"] = True
					self.Manager.verifica()
				elif "down" in service:
					self.Manager.Variaveis_de_controle["SDU"]["keepAlive"] = False	
					self.Manager.finaliza('sdu')
				else: pass
			if "start" in service:
				if self.Manager.Jobs['SDU'].isAlive():
					message = "SERVIÇO JA ATIVO"
					return message.encode()
				else:
					self.Manager.inicia("sdu")
		
			return bytearray(response.format(self.Manager.Jobs['SDU'].isAlive(),
			 self.Manager.Variaveis_de_controle["SDU"]["init"],
			 self.Manager.Variaveis_de_controle["SDU"]["init_time"],
			 self.Manager.Variaveis_de_controle["SDU"]["keepAlive"],
			 self.Manager.Variaveis_de_controle["SDU"]["lasttimerunning"],
			 self.Manager.Variaveis_de_controle["SDU"]["nextrun"],
			 self.Manager.Variaveis_de_controle["SDU"]["firstTime"],
			 self.Manager.Variaveis_de_controle["SDU"]["stop"]),'utf-8')
		elif 'src' in service :
			if "mode" in service:
				if "up" in service:
					self.Manager.Variaveis_de_controle["SRC"]["keepAlive"] = True
					self.Manager.verifica()
				elif "down" in service:
					self.Manager.Variaveis_de_controle["SRC"]["keepAlive"] = False
					self.Manager.Variaveis_de_controle["SRC"]["stop"] = True
					self.Manager.verifica()
				else: pass
			if "start" in service:
				if self.Manager.Jobs['SRC'].isAlive():
					message = "SERVIÇO JA ATIVO"
					return message.encode()
				else:
					self.Manager.inicia("src")
			if "run" in service:
			
				if self.Manager.run('src'):

					client_socket.send("Serviço executado".encode())
					time.sleep(2)
				else:
					client_socket.send("Não haviam tarefas a serem executadas ou tivemos um erro, verificar logs".encode())
					time.sleep(2)
			return bytearray(response.format(self.Manager.Jobs['SRC'].isAlive(),
			 self.Manager.Variaveis_de_controle["SRC"]["init"],
			 self.Manager.Variaveis_de_controle["SRC"]["init_time"],
			 self.Manager.Variaveis_de_controle["SRC"]["keepAlive"],
			 self.Manager.Variaveis_de_controle["SRC"]["lasttimerunning"],
			 self.Manager.Variaveis_de_controle["SRC"]["nextrun"],
			 self.Manager.Variaveis_de_controle["SRC"]["firstTime"],
			 self.Manager.Variaveis_de_controle["SRC"]["stop"]),'utf-8')
		elif 'SELFDESTROY' in service :
			message = []
			message.append("!!! Comando de Autodestruição recebido!")
			self.feedback(metodo="job_info", status =5, message = message, erro = False)
			message = None
			self.feedback()
			os.system("pkill python3")
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

		self.Manager.callback(feedback)
