#!/usr/bin/python3
# coding: utf-8
import sys
import os
from datetime import datetime
import json
import requests
import random
from utils import funcoes
from datetime import timedelta  

class MercadoPago(object):
    def __init__(self, M):
		try:
			self.Manager
		except NameError:
			self.Manager 			= M
			self.database 			= self.Manager.database
			self.Logfile			= M.Controle.logs.MercadoPago_log

	def transacao(self, data):
		body = json.dumps(data).encode('utf8')
		url = "{}access_token={}".format(self.Manager.MP_info['url'],self.Manager.MP_info['api_key'])
		res = requests.post(url=url, data=body)
		self.Logs({'body':body},res)
		status = res.status_code
		response = {
			'status_code' :status,
			'body':json.loads(res)
		}
		return response
	
	def boleto(self,carrinho):
		boleto = {
				"transaction_amount": float(carrinho['valorBoleto']),
				"description": "Eis aqui uma nova oportunidade de Concluir sua Compra! MEGA SORTE",
				"payment_method_id": "bolbradesco",
				"payer": {
					"email": carrinho['email'],
					"first_name": carrinho['nome'],
					"last_name": carrinho['sobrenome'],
					"identification": {
						"type": "CPF",
						"number": carrinho['CPFCNPJ']
					},
					"address": {
						"zip_code": carrinho['CEP'],
						"street_name": carrinho['Endereco'],
						"street_number": carrinho['Numero'],
						"neighborhood": carrinho['Bairro'],
						"city": carrinho['Cidade'],
						"federal_unit": carrinho['SgUF']
					}
				}  
		}
		
		self.Manager.MP_info['boletos_gerados'] += 1
		boleto = json.dumps(boleto).encode('utf8')
		
		
		transacao = self.transacao(boleto)
		
		if transacao['status'] > 204 or transacao['status'] < 200:
			return False
		else:
			boleto_mp = {
				"id_cliente"		 	: carrinho["user_id"],
				"gateway_payment_id" 	: transacao['body']["id"],
				"valor"			  		: boleto_mp['body']['transaction_amount'],
				"vencimento"		 	: transacao['body']['date_of_expiration'].split("T")[0]
				"nosso_numero"	   		: transacao['body']['transaction_details']['payment_method_reference_id'],
				"linha_digitavel"		: transacao['body']['barcode']['content'],
				"link_mp"				: transacao['body']['transaction_details']['external_resource_url'],
				"id_status"				: 0 
			}
			
			self.Manager.MP_info['boletos_gerados'] += 1
			query = "INSERT INTO %s (%s) VALUES(%s)" % ('boleto_mp', ",".join(boleto_mp.keys()), ",".join(boleto_mp.values()))
			self.database.execute("W",query,commit=True)
			return boleto_mp
			
			# retorna dados do boleto 

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
