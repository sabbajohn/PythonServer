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
import requests
class recuperacaoDeCarrinhos(object):
	def __init__(self, M):
		
		self.Manager 			= M
		self.database 			= self.Manager.database
		self.mandrill_client 	= None
		

	def start(self, stop):
	
		try:
			message = []
			message.append( "Inicializando Servico de Recuperação de Carrinhos")
			self.feedback(metodo="start", status =-1, message = message, erro = False )
			message = None
			if stop():
				return
			
			self.db_monitor_src()
			self.recCarrinho2()
			self.Manager.SRC_info['last_run'] = str(self.Manager.Agenda['SRC'].last_run)
			self.Manager.update_info()
			time.sleep(1)
			return
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
		return
		

		

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

	def db_monitor_src(self):
		message = []
		message.append( "Inicializando o Monitoramento do Banco de Dados")
		self.feedback(metodo="Monitor", status =5, message = message, erro = False )
		message = None
		escreveu = False
	
		
			
		try:
			result = None
			
			
			result = self.database.execute("R",self.Manager.SRC_info['query'][0])
		
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
			vlbilhete = format(x[2], '.2f').replace(".",",")
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

	def recCarrinho2(self,*args, **kwargst):
		message = []
		message.append( "Inicializando o Recuperação de Carrinhos II")
		self.feedback(metodo="recCarrinho2", status =5, message = message, erro = False )
		message = None
		escreveu = False
	
		try:
			query = self.Manager.SRC_info['query'][1]
			# Se não estiver definida sai da função
		except:
			pass 
		
		try:
			carrinhos = None
			carrinhos = self.database.execute("R",self.Manager.SRC_info['query'][1])

			if len(carrinhos)>0:
			
				if(escreveu == True):
					message = []
					message.append( "Novos carrinhos encontrados!")
					self.feedback(metodo="recCarrinho2", status =5, message = message, erro = False )
					message = None

				message = []
				message.append( "{0} Carrinhos a serem Resgatados!".format(len(carrinhos)))
				self.feedback(metodo="recCarrinho2", status =5, message = message, erro = False )
				message = None
				emails = []
				message = []
				message.append('Gerando Boletos via MP')
				self.feedback(metodo="recCarrinho2", status =5, message = message )
				message = None
				
				for i, carrinho in enumerate(carrinhos):
					carrinho = list(carrinho)
					carrinhos[i] = list(carrinhos[i])
					nome = carrinho[2].split(" ")
					if not nome[len(nome)-1] == "":
						sobrenome = nome[len(nome)-1]
					else:
						sobrenome = nome[len(nome)-2]
					nome = nome[0]
					total = float(carrinho[11]*carrinho[16])
					if total < 10:	
						valorBoleto = 10
					else:
						valorBoleto = total
						valorBoleto = format(valorBoleto, '.2f')

					data= {
						"transaction_amount": float(valorBoleto),
						"description": "Eis aqui uma nova oportunidade de Concluir sua Compra! MEGA SORTE",
						"payment_method_id": "bolbradesco",
						"payer": {
							"email": carrinho[3],
							"first_name": nome,
							"last_name": sobrenome,
							"identification": {
								"type": "CPF",
								"number": carrinho[4]
							},
							"address": {
								"zip_code": carrinho[10],
								"street_name": carrinho[5],
								"street_number": carrinho[6],
								"neighborhood": carrinho[7],
								"city": carrinho[8],
								"federal_unit": carrinho[9]
							}
						}  
					}
					carrinhos[i] = self.geraBoleto(data, carrinho)
				email = self.emailParams2(carrinhos)
				self.send2(email)
				return 
		except Exception as e:
			message = []
			message.append( "{0} ".format(len(e)))
			self.feedback(metodo="recCarrinho2", status =2, message = message, erro = False )
			message = None

	def geraBoleto(self,data,carrinho):
		
		
		self.Manager.MP_info['boletos_gerados'] += 1
		body = json.dumps(data).encode('utf8')
		url = "{}access_token={}".format(self.Manager.MP_info['url'],self.Manager.MP_info['api_key'])
		
		response = requests.post(url=url, data=body)
		status = response.status_code
		#response =   r.read()
		response=json.loads(response.text)
		if status > 204 or status < 200:
				message = []
				message.append( "Não foi possivel gerar Boleto. Status {}".format(status))
				self.feedback(metodo="Gera Boleto", status =5, message = message, erro = False )
				message = None
		else:
			pass
			self.Manager.MP_info['boletos_gerados'] += 1
			# Registra boleto no banco de Dados
			vencimento = response['date_of_expiration'].split("T")[0]
			query = "INSERT INTO `megasorte`.`boleto_mp` (`gateway_payment_id`, `id_cliente`, `valor`, `vencimento`, `nosso_numero`, `linha_digitavel`, `link_mp`, `id_status`) VALUES ({0}, {1}, {2}, '{3}', '{4}', '{5}', '{6}', 0)".format(response['id'],carrinho[1], response['transaction_amount'],vencimento,response['transaction_details']['payment_method_reference_id'],response['barcode']['content'],response['transaction_details']['external_resource_url'])
			self.database.execute("W",query,commit=True)
			self.googleLog(carrinho, response)
			carrinho.append(response['barcode']['content'])
			carrinho.append(response['transaction_details']['external_resource_url'])
			return carrinho
			# retorna dados do boleto 
	
	def emailParams2(self, result):
		cont = 0
		to = []
		merge_vars = []
		keys_to = [ "email","name","VlBilhete"]
		template_content =  [{'content': 'example content', 'name': 'example name'}]# faço nem ideia do que seja isso
		global_merge_vars=  [{'content':  self.Manager.LINK_info['link_site'], 'name': 'link_site'},{'content': self.Manager.LINK_info['contact_mail'], 'name': 'CONTACT_MAIL'},{'content':  self.Manager.LINK_info['link_de_compra'], 'name': 'link_de_compra'}]
		for x in result:
			nome = x[2].split(" ",1)
			valor = float(x[16])*float(x[11])
			valor = format(valor, '.2f').replace(".",",")
			vlbilhete = format(x[11], '.2f').replace(".",",")
			merge_vars.append({'rcpt':x[3],'vars': [{'content': nome[0], 'name':'Nome'},{'content':vlbilhete, 'name':'VlBilhete'},{'content':x[17],'name':'linhaDigitavel'},{'content':x[18],'name':'link_boleto'},{'content':valor,'name':'Valor'}]})
			#É aqui que vou passar raiva, nem lembro o que é isso
			values_to = []
			values_to.append(x[3])
			values_to.append(x[2])
			values_to.append(x[11])

			to.append(dict(zip(keys_to, values_to)))
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
	
	def send2(self, p):
		
		if(self.checkAPI()):
			try:
				result = self.mandrill_client.messages.send_template(template_name='carrinhos-recuperados-adv', template_content=p['template_content'], message=p['message'], ip_pool='Main Pool')
				if 'queued' in result[0]["status"] or 'sent' in result[0]["status"] :
					self.Manager.MANDRILL_info['enviados'] += p['cont'] 
					
						
					
					messages = []
					messages.append("{0} email's foram enviados".format(p['cont'] ))
					self.feedback(metodo="send2", status =5, message = messages, erro = True, comments = "Email's de recuperação de carrinho(ADV)" )
					messages = None
					
					return True
			except mandrill.Error as e:
				
				
				messages = []
				messages.append( type(e))
				messages.append(e)
				self.feedback(metodo="send2", status =1, message = messages, erro = True, comments = "Provavelmente algum erro no mandrill" )
				messages = None
				
				return False
	
			except Exception as e:
				messages = []
				messages.append( type(e))
				messages.append(e)
				self.feedback(metodo="send2", status =1, message = messages, erro = True)
				messages = None
				return False
		else:
				messages = []
				messages.append( "Não foi Possivel validara a Chave API")
				self.feedback(metodo="send", status =1, message = messages, erro = True, comments = "Chave Mandrill" )
				messages = None
				return False

	def googleLog(self, carrinho, response):
		weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
		today = datetime.datetime.now().weekday()
		weekday = weekDays[today]
		log = {
				"env"  : "production",
				"fn"   : "SRC-II",
				"type" : "BOLETO-SRC", 
				"cliente":{
					"sexo":carrinho[13],
					"cidade":carrinho[8],
					"uf":carrinho[9],
					"nascimento":str(carrinho[14])
				},
				"payment":{
					"payment_method_id":"BOLETO-SRC",
					"status":"approved",
					"transaction_amount":response['transaction_amount'],
					"weekday":weekday,
					
				},
				
			}
		with open("/tmp/megasorte-venda.log","a+") as f:
			l = json.dumps(log)
			f.write(l)
			f.write('\n')
		f.close
		return

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

	
	