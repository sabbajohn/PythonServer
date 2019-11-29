#!/usr/bin/python3
# coding: utf-8
import sys
import os
import time
from time import sleep
import json
from json import dumps
import getpass
from utils import cpf
from utils.Relatorios import Relatorios as log
USER = getpass.getuser()
if sys.version_info[0] < 3:

	raise Exception("[!]Must be using Python 3, You can install it using: # apt-get install python3")
try:
	from flask import Flask, request, jsonify
except:
	try:
		comando = os.system
		comando('pip3 install flask')
		print('[!] Tentando Instalar as Dependencias')	
	except :
		if IOError:	
			sys.exit("[!] Please install the flask library: pip install flask")
		else:
			sleep(7) 
			comando('python3 server.py')

	
	
try:
   from flask_restful import Resource, Api
except:
	try:
		comando = os.system
		comando('pip3 install flask_restful')
		print('[!] Tentando Instalar as Dependencias')
	except:
		if IOError:	
			sys.exit("[!] Please install the flask_restful library: pip3 install flask_restful")	
		
		else:  
			sleep(10)   
			comando('python3 server.py')	
		
try:
  import urllib.request
except:
	try:
		comando = os.system
		comando('pip3 install urllib')
		print('[!] Tentando Instalar as Dependencias')
	except:
		if IOError:	
			sys.exit("[!] Please install the urllib library: pip3 install urllib")	
		
		else:  
			sleep(10)   
			comando('python3 server.py')	
			


app = Flask(__name__)
api = Api(app)


class API(Resource):
	"""  def get(self):
		conn = db_connect.connect() # connect to database
		query = conn.execute("select * from employees") # This line performs query and returns json result
		return {'employees': [i[0] for i in query.cursor.fetchall()]} # Fetches first column that is Employee ID """

	def post(self):
		resp = []
		print(request.json)
	
		return{ 
			"result":"A requisição de envio foi encaminhada para processamento com sucesso. Você poderá acompanhar o status pelos relatórios."
		}
	   
		



api.add_resource(API, '/sms_mock') # Route_1



if __name__ == '__main__':
	app.run()

