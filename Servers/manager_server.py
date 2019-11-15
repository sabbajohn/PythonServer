#!/usr/bin/python3
# coding: utf-8
import sys
import os
import time
from time import sleep
import json
from json import dumps
import getpass
USER = getpass.getuser()
sys.path.insert(1,'/home/{0}/PythonServer/Class'.format(USER))
import cpf
from startup import Startup
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import urllib.request
import datetime			


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
		action = request.json['action']
		
		if(service == 'sdu'):
			self.sdu(action)
		elif(service == 'svc'):
			self.svc(action)
		elif(service == 'sms'):
			self.sms(action)
		elif(service == 'startup'):
			self.startup(action)
		elif(service == 'help'):
			self.help()
		else:
			return {
				'erro': 'servico nao definido!'
			}
		
	
	def sms(self, action,):

		if action == 'status':
			status  = Startup.checkIfProcessRunning('sms.py')
			if status:
				return{

					'service':'SMS',
					'status': status,
					'hora': datetime.datetime.now(),
					'message':'O servico esta ativo!'
				}
			else:

				return{

					'service':'SMS',
					'status': status,
					'hora': datetime.datetime.now(),
					'message':'O servico esta parado!',
					'logs': self.tail('logs/sms.log')
				}

		elif action == 'start':
			if not Startup.checkIfProcessRunning('sms.py'):
				try:
					os.system('nohup python3 sms.py &')
					return{
						'service':'SMS',
						'message':'Inicializando servico',
						'hora': datetime.datetime.now(),
						
						
					}
				except :
					return{
						'service':'SMS',
						'message':'Nao foi possivel iniciar o servico',
						'hora': datetime.datetime.now(),
						'logs': self.tail('logs/sms.log')
						
					}
				

			else:
				return{

					'service':'SMS',
					'status': status,
					'hora': datetime.datetime.now(),
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
			status  = Startup.checkIfProcessRunning('Databaseupdate.py')
			if status:
				return{

					'service':'SDU',
					'status': status,
					'hora': datetime.datetime.now(),
					'message':'O servico esta ativo!'
				}
			else:

				return{

					'service':'SDU',
					'status': status,
					'hora': datetime.datetime.now(),
					'message':'O servico esta parado!',
					'logs': self.tail('logs/sdu.log')
				}

		elif action == 'start':
			if not Startup.checkIfProcessRunning('Databaseupdate.py'):
				try:
					os.system('nohup python3 Databaseupdate.py &')
					return{
						'service':'SDU',
						'message':'Inicializando servico',
						'hora': datetime.datetime.now()
						
					}
				except :
					return{
						'service':'SDU',
						'message':'Nao foi possivel iniciar o servico',
						'hora': datetime.datetime.now(),
						'logs': self.tail('logs/sdu.log')
						
					}
				

			else:
				return{

					'service':'SDU',
					'status': status,
					'hora': datetime.datetime.now(),
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
			status  = Startup.checkIfProcessRunning('servico_de_validacao.py')
			if status:
				return{

					'service':'SVC',
					'status': status,
					'hora': datetime.datetime.now(),
					'message':'O servico esta ativo!'
				}
			else:

				return{

					'service':'SVC',
					'status': status,
					'hora': datetime.datetime.now(),
					'message':'O servico esta parado!',
					'logs': self.tail('logs/svc.log')
				}

		elif action == 'start':
			if not Startup.checkIfProcessRunning('servico_de_validacao.py'):
				try:
					os.system('nohup python3 servico_de_validacao.py &')
					return{
						'service':'SVC',
						'message':'Inicializando servico',
						'hora': datetime.datetime.now()
						
					}
				except :
					return{
						'service':'SVC',
						'message':'Nao foi possivel iniciar o servico',
						'hora': datetime.datetime.now(),
						'logs': self.tail('logs/svc.log')
						
					}
				

			else:
				return{

					'service':'SVC',
					'status': status,
					'hora': datetime.datetime.now(),
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
			status  = Startup.checkIfProcessRunning('startup.py')
			if status:
				return{

					'service':'Start up',
					'status': status,
					'hora': datetime.datetime.now(),
					'message':'O servico esta ativo!'
				}
			else:

				return{

					'service':'Start up',
					'status': status,
					'hora': datetime.datetime.now(),
					'message':'O servico esta parado!',
					'logs': self.tail('logs/startup.log')
				}

		elif action == 'start':
			if not Startup.checkIfProcessRunning('startup.py'):
				try:
					os.system('nohup python3 startup.py &')
					return{
						'service':'Start up',
						'message':'Inicializando servico',
						'hora': datetime.datetime.now()
						
					}
				except :
					return{
						'service':'Start up',
						'message':'Nao foi possivel iniciar o servico',
						'hora': datetime.datetime.now(),
						'logs': self.tail('logs/startup.log')
						
					}
				

			else:
				return{

					'service':'Start up',
					'status': status,
					'hora': datetime.datetime.now(),
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

	def tail(self,filename, lines=20 ):
		with open(filename, 'r') as f:
			total_lines_wanted = lines
			BLOCK_SIZE = 1024
			f.seek(0, 2)
			block_end_byte = f.tell()
			lines_to_go = total_lines_wanted
			block_number = -1
			blocks = [] # blocks of size BLOCK_SIZE, in reverse order starting
						# from the end of the file
			while lines_to_go > 0 and block_end_byte > 0:
				if (block_end_byte - BLOCK_SIZE > 0):
					# read the last block we haven't yet read
					f.seek(block_number*BLOCK_SIZE, 2)
					blocks.append(f.read(BLOCK_SIZE))
				else:
					# file too small, start from begining
					f.seek(0,0)
					# only read what was not read
					blocks.append(f.read(block_end_byte))
				lines_found = blocks[-1].count('\n')
				lines_to_go -= lines_found
				block_end_byte -= BLOCK_SIZE
				block_number -= 1
			all_read_text = ''.join(reversed(blocks))
			return '\n'.join(all_read_text.splitlines()[-total_lines_wanted:])

api.add_resource(Command, '/services/') # Route_1



if __name__ == '__main__':
	app.run()

