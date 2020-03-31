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

class Digimais(object):
	
	def __init__(self, M):
		try:
			self.Manager
		except NameError:
			self.Manager 			= M
			self.database 			= self.Manager.database
			self.Logfile			= M.Controle.logs.Digimais_log
		self.url				= self.Manager.Digimais_info['url']
		self.token				= self.Manager.Digimais_info['token']
		self.gateway_uuid		= self.Manager.Digimais_info['gateway_id']
		self.cardTypeUUID 		= self.Manager.Digimais_info['cardtype']
		self.resquester_id		= self.Manager.Digimais_info['requesterId']
		
		self.boletos_gerados 	= self.Manager.Digimais_info['boletos_gerados']

	def	tranascao(self,type,data):
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
	
	def boleto(self, carrinho):
		if not carrinho['digimais_id']:
			cardHolder = self.dados("incluir_cliente", false, false, carrinho)
		if cardHolder:
			transacao = self.transacao("incluir_cliente", card_holder)
			if transacao.body['responseCode'] == '0':
				cardHolderUUID = carrinho["digimais_id"] = transacao["cardHolderUUID"]
				cliente_id = carrinho["id"]
				query = 'UPDATE cliente SET digimais_id = "{}" WHERE id = {}'.format(cardHolderUUID, cliente_id)
				self.database.execute("W",query,commit=True)
		else:
			return False
		if self.Manager.Controle.Key.env in ('BETA', 'PROD'):
			callBack ="https://www.megasorte.com/gateway/notifications_digimais"
		else:
			callBack =  "https://webhook.site/28100f89-bb10-4fd3-afd7-8edb0c1c1130"
		boleto = {
			"amount"				 : valor_boleto,
			"invoiceTemplateUUID"	: self.invoiceTemplateUUID,
			"originUUID"			 : carrinho["digimais_id"],
			"transactionUUID"		: self.transactionUUID,
			"destinationUUID"		: self.destinationUUID,
			"dateDue"				: datetime.date(datetime.now()) + timedelta(weeks=5),
			"transactionType"		: 1,
			"callBackInvoiceInfoURL" : callBack
			"softDescriptor"		 : "Eis aqui uma nova oportunidade de Concluir sua Compra! MEGA SORTE"
		}

		transacao = self.tranascao('gerar_boleto', boleto)
		if transacao['body']['responseCode'] == '0':
			boleto_dm = {
			"id_cliente"		 	: carrinho["user_id"],
			"gateway_payment_id" 	: transacao['body']["invoiceUUID"],
			"valor"			  		: valor_boleto,
			"vencimento"		 	: datetime.date(datetime.now()) + timedelta(weeks=5),
			"nosso_numero"	   		: transacao['body']["uniqueInvoiceNumber"],
			"linha_digitavel"		: transacao['body']["barcode"],
			"url"					: transacao['body']["url"],
		}
			query = "INSERT INTO %s (%s) VALUES(%s)" % ('boleto_digimais', ",".join(boleto_dm.keys()), ",".join(boleto_dm.values()))
			self.database('W',query,commit=True)
			return = boleto_dm
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

