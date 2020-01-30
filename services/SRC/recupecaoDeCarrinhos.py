#!/usr/bin/python3
# coding: utf-8
import sys
import os
import logging
import time
import datetime
from datetime import date
import json
import getpass
import threading
import mandrill
import configparser	
import asyncio
import schedule
class recuperacaoDeCarrinhos(object):
	def __init__(self, M):
	
		self.Manager 			= M
		self.database 			= self.Manager.database
		self.mandrill_client 	= None
		
		self.src_service 		= self.Manager.getControle('src')
		
		
		

	def start(self, stop):
	
		try:
			message = []
			message.append( "Inicializando Servico de Recuperação de Carrinhos")
			self.feedback(metodo="start", status =-1, message = message, erro = False )
			message = None
			schedule.every().hour.at(":00").do(self.db_monitor)
			self.Manager.SRC_info['nextrun'] = schedule.jobs[0].next_run
			self.Manager.SRC_controle.setControle(self.Manager.SRC_info)
			while True:
				self.Manager.update_info()
				if stop():
					break
				schedule.run_pending()
				self.Manager.SRC_info['lasttimerunning'] = datetime.datetime.now()
				self.Manager.SRC_controle.setControle(self.Manager.SRC_info)
				self.Manager.Controle.writeConfigFile()
				time.sleep(1)
			
		except SystemExit:
			message = []
			message.append( "Serviço finalizado via Watcher")
			self.feedback(metodo="start", status =5, message = message, erro = False, comments = "Finalizado via Watcher" )
			message = None
			sys.exit()
		except Exception as e:
			
			message = []
			message.append( type(e))
			message.append(e)
			self.feedback(metodo="start", status =4, message = message, erro = True, comments = "Algo não panejado" )
			message = None
		
		

		pass

	async def runNow(self):
		message = []
		message.append( "Inicializando Consulta não agendada")
		self.feedback(metodo="Monitor", status =5, message = message, erro = False )
		message = None
		escreveu = False
		try:
				result = None
				
			
				result = self.database.execute("R",self.Manager.SRC_info['query'])
			
				if len(result)>0:
					
					if(escreveu == True):
						message = []
						message.append( "Novos carrinhos encontrados!")
						self.feedback(metodo="Monitor", status =5, message = message, erro = False )
						message = None

					message = []
					message.append( "{0} Carrinhos a serem Resgatados!".format(len(result)))
					self.feedback(metodo="Monitor", status =5, message = message, erro = False )
					message = None
	
					params = self.emailParams(result)
					return self.send(params)
					
					
				else: 
					if(escreveu == False):
						message = []
						message.append( "Nenhum carrinho abandonado no momento!")
						self.feedback(metodo="runNow", status =5, message = message, erro = False, comments ="Nenhum Carrinho!"  )
						message = None
						escreveu= True
						return False
		except Exception as e: 

			message = []
			message.append(type(e))
			message.append(e)

			self.feedback(metodo="Monitor", status =5, message = message, erro = False, comments ="Exceção não tratada "  )
			message = None
			return False

	def db_monitor(self):
		message = []
		message.append( "Inicializando o Monitoramento do Banco de Dados")
		self.feedback(metodo="Monitor", status =5, message = message, erro = False )
		message = None
		escreveu = False
	
		
			
		try:
			result = None
			
		
			result = self.database.execute("R",self.self.Manager.SRC_info['query'])
		
			if len(result)>0:
			
				if(escreveu == True):
					message = []
					message.append( "Novos carrinhos encontrados!")
					self.feedback(metodo="Monitor", status =5, message = message, erro = False )
					message = None

				message = []
				message.append( "{0} Carrinhos a serem Resgatados!".format(len(result)))
				self.feedback(metodo="Monitor", status =5, message = message, erro = False )
				message = None
				params = self.emailParams(result)
				self.send(params)
				return
				
			else: 
				if(escreveu == False):
					message = []
					message.append( "Nenhum carrinho abandonado no momento!")
					self.feedback(metodo="Monitor", status =5, message = message, erro = False, comments ="Tentaremos novamente em Breve! L144"  )
					message = None
					escreveu= True
				
				return
				#time.sleep(self.delay)
		except Exception as e :
			message = []
			message.append(type(e))
			message.append(e)
			self.feedback(metodo="Monitor", status =2, message = message, erro = False, comments ="L154"  )
			message = None
		finally:
			return

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

	def emailParams(self, result):
		cont = 0
		to = []
		merge_vars = []
		keys_to = [ "email","name","VlBilhete"]
		template_content =  [{'content': 'example content', 'name': 'example name'}]# faço nem ideia do que seja isso
		global_merge_vars=  [{'content':  self.Manager.LINK_info['link_site'], 'name': 'link_site'},{'content': self.Manager.LINK_info['contact_mail'], 'name': 'CONTACT_MAIL'},{'content':  self.Manager.LINK_info['link_de_compra'], 'name': 'link_de_compra'}]
		for x in result:
			nome = x[1].split(" ",1)
			vlbilhete = str(x[2]).replace(".",",")
			merge_vars.append({'rcpt':x[0],'vars': [{'content': nome[0], 'name':'Nome'},{'content':vlbilhete, 'name':'VlBilhete'}]})

			to.append(dict(zip(keys_to, x)))
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

	def send(self, p):
		
		if(self.checkAPI()):
			try:
				result = self.mandrill_client.messages.send_template(template_name='carrinhos-recuperados', template_content=p['template_content'], message=p['message'], ip_pool='Main Pool')
				if 'queued' in result[0]["status"] or 'sent' in result[0]["status"] :
					self.Manager.MANDRILL_info['enviados'] += p['cont'] 
					self.MANDRILL_controle.setControle(self.Manager.MANDRILL_info)
						
					except:
						pass
					
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
				messages.append( "Não foi Possivel validara a Chave API")
				self.feedback(metodo="send", status =1, message = messages, erro = True, comments = "Chave Mandrill" )
				messages = None
				return False

	def feedback(self,*args, **kwargst):
		message = kwargst.get('message')
		comments = kwargst.get('comments')
		metodo =kwargst.get('metodo')
		status =kwargst.get('status')
		try:
			erro =kwargst.get('erro')
		except:
			erro = False
		feedback = {
			"class":"recuperacaoDeCarrinhos",
			"metodo":kwargst.get('metodo'),
			"status":kwargst.get('status'),
			"message":[],
			"erro":False,
			"comments":"",
			"time":None
		}
		feedback["metodo"] = metodo
		feedback["status"] = status
		feedback["erro"]=erro
		if feedback['status']== 0:
			for msg in message:
				feedback["message"].append( '[OK]:{0}'.format(msg)) 
			
		elif feedback['status']== 1:
			for msg in message:
				feedback["message"].append('[X]:{0}'.format(msg))
		elif feedback['status']== 2:
			for msg in message:
				feedback["message"].append('[!]:{0}'.format(msg))
		elif feedback['status']== 3:
			for msg in message:
				feedback["message"].append( '[SQL_ERRO]:{0}'.format(msg))
		elif feedback['status']== 4:
			for msg in message:
				feedback["message"].append('[!!!]:{0}'.format(msg))
		elif feedback['status']== 5:
			for msg in message:
				feedback["message"].append('[INFO]:{0}'.format(msg)) 
		
		try: 
			feedback["comments"] = comments
		except:
			feedback["comments"] = ""
		
		feedback['time'] = datetime.datetime.now()
	
		self.Manager.callback(feedback)
