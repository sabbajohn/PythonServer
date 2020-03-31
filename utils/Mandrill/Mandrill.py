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
from time import sleep
from utils import funcoes

class Mandrill(object):
	def __init__(self, M):
		
		self.Manager 			= M
		self.database 			= self.Manager.database
		self.mandrill_client 	= None
		

	def checkAPI(self):
		if self.mandrill_client is None:
			try:
				self.mandrill_client = mandrill.Mandrill(self.Manager.MANDRILL_info['api_key'])
				return True
			except Exception as e:
				message = []
				message.append(type(e))
				message.append(e)
				self.feedback(metodo="Monitor", status =2, message = message, erro = True )
				message = None
				
		else:
			try:
				valida= self.mandrill_client.users.ping()
				if "PONG" in valida:
					return True
			except:
				try:
					self.mandrill_client = mandrill.Mandrill(self.Manager.MANDRILL_info['api_key'])
					return True
				except Exception as e :
					message = []
					message.append(type(e))
					message.append(e)
					self.feedback(metodo="Monitor", status =2, message = message, erro = True )
					message = None
					return False

	def Params(self, data):
		cont = 0
		to = []
		merge_vars = []
		keys_to = [ "email","name","VlBilhete"]
		template_content =  [{'content': 'example content', 'name': 'example name'}]# faço nem ideia do que seja isso
		global_merge_vars=  [{'content':  self.Manager.LINK_info['link_site'], 'name': 'link_site'},{'content': self.Manager.LINK_info['contact_mail'], 'name': 'CONTACT_MAIL'},{'content': self.Manager.LINK_info['link_de_compra'], 'name': 'link_de_compra'}]
		for x in data:
			
			
			vlbilhete = funcoes.formataValor(x['vlBilhete'])
			
			if 'boleto' in x.keys():
				valor = funcoes.formataNumero(x['boleto']['valor'])
				merge_vars.append({'rcpt':x[email],'vars': [{'content': x['nome'], 'name':'Nome'},{'content':vlbilhete, 'name':'VlBilhete'},{'content':x['boleto']['linha_digitavel'],'name':'linhaDigitavel'},{'content':x['boleto']['url'],'name':'link_boleto'},{'content':valor,'name':'Valor'}]})
			else:
				merge_vars.append({'rcpt':x['email'],'vars': [{'content': x['nome'], 'name':'Nome'},{'content':vlbilhete, 'name':'VlBilhete'}]})
			
			to.append(dict(zip(keys_to, [x['email'],x['nome'],x['vlBilhete']])))
			cont +=1

		
		message = {
			'global_merge_vars':global_merge_vars,
			'to': to,
			'merge_vars':merge_vars,
			'track_clicks': True,
			'track_opens': True
			
			
		}
		return {
			"template_content":template_content,
			"message":message,
			"cont":cont
		}
  
	def send(self, type, data):
		lista_de_envio = None
		
		lista_de_envio = self.Params(data)
		if(self.checkAPI()):
			try:
				result = self.mandrill_client.messages.send_template(template_name='carrinhos-recuperados', template_content=lista_de_envio['template_content'], message=lista_de_envio['message'], ip_pool='Main Pool')
				if 'queued' in result[0]["status"] or 'sent' in result[0]["status"] :
					self.Manager.MANDRILL_info['enviados'] += lista_de_envio['cont'] 
					
						
					
					messages = []
					messages.append("{0} email's foram enviados".format(p['cont'] ))
					self.feedback(metodo="send", status =5, message = messages, erro = True, comments = "Email's de recuperação de carrinho" )
					messages = None
					
					return True
			except mandrill.Error as e:
				
				
				messages = []
				messages.append( type(e))
				messages.append(e)
				self.feedback(metodo="send", status =1, message = messages, erro = True, comments = "Provavelmente algum erro no mandrill" )
				messages = None
				
				return False
	
			except Exception as e:
				messages = []
				messages.append( type(e))
				messages.append(e)
				self.feedback(metodo="send", status =1, message = messages, erro = True)
				messages = None
				return False
		else:
				messages = []
				messages.append( "Não foi Possivel validar a Chave API")
				self.feedback(metodo="send", status =1, message = messages, erro = True, comments = "Chave Mandrill" )
				messages = None
				return False

