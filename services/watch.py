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
		self.log = logging.getLogger('Watcher')
		
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
	
	def client_handler(self,client_socket):
		""" self.usage(client_socket) """
		while True:
				# show a simple prompt
				client_socket.send(str.encode("<SERVICES:#>"))
				
				# now we receive until we see a linefeed (enter key)
				cmd_buffer = ""
				while "\n" not in cmd_buffer:
					try:
						cmd_buffer += client_socket.recv(1024).decode()
						if cmd_buffer =="\n":
							cmd_buffer = ""
						if "exit" in cmd_buffer:
							return 
					except:
						return
	
		
				
				# we have a valid command so execute it and send back the results
				self.log.info("Consulta realizada:{0}".format(cmd_buffer))
				response = self.job_info(cmd_buffer, client_socket)
				
				# send back the response
				try:
					len(response)>0 
					client_socket.sendall(response)
					self.log.info("Resposta encaminhada:{0}".format(response))
					
				except:
					pass

	def server_loop(self):
				
		# if no target is defined we listen on all interfaces
		if not len(self.target):
			self.target = "0.0.0.0"

		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.bind((self.target,self.port))
				
		server.listen(5)
				
		while True:
			client_socket, addr = server.accept()

			# spin off a thread to handle our new client
			self.log.info("Inicializando conexão")
			client_thread = threading.Thread(target=self.client_handler,args=(client_socket,),name="Watcher client")
			client_thread.start()
	
	""" def usage(self,client_socket):
		msg1 = "\tGerenciamento de Servicos v2.0\r"
		msg2 = "Uso:\r[servico]\t - \t #> Informacoes gerais\r[nome do servico] mode [up/down]\t - \t #> Iniciar ou parar serviço\n"
		msg3 ="\t\t by John. Sabbá\n"
		client_socket.sendall(str.encode("{}{}{}".format(msg1,msg2,msg3))) """

	def start(self):
		self.log.info("Inicializando Watcher")
		self.server_loop()

	def job_info(self, service,client_socket ):
		response = "status:{0}\ninit:{1}\ninit_time:{2}\nkeepAlive: {3}\nlasttimerunning:{4}\nnextrun:{5}\nfirstTime:{6}\nstop:{7}"
		
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
				
			return str.encode(response.format(self.Manager.Jobs['SMS'].isAlive(),
			 self.Manager.Variaveis_de_controle["SMS"]["init"],
			 self.Manager.Variaveis_de_controle["SMS"]["init_time"],
			 self.Manager.Variaveis_de_controle["SMS"]["keepAlive"],
			 self.Manager.Variaveis_de_controle["SMS"]["lasttimerunning"],
			 self.Manager.Variaveis_de_controle["SMS"]["nextrun"],
			 self.Manager.Variaveis_de_controle["SMS"]["firstTime"],
			 self.Manager.Variaveis_de_controle["SMS"]["stop"]))
			
			
			
			return
		elif 'svc' in service :
			
			if "mode" in service:
				if "up" in service:
					self.Manager.Variaveis_de_controle["SVC"]["keepAlive"] = True
					self.Manager.verifica()
				elif "down" in service:
					self.Manager.Variaveis_de_controle["SVC"]["keepAlive"] = False
					self.Manager.finaliza()
				else: pass

			if "start" in service:
				if self.Manager.Jobs['SVC'].isAlive():
					message = "SERVIÇO JA ATIVO"
					return message.encode()
				else:
					self.Manager.inicia("svc")
			""" if "set" in service: """
			#TODO: Definir qual query será utilizada no processo!



			return str.encode(response.format(self.Manager.Jobs['SVC'].isAlive(),
			 self.Manager.Variaveis_de_controle["SVC"]["init"],
			 self.Manager.Variaveis_de_controle["SVC"]["init_time"],
			 self.Manager.Variaveis_de_controle["SVC"]["keepAlive"],
			 self.Manager.Variaveis_de_controle["SVC"]["lasttimerunning"],
			 self.Manager.Variaveis_de_controle["SVC"]["nextrun"],
			 self.Manager.Variaveis_de_controle["SVC"]["firstTime"],
			 self.Manager.Variaveis_de_controle["SVC"]["stop"]))
		elif 'sdu' in service:
			if "mode" in service:
				if "up" in service:
					self.Manager.Variaveis_de_controle["SDU"]["keepAlive"] = True
					self.Manager.verifica()
				elif "down" in service:
					self.Manager.Variaveis_de_controle["SDU"]["keepAlive"] = False	
					self.Manager.finaliza()
				else: pass
			if "start" in service:
				if self.Manager.Jobs['SDU'].isAlive():
					message = "SERVIÇO JA ATIVO"
					return message.encode()
				else:
					self.Manager.inicia("sdu")
		
			return str.encode(response.format(self.Manager.Jobs['SDU'].isAlive(),
			 self.Manager.Variaveis_de_controle["SDU"]["init"],
			 self.Manager.Variaveis_de_controle["SDU"]["init_time"],
			 self.Manager.Variaveis_de_controle["SDU"]["keepAlive"],
			 self.Manager.Variaveis_de_controle["SDU"]["lasttimerunning"],
			 self.Manager.Variaveis_de_controle["SDU"]["nextrun"],
			 self.Manager.Variaveis_de_controle["SDU"]["firstTime"],
			 self.Manager.Variaveis_de_controle["SDU"]["stop"]))
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
				
			return str.encode(response.format(self.Manager.Jobs['SRC'].isAlive(),
			 self.Manager.Variaveis_de_controle["SRC"]["init"],
			 self.Manager.Variaveis_de_controle["SRC"]["init_time"],
			 self.Manager.Variaveis_de_controle["SRC"]["keepAlive"],
			 self.Manager.Variaveis_de_controle["SRC"]["lasttimerunning"],
			 self.Manager.Variaveis_de_controle["SRC"]["nextrun"],
			 self.Manager.Variaveis_de_controle["SRC"]["firstTime"],
			 self.Manager.Variaveis_de_controle["SRC"]["stop"]))
			
			
			
			return
		else:
			return None