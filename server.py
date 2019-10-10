#!/usr/bin/python3
# coding: utf-8
import sys
import os
import time
from time import sleep
import cpf
import json
from json import dumps
from Relatorios import Relatorios as log

if sys.version_info[0] < 3:

    raise Exception("[!]Must be using Python 3, You can install it using: # apt-get install python3")
try:
    from flask import Flask, request, jsonify
except:
    comando = os.system
    comando('pip install flask')
    print('[!] Tentando Instalar as Dependencias')    
    if IOError:    
        sys.exit("[!] Please install the flask library: pip install flask")
    else:
        sleep(7) 
        comando('python3 server.py')

try:
   from flask_restful import Resource, Api
except:
    comando = os.system
    comando('pip install flask_restful')
    print('[!] Tentando Instalar as Dependencias')
    if IOError:    
        sys.exit("[!] Please install the flask_restful library: pip install flask_restful")    
    
    else:  
        sleep(10)   
        comando('python3 server.py')    
        
try:
  import urllib.request
except:
    comando = os.system
    comando('pip install urllib')
    print('[!] Tentando Instalar as Dependencias')
    if IOError:    
        sys.exit("[!] Please install the urllib library: pip install urllib")    
    
    else:  
        sleep(10)   
        comando('python3 server.py')    
        




#TODO: Deverá ser migrado para uma aplicação de produção como uWSGi
#TODO: É preciso implementar mecanismos de autenticação
class Clientes(Resource):
    
    def post(self):
       
       
        resp = []
        print(request.json)
        Nome = request.json['Nome']
        CPFCNPJ= request.json['CPFCNPJ']
        Dtnascimento= request.json['Dtnascimento']
        if CPFCNPJ!= None and Dtnascimento !=None:
            if len(CPFCNPJ) > 11:
                checa_cpfcnpj = cpf.isCnpjValid(CPFCNPJ)
            else:
                checa_cpfcnpj = cpf.isCpfValid(CPFCNPJ)

            if checa_cpfcnpj==True:
                contents = urllib.request.urlopen("https://ws.hubdodesenvolvedor.com.br/v2/cpf/?cpf={0}&data={1}&token=63764620RjLiAJcVnv115125088".format(CPFCNPJ,Dtnascimento)).read()
               
                resp.append(json.loads(contents)) 
                log.responses(resp)
                log.query_generator(resp)
                return {'status':'success','message':'Cliente inserido na fila para validação de dados'}
            else:
                data = {}
                data['status'] = False
                data['id'] = CPFCNPJ
                data['code'] = 1
                data['message'] ="Cliente não foi validado pois o CPF/CNPJ: {0} esta incorreto ".format(CPFCNPJ)
               
                resp.append(data) 
                log.responses(resp)
                log.query_generator(resp)
                return {'status':'erro','message':"Cliente não foi validado pois o CPF/CNPJ: {0} esta incorreto ".format(CPFCNPJ)}
        else:
            if CPFCNPJ== None:
                data = {}
                data['status'] = False
                data['code'] = 2
                data['message'] ='Cliente  não foi validado pois o CPF/CNPJ esta em branco'
                
                resp.append(data) 
                log.responses(resp)
                return {'status':'erro','message':'Cliente  não foi validado pois o CPF/CNPJ esta em branco'}
        return {'status':'erro','message':'bad_request'}        
                
           
     
        





class ApiSetting(object):
    def __init__(self):
        
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(Clientes, '/fila') # Route_1

        self.runner(self.app)
    def runner(self, app):
        app.run(port=4444)
if __name__ == '__main__':
    test= ApiSetting()     
