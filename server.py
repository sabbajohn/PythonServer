#!/usr/bin/python3
# coding: utf-8
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import urllib.request
import json
from Relatorios import Relatorios as log
import cpf


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
                return {'status':'erro','message':'bad_request'}
        else:
            if CPFCNPJ== None:
                data = {}
                data['status'] = False
                data['code'] = 2
                data['message'] ='Cliente  não foi validado pois o CPF/CNPJ esta em branco'
                
                resp.append(data) 
                log.responses(resp)
                return {'status':'erro','message':'bad_request'}
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
