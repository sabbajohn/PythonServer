#!/usr/bin/python3
# coding: utf-8
import sys
import os
import time
from time import sleep
import json
from json import dumps
import getpass
from Class import cpf
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import urllib.request
import datetime			
import subprocess
import codecs
USER = getpass.getuser()
app = Flask(__name__)
api = Api(app)


class Status(Resource):
	"""  def get(self):
		conn = db_connect.connect() # connect to database
		query = conn.execute("select * from employees") # This line performs query and returns json result
		return {'employees': [i[0] for i in query.cursor.fetchall()]} # Fetches first column that is Employee ID """

	def post(self):
		resp = []
		print(request.json)
	
class Command(Resource):

	def post(self):
		resp = []
		print(request.json)
		service = request.json['service']
		try:
			action = request.json['action']
		except:
			pass

		
		if(service == 'sdu'):
			return self.sdu(action)
		elif(service == 'svc'):
			return self.svc(action)
		elif(service == 'sms'):
			return self.sms(action)
		elif(service == 'startup'):
			return self.startup(action)
		elif(service == 'nohup'):
			self.tail('nohup.out')
		else:
			return {
				'erro': 'servico nao definido!'
			}
		
	
	def sms(self, action,):

		if action == 'status':
			status  = self.checkIfProcessRunning('sms.py')
			if status:
				return{

					'service':'SMS',
					'status': status,
					'hora': str(datetime.datetime.now().strftime(" %H:%i:%s %d/%m/%Y")),
					'message':'O servico esta ativo!'
				}
			else:

				return{

					'service':'SMS',
					'status': status,
					'hora': str(datetime.datetime.now().strftime(" %H:%i:%s %d/%m/%Y")),
					'message':'O servico esta parado!',
					'logs': self.tail('logs/sms.log')
				}

		elif action == 'start':
			if not self.checkIfProcessRunning('sms.py'):
				try:
					os.system('nohup python3 sms.py &')
					return{
						'service':'SMS',
						'message':'Inicializando servico',
						'hora': str(datetime.datetime.now().strftime(" %H:%i:%s %d/%m/%Y")),
						
						
					}
				except :
					return{
						'service':'SMS',
						'message':'Nao foi possivel iniciar o servico',
						'hora': str(datetime.datetime.now().strftime(" %H:%i:%s %d/%m/%Y")),
						'logs': self.tail('logs/sms.log')
						
					}
				

			else:
				return{

					'service':'SMS',
					'status': status,
					'hora': str(datetime.datetime.now().strftime(" %H:%i:%s %d/%m/%Y")),
					'message':'O servico ja esta ativo!'
				}
				
		elif action == 'stop':
			pass
		elif action == 'restart':
			pass
		else:
			self.help()

	def sdu(self, action):
		if action == 'status':
			status  = self.checkIfProcessRunning('Databaseupdate.py')
			if status:
				return{

					'service':'SDU',
					'status': status,
					'hora': str(datetime.datetime.now().strftime(" %H:%i:%s %d/%m/%Y")),
					'message':'O servico esta ativo!'
				}
			else:

				return{

					'service':'SDU',
					'status': status,
					'hora': str(datetime.datetime.now().strftime(" %H:%i:%s %d/%m/%Y")),
					'message':'O servico esta parado!',
					'logs': self.tail('logs/sdu.log')
				}

		elif action == 'start':
			if not self.checkIfProcessRunning('Databaseupdate.py'):
				try:
					os.system('nohup python3 Databaseupdate.py &')
					return{
						'service':'SDU',
						'message':'Inicializando servico',
						'hora': str(datetime.datetime.now().strftime(" %H:%i:%s %d/%m/%Y"))
						
					}
				except :
					return{
						'service':'SDU',
						'message':'Nao foi possivel iniciar o servico',
						'hora': str(datetime.datetime.now().strftime(" %H:%i:%s %d/%m/%Y")),
						'logs': self.tail('logs/sdu.log')
						
					}
				

			else:
				return{

					'service':'SDU',
					'status': status,
					'hora': str(datetime.datetime.now().strftime(" %H:%i:%s %d/%m/%Y")),
					'message':'O servico ja esta ativo!'
				}
		elif action == 'stop':
			pass
		elif action == 'restart':
			pass
		else:
			self.help()

	def svc(self, action):
		if action == 'status':
			status  = self.checkIfProcessRunning('servico_de_validacao.py')
			if status:
				return{

					'service':'SVC',
					'status': status,
					'hora': str(datetime.datetime.now().strftime(" %H:%i:%s %d/%m/%Y")),
					'message':'O servico esta ativo!'
				}
			else:

				return{

					'service':'SVC',
					'status': status,
					'hora': str(datetime.datetime.now().strftime(" %H:%i:%s %d/%m/%Y")),
					'message':'O servico esta parado!',
					'logs': self.tail('logs/svc.log')
				}

		elif action == 'start':
			if not self.checkIfProcessRunning('servico_de_validacao.py'):
				try:
					os.system('nohup python3 servico_de_validacao.py &')
					return{
						'service':'SVC',
						'message':'Inicializando servico',
						'hora': str(datetime.datetime.now().strftime(" %H:%i:%s %d/%m/%Y"))
						
					}
				except :
					return{
						'service':'SVC',
						'message':'Nao foi possivel iniciar o servico',
						'hora': str(datetime.datetime.now().strftime(" %H:%i:%s %d/%m/%Y")),
						'logs': self.tail('logs/svc.log')
						
					}
				

			else:
				return{

					'service':'SVC',
					'status': status,
					'hora': str(datetime.datetime.now().strftime(" %H:%i:%s %d/%m/%Y")),
					'message':'O servico ja esta ativo!'
				}

		elif action == 'stop':
			pass
		elif action == 'restart':
			pass
		else:
			self.help()
	
	def startup(self, action):
		if action == 'status':
			status  = self.checkIfProcessRunning('startup.py')
			if status:
				return{

					'service':'Start up',
					'status': status,
					'hora': str(datetime.datetime.now().strftime(" %H:%i:%s %d/%m/%Y")),
					'message':'O servico esta ativo!'
				}
			else:

				return{

					'service':'Start up',
					'status': status,
					'hora': str(datetime.datetime.now().strftime(" %H:%i:%s %d/%m/%Y")),
					'message':'O servico esta parado!',
					'logs': self.tail('logs/startup.log')
				}

		elif action == 'start':
			if not self.checkIfProcessRunning('startup.py'):
				try:
					os.system('nohup python3 startup.py &')
					return{
						'service':'Start up',
						'message':'Inicializando servico',
						'hora': str(datetime.datetime.now().strftime(" %H:%i:%s %d/%m/%Y"))
						
					}
				except :
					return{
						'service':'Start up',
						'message':'Nao foi possivel iniciar o servico',
						'hora': str(datetime.datetime.now().strftime(" %H:%i:%s %d/%m/%Y")),
						'logs': self.tail('logs/startup.log')
						
					}
				

			else:
				return{

					'service':'Start up',
					'status': status,
					'hora': str(datetime.datetime.now().strftime(" %H:%i:%s %d/%m/%Y")),
					'message':'O servico ja esta ativo!'
				}
		elif action == 'stop':
			pass
		elif action == 'restart':
			pass
		else:
			self.help()

	def help(self):
		pass
	def tail(self, f, n=20, offset=0):
		proc = subprocess.Popen(['tail', '-n', str(n+offset),f ], stdout=subprocess.PIPE)
		lines= [x.decode('utf8') for x in proc.stdout.readlines()]
		return lines[:]
		
	
	def checkIfProcessRunning(self,processName):
		'''
		Check if there is any running process that contains the given name processName.
		'''
		#Iterate over the all the running process

		ps = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE).communicate()[0]
		processes = ps.decode().split('\n')
		# this specifies the number of splits, so the splitted lines
		# will have (nfields+1) elements
		nfields = len(processes[0].split()) - 1
		
		for row in processes[1:]:
			try:
				proc = row.split(None, nfields)
				if len(proc)>0:

					# Check if process name contains the given name string.
					if processName.lower() in proc[10].lower():
						return True
				else: 
					pass
			except:
				pass
		return False 

		
	

	
api.add_resource(Command, '/services/') # Route_1



if __name__ == '__main__':
	app.run()

