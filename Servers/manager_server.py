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
from Class import cpf
from Class.Relatorios import Relatorios as log
from startup import Startup
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import urllib.request
			


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
		if(service == 'all'):
			pass
		elif(service == 'sdu'):
			pass
		elif(service == 'svc'):
			pass
		elif(service == 'sms'):
			pass
		elif(service == 'startup'):
			pass

	def sms(self, parameter_list):
		raise NotImplementedError
	def sdu(self, parameter_list):
		raise NotImplementedError
	def svc(self, parameter_list):
		raise NotImplementedError
	def startup(self, parameter_list):
		raise NotImplementedError


api.add_resource(Command, '/services/') # Route_1



if __name__ == '__main__':
	app.run()

