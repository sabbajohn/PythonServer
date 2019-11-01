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
from Relatorios import Relatorios as log

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
			"Documento": "00980556236",
			"Nome": "ISSO È UM TESTE",
			"NomeMae": "",
			"DataNascimento": "04/04/1996",
			"Sexo": "Masculino",
			"DataConsultaRFB": "0001-01-01T00:00:00",
			"Enderecos": [],
			"Telefones": [
			{
				"TipoTelefone": 1,
				"Numero": "91983370603",
				"DataAtualizacao": "2019-10-31T10:59:06.7379939-03:00"
			}
			],
		  "Emails": [
			{
			  "Email": "victorsabba@hotmail.com"
			}
		  ],
		  "Participacoes": [],
		  "RendaPresumida": "0",
		  "Mensagem": "Transacao teste realizada com sucesso!",
		  "Status": True,
		  "Transacao": {
			"Status": True,
			"CodigoStatus": "G000M001",
			"CodigoStatusDescricao": "Transacao Teste realizada com sucesso"
		  }
		}
	   
		








api.add_resource(API, '/restservices/producao/cdc/pessoafisicaestendida') # Route_1



if __name__ == '__main__':
	app.run()

