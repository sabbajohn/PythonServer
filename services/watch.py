#!/usr/bin/python3
# coding: utf-8
import sys
import os
import logging
import time
import datetime

class Watch(object):
	def __init__(self, M):
		self. Manager = M
		# read in the buffer from the commandline
		# # this will block, so send CTRL-D if not sending input
		# to stdin
		
	def start(self):
		print("Digite o nome do serviço para obter informações\n")
		print("CTRL-D para solicitar informações!\n")
		print("[nome do servico] - Para informações")
		print("[nome do servico] mode up/down - Para para definir se o serviço deve continuar em execucao")
		while True:
			buffer = sys.stdin.read()	
			self.job_info(buffer)
			print("Digite o nome do serviço para obter informações\n")
			print("CTRL-D para solicitar informações!\n")
			print("[nome do servico] - Para informações")
			print("[nome do servico] mode up/down - Para para definir se o serviço deve continuar em execucao")

	def job_info(self, service):
		
		if 'sms' in service :
			if "mode" in service:
				if "up" in service:
					self.Manager.Variaveis_de_controle["SMS"]["keepAlive"] = True	
				elif "down" in service:
					self.Manager.Variaveis_de_controle["SMS"]["keepAlive"] = False	
				else: pass
			status = self.Manager.Jobs['SMS'].isAlive()
			print("Status do Serviço: {0}".format(status))
			print(self.Manager.Variaveis_de_controle["SMS"])
			return
		elif 'svc' in service :
			if "mode" in service:
				if "up" in service:
					self.Manager.Variaveis_de_controle["SVC"]["keepAlive"] = True	
				elif "down" in service:
					self.Manager.Variaveis_de_controle["SVC"]["keepAlive"] = False	
				else: pass
			status = self.Manager.Jobs['SVC'].isAlive()
			print("Status do Serviço: {0}".format(status))
			print(self.Manager.Variaveis_de_controle["SVC"])
			return
		elif 'sdu' in service:
			if "mode" in service:
				if "up" in service:
					self.Manager.Variaveis_de_controle["SDU"]["keepAlive"] = True	
				elif "down" in service:
					self.Manager.Variaveis_de_controle["SDU"]["keepAlive"] = False	
				else: pass
			status = self.Manager.Jobs['SDU'].isAlive()
			print("Status do Serviço: {0}".format(status))
			print(self.Manager.Variaveis_de_controle["SDU"])
			return
		