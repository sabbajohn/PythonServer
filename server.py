#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps





class Clientes(Resource):
    
    def post(self):
        #TODO: Inserir validação ṕor token....
        print(request.json)
        Nome = request.json['Nome']
        CPFCNPJ= request.json['CPFCNPJ']
        Dtnascimento= request.json['Dtnascimento']
        # manda os dados dessa requisição pra uma estrutura de dados
        return {'status':'success','message':'Cliente inserido na fila para validação de dados1'}





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
