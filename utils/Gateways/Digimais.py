#!/usr/bin/python3
# coding: utf-8
import sys
import os
import datetime
from datetime import date
import json
import requests
import random
from utils import funcoes

class Digimais(object):
	
	def __init__(self, M):
		try:
			self.Manager
		except NameError:
			self.Manager = M
			self.Logfile = M.Controle.logs.Digimais_log
		self.url				= self.Manager.Digimais_info['url']
		self.token				= self.Manager.Digimais_info['token']
		self.gateway_uuid		= self.Manager.Digimais_info['gateway_id']
		self.cardTypeUUID 		= self.Manager.Digimais_info['cardtype']
		self.resquester_id		= self.Manager.Digimais_info['requesterId']
		
		self.boletos_gerados 	= self.Manager.Digimais_info['boletos_gerados']

	def	tranascoes(self,type,data):
		unique_id			= random.randrange(0, 999999999)
		api_url = {
			"incluir_cliente"		: "/acquire/cardHolder/add",
			"salvar_cartao"			: "/acquire/cardManager/add",
			"compra_direta"			: "/acquire/card/authorize",
			"compra_cartao_salvo"	: "/acquire/card/authorize",
			"remover_cartao"		: "/acquire/cardManager/remove",
			"gerar_boleto"			: "/acquire/invoice/create"
		}
		
		default_headers = {
			"Content-Type: application/json", 
			"requester-id: {}".format(self.resquester_id),
			"requester-token: {}".format(self.token),
			"unique-trx-id: {}".format(unique_id)
		}
		res = requests.post(url=self.url+api_url[type], data=body, headers=default_headers)
		self.Logs({'headers':default_headers,'body':body},res)
		response = {
			'status_code': res.status_code,
			'body':json.loads(res.text)
		}
		
		return response
	
	def dados(self, type, compra, form, cliente):
		
		if 'incluir_cliente' in type:
			data = {
				"cardHolder" : {
					"entity" : {
						"name"				 	: cliente["Nome"],
						"phoneCelular"		 	: funcoes.soNumero(cliente["Ceular"]),
						"email"				 	: cliente["Email"],
						"erpUniqueId"		 	: cliente["id"],
						"vatNumber"			 	: funcoes.soNumero(cliente["CPFCNPJ"]),
						"identificationTypeId" :1
					}
				}
				
				
			}
		else:
			data = {}
		
		if len(data)>0:
			return data
		else:
			return False
		
	def Logs(self, request, response):
			log = {
				'datetime' str(datetime.datetime.now())
				'request': request,
				'response':{
					'status_code':response.status_code,
					'body':json.loads(response.text)
				}
			}
			with open(self.Logfile,'a+') as f:
				f.write(json.dumps(log)+'\n')
				f.close()
			return

