#!/usr/bin/python3
# coding: utf-8
import sys
import os
import logging
import time
from datetime import date
import json
import threading
from  urllib import request, parse
from time import sleep
import datetime
import concurrent.futures
import asyncio.coroutines
import getpass
from utils import CPF as cpf
import asyncio
import aiohttp
from aiofile import AIOFile, LineReader, Writer
import ctypes 

#from Manager import Manager


class servicoDeValidacao(object):

	def __init__(self, M):
	
		self.failsafe_tasks=[]
		self.failsafe_cpf = []
		self.responses = []
		self.pendentes_f = []
		self.result=[]	
		self.Manager = M
		self.database = self.Manager.database
		self.contador_failsafe = self.Manager.SOA_info['consultas']
		self.contador_hd =self.Manager.HUBD_info['consultas']
		self.contador_dispensadas = 0
		self.contador_ViaCep = self.Manager.VIACEP_info['consultas']

	def start(self):
		
		self.Manager.SVC_info['next_run'] = self.Manager.Agenda["SVC"].next_run
		self.feedback(metodo="start",status=-1,message ='Inicializando serviço de Validação de cadastros...')
		executor = concurrent.futures.ThreadPoolExecutor(
			max_workers=1,
			)
		self.event_loop = asyncio.new_event_loop()
		start_time = time.time()
		loop = asyncio.new_event_loop()
		
		self.pendentes=loop.run_until_complete(self.list_generator(self.database))
		if not len(self.pendentes)>0:
			message = []
			message.append("Finalizando graciosamente")
			self.feedback(metodo="start",status=0,message = message)
			message = None
			return 
		try:
			self.event_loop.run_until_complete(
				self.runner(executor)
			)
		finally:
			self.event_loop.close()

			duration = time.time() - start_time
			
			
			message = []
			message.append("Foram efetuadas {0} requisições à API Soawebservices".format(self.Manager.SOA_info['consultas'] - self.contador_failsafe))
			message.append("Foram efetuadas {0} requisições à API HubdoDesenvolvedor".format(self.Manager.HUBD_info['consultas'] - self.contador_hd))
			message.append("Foram dispensados {0} registros da validação online por falta de parametros".format(self.contador_dispensadas))
			message.append("Foram realizadas {0} ao Via Cep".format(self.Manager.VIACEP_info['consultas'] - self.contador_ViaCep))
			message.append(f"Total de {len(self.pendentes['pendentes'])} dados consultados em {duration} seconds") 
			
			

			message.append("Encerrando serviço.")
			self.feedback(metodo="start",status=0,message = message)
			message = None
			sleep(5)
			message = []
			message.append("Inicializaremos a Atualização do Banco em breve.")
			self.feedback(metodo="start",status=0,message = message)
			message = None
			if (not self.Manager.Jobs['SDU'].isAlive()):
				
				self.Manager.SDU_info["init_time"]= datetime.datetime.now()
				self.Manager.SDU_info["next_run"]=self.Manager.Agenda['SVC'].next_run
				self.Manager.Jobs['SDU'].start()
				self.Manager.Jobs['SDU'].join()
				self.Manager.Jobs['SDU'] = threading.Thread(target=self.Manager.DataUpdate.start, name="SDU")
			self.Manager.SDU_info['last_run'] = datetime.datetime.now()
			self.Manager.SVC_info['last_run'] = self.Manager.Agenda["SVC"].last_run
			self.failsafe_tasks=[]
			self.failsafe_cpf = []
			self.responses = []
			self.pendentes_f = []
			self.result=[]	
			
			self.contador_failsafe = self.Manager.SOA_info['consultas']
			self.contador_hd =self.Manager.HUBD_info['consultas']
			self.contador_dispensadas = 0
			self.contador_ViaCep = self.Manager.VIACEP_info['consultas']
			self.Manager.update_info()
			
			time.sleep(1)
			return


	async def list_generator(self,database):
		self.result, self.contador_dispensadas
		message = []
		message.append("Buscando registros pendentes na base de dados. Aguarde!")
		self.feedback(metodo ='list_generator', status =5, message=message)
		message = None
		for query in self.Manager.SVC_info['query']:
			try:
				self.result=list(set().union(self.result,database.execute("R", query))) 
				
			except Exception as e:
				message = []
				message.append(type(e))
				message.append(e)
				self.feedback(metodo ='list_generator', status =3, message=message)
				message = None
				
		if len(self.result) > 0:
			message = []
			message.append('{0} itens serão analisados.'.format(len(self.result)))
			self.feedback(metodo ='list_generator', status =5, message=message)
			message = None
		else:
			message = []
			message.append('Não há itens pendentes no momento!')
			message.append("Encerrando serviço.")
			self.feedback(metodo ='list_generator', status =0, message=message)
			message = None
			return []
		lista = {}
		lista['pendentes']={}
		i = 0
		for x in self.result:
			
			if x[0]!= None and x[1]!=None:

				if len(x[0]) > 11:
					checa_cpfcnpj = cpf.isCnpjValid(x[0])
				else:
					checa_cpfcnpj = cpf.isCpfValid(x[0])

				if checa_cpfcnpj==True:
					lista['pendentes'][i]="https://ws.hubdodesenvolvedor.com.br/v2/cpf/?cpf={0}&data={1}&token={2}".format(x[0], x[1].strftime("%d/%m/%Y"), self.Manager.HUBD_info['api_key'])
				else:
					
					data = {}
					data['status'] = False
					data['id'] = x[2]
					data['code'] = 1
					data['message'] ="Cliente {0} não foi validado pois o CPF/CNPJ: {1} está incorreto ".format(x[2],x[0])
					if ((x[4] == "" or x[4] == None) and (x[5] == "" or x[5] == None)) and (x[6] !="" and x[6] !=None):
						data['viaCep']=True
						data['CEP'] = x[6]
					else:
						data['viaCep']=False
					self.contador_dispensadas += 1 
					await self.query_generator(data)
			else:
				if x[0]== None:
					data = {}
					data['status'] = False
					data['id'] = x[2]
					data['code'] = 2
					data['message'] ='Cliente {0} não foi validado pois o CPF/CNPJ está em branco'.format(x[2])
					if ((x[4] == "" or x[4] == None) and (x[5] == "" or x[5] == None)) and (x[6] !="" and x[6] !=None):
						data['viaCep']=True
						data['CEP'] = x[6]
					else:
						data['viaCep']=False
					self.contador_dispensadas += 1
					await self.query_generator(data)
					
				else:	
					if( x[1]== None and (x[3]==None or x[3]=="" )):
						
						params={}
						params['CPF']=x[0]
						if ((x[4] == "" or x[4] == None) and (x[5] == "" or x[5] == None)) and (x[6] !="" and x[6] !=None):
							params['viaCep']=True
							params['CEP'] = x[6]
						else:
							params['viaCep']=False

						await self.failsafe_api_validation_request(params)
					else:	
						if	x[1]== None:
							data = {}
							data['status'] = False
							data['id'] = x[2]
							data['code'] = 3
							data['message'] ="Cliente {0} não foi validado pois o campo data de nascimento está em branco".format(x[2])
							if ((x[4] == "" or x[4] == None) and (x[5] == "" or x[5] == None)) and (x[6] !="" and x[6] !=None):
								data['viaCep']=True
								data['CEP'] = x[6]
							else:
								data['viaCep']=False
							self.contador_dispensadas += 1
							await self.query_generator(data)
			i += 1		
			
		return lista 	

	async def runner(self,executor):
		message = []
		message.append('Iniciando Solicitações a API hubdodesenvolvedor ')
		self.feedback(metodo="Runner",status=5,message = message)
		message = None
		index = 0
		tasks=[]
		loop = asyncio.new_event_loop()
		async with aiohttp.ClientSession() as session:
			with concurrent.futures.ThreadPoolExecutor() as pool:
				for i in self.pendentes['pendentes']:
					url = self.pendentes['pendentes'][i]
					task = asyncio.ensure_future(self.api_validation_request(session, url, i))
					tasks.append(task)
				

				await asyncio.gather(*tasks, return_exceptions=True)
			
				message = []
				message.append('Exiting ')
				self.feedback(metodo="Runner",status=0,message = message)
		return

	async def viaCEP(self,CEP):

		url = "https://viacep.com.br/ws/{0}/json".format(CEP)
		async with aiohttp.ClientSession() as s:
			async with s.get(url) as r:
				endereco = await r.read()
				endereco =json.loads(endereco)
				self.Manager.VIACEP_info['consultas'] += 1
				return endereco

	async def api_validation_request(self,session, url,index):
		async with session.get(url) as response:
			response = await response.read()
			response =json.loads(response)
			response['CPF'] = url[49:60]
			response['index'] = index
			if ((self.result[index][4] == "" or self.result[index][4] == None) and (self.result[index][5] == "" or  self.result[index][5] == None)) and  (self.result[index][6] !="" and  self.result[index][6] !=None):
				response['viaCep'] = True
				response['CEP'] =  self.result[index][6]
			else:
				response['viaCep'] = False
			if len(response)>0:
				self.Manager.HUBD_info['consultas'] += 1 
				await self.query_generator(response)
			
			else:
				pass

	async def failsafe_api_validation_request(self,params):
		message = []
		message.append('[INFO]:Realizando requisição à API soawebservices')
		self.feedback(metodo="failsafe_api_validation_request", status =5, message = message )
		message = None

		self.Manager.SOA_info['consultas'] += 1
		
		
		
		data={
		'Credenciais': {
			'Email':self.Manager.SOA_info['user'],
			'Senha':self.Manager.SOA_info['key']
		},
		"Documento": str(params['CPF'])
		}
			
		body = json.dumps(data).encode('utf8')
		async with aiohttp.ClientSession() as s:
			async with s.post(self.Manager.SOA_info['url'], data=body) as r:

				response =  await r.read()
				response=json.loads(response)
				response['failsafe'] = True
				
				response['index'] = params['index']
				if  params['viaCep']:
					response['viaCep'] = params['viaCep']
					response['CEP'] = params['CEP']
				else:
					response['viaCep'] = params['viaCep']
				if len(response)>0:
					await self.query_generator(response)

	async def query_generator(self,resp):
		self.result
		caracteres = ['.','-']
		data=[]
		failsafe=[]
		if len(resp)>0:
			try:
				r = resp['failsafe']
				if r:
					if(resp['failsafe']==True):
						failsafe.append(resp)

						with open(self.Manager.Files['responses'],"a+") as f: #Analizar Resposatas e Gerar Querys
							for item in failsafe:
								agora = datetime.datetime.now()
								f.write("{0}:{1}\n".format(agora ,item))
						with open(self.Manager.Files['query'],"a+") as f:
							for item in failsafe:
								if item['viaCep'] == True:
									endereco =  await self.viaCEP(item["CEP"])
									try:
										err = endereco['erro']
									except:

										if item['Status'] == True:
											try:


												data_api = time.mktime(datetime.datetime.strptime(item['DataNascimento'], "%d/%m/%Y").timetuple())

												sixteenyearsago  = date.today()
												sixteenyearsago = sixteenyearsago.replace(year =sixteenyearsago.year -16 )
												sixteenyearsago = time.mktime(sixteenyearsago.timetuple())


											except :

												pass
											if data_api < sixteenyearsago: #OU SEJA, MAIOR DE 16 ATUALIZO COM O RESULTADO DA API
												status = 1
												message = '{0} verificado via API em {1}'.format(item['Nome'], datetime.datetime.now())
												item['DataNascimento'] = datetime.datetime.strptime(item['DataNascimento'], "%d/%m/%Y").strftime("%Y-%m-%d")
												f.write("UPDATE cliente SET id_status='{8}', Nome = '{0}' , motivo ='{1}', DtNascimento='{2}', Cidade = '{4}', SgUF='{5}', Endereco= '{6}', Bairro='{7}'   WHERE CPFCNPJ = '{3}';\n".format(item['Nome'],message,item['DataNascimento'], item['Documento'].replace('-','').replace('.',''),endereco['localidade'], endereco['uf'], endereco['logradouro'], endereco['bairro'],status))#Gerar query caso o TRUE
											else:# SE NAO, È MENOR. FINJO QUE NÂO VI
												status = 2
												message = 'Data de Nascimento divergente do informado pela Receita Federal {0}'.format( datetime.datetime.now())
												item['DataNascimento'] = self.result[item['index']][1].strftime("%Y-%m-%d")
												f.write("UPDATE cliente SET id_status='{8}', Nome = '{0}' , motivo ='{1}', DtNascimento='{2}', Cidade = '{4}', SgUF='{5}', Endereco= '{6}', Bairro='{7}'   WHERE CPFCNPJ = '{3}';\n".format(item['Nome'],message,item['DataNascimento'], item['Documento'].replace('-','').replace('.',''),endereco['localidade'], endereco['uf'], endereco['logradouro'], endereco['bairro'],status))#Gerar query caso o TRUE
										if item['Status'] == False:
											f.write("UPDATE cliente SET id_status='3' , motivo ='{0}', Cidade = '{2}', SgUF='{3}', Endereco='{4}', Bairro='{5}'  WHERE CPFCNPJ = '{1}';\n".format(item['Mensagem'], item['Documento'].replace('-','').replace('.',''),endereco['localidade'], endereco['uf'], endereco['logradouro'], endereco['bairro']))#Gerar query caso o TRUE
										else:
											pass
									#TODO ELSE do erro do via cep
								else:
									if item['Status'] == True:

										try:


											d2 = time.mktime(datetime.datetime.strptime(item['DataNascimento'], "%d/%m/%Y").timetuple())

											sixteenyearsago  = date.today()
											sixteenyearsago = sixteenyearsago.replace(year =sixteenyearsago.year -16 )
											sixteenyearsago = time.mktime(sixteenyearsago.timetuple())


										except:
											pass
										if d2 < sixteenyearsago: #OU SEJA, MAIOR DE 16 ATUALIZO COM O RESULTADO DA API
											status = 1
											message = '{0} verificado via API em {1}'.format(item['Nome'], datetime.datetime.now())
											item['DataNascimento'] = datetime.datetime.strptime(item['DataNascimento'], "%d/%m/%Y").strftime("%Y-%m-%d")
										else:# SE NAO, È MENOR. FINJO QUE NÂO VI
											status = 2
											message = 'Data de Nascimento divergente do informado pela Receita Federal {0}'.format( datetime.datetime.now())
											item['DataNascimento'] = self.result[item['index']][1].strftime("%Y-%m-%d")



										f.write("UPDATE cliente SET id_status='1', Nome = '{0}' , motivo ='{1}', DtNascimento='{2}'  WHERE CPFCNPJ = '{3}';\n".format(item['Nome'],message,item['DataNascimento'], item['Documento'].replace('-','').replace('.','')))#Gerar query caso o TRUE
									if item['Status'] == False:
										f.write("UPDATE cliente SET id_status='3' , motivo ='{0}'  WHERE CPFCNPJ = '{1}';\n".format(item['Mensagem'], item['Documento'].replace('-','').replace('.','')))#Gerar query caso o TRUE
									else:
										pass
				else:
					pass

			except:

				data.append(resp)
				with open(self.Manager.Files['responses'],"a+") as f: #Analizar Resposatas e Gerar Querys
					for item2 in data:
						agora = datetime.datetime.now()
						f.write("{0}:{1}\n".format(agora ,item2))

				with open(self.Manager.Files['query'],"a+") as f:
					for item2 in data:
						try:
							r = item2['result']['numero_de_cpf']
							if r:
								item2['result']['numero_de_cpf'] = item2['result']['numero_de_cpf'].replace('.','').replace('-','')
						except :
							pass

						if item2['status']==True:
							if item2['viaCep'] is True:
								endereco = await self.viaCEP(item2["CEP"])
								try:
									err = endereco['erro']
								except:
									if self.result[item2['index']][3] == None or self.result[item2['index']][3] == 'None':

										try:


											d2 = time.mktime(datetime.datetime.strptime(item2['result']['data_nascimento'], "%d/%m/%Y").timetuple())

											sixteenyearsago  = date.today()
											sixteenyearsago = sixteenyearsago.replace(year =sixteenyearsago.year -16 )
											sixteenyearsago = time.mktime(sixteenyearsago.timetuple())


										except:
											pass
										if d2 < sixteenyearsago: #OU SEJA, MAIOR DE 16 ATUALIZO COM O RESULTADO DA API
											status = 1
											message = '{0} verificado via API em {1}'.format(item2['result']['nome_da_pf'], item2['result']['comprovante_emitido_data'])
											item2['result']['data_nascimento'] = datetime.datetime.strptime(item2['result']['data_nascimento'], "%d/%m/%Y").strftime("%Y-%m-%d")
											f.write("UPDATE cliente SET id_status='{8}', Nome = '{0}' , motivo ='{1}', Cidade='{3}', SgUF='{4}',DtNascimento ='{5}', Endereco='{6}', Bairro='{7}'  WHERE CPFCNPJ = '{2}';\n".format(item2['result']['nome_da_pf'],message,item2['result']['numero_de_cpf'],endereco['localidade'], endereco['uf'],item2['result']['data_nascimento'], endereco['logradouro'], endereco['bairro'],status))#Gerar query caso o TRUE
										else:# SE NAO, È MENOR. FINJO QUE NÂO VI
											status = 2
											message = 'Data de Nascimento divergente do informado pela Receita Federal {0}'.format( datetime.datetime.now())
											item2['result']['data_nascimento'] = self.result[item2['index']][1].strftime("%Y-%m-%d")

											f.write("UPDATE cliente SET id_status='{8}', Nome = '{0}' , motivo ='{1}', Cidade='{3}', SgUF='{4}',DtNascimento ='{5}', Endereco='{6}', Bairro='{7}'  WHERE CPFCNPJ = '{2}';\n".format(item2['result']['nome_da_pf'],message,item2['result']['numero_de_cpf'],endereco['localidade'], endereco['uf'],item2['result']['data_nascimento'], endereco['logradouro'], endereco['bairro'],status))#Gerar query caso o TRUE
									else:
										try:


											d2 = time.mktime(datetime.datetime.strptime(item2['result']['data_nascimento'], "%d/%m/%Y").timetuple())

											sixteenyearsago  = date.today()
											sixteenyearsago = sixteenyearsago.replace(year =sixteenyearsago.year -16 )
											sixteenyearsago = time.mktime(sixteenyearsago.timetuple())


										except:
											pass
										if d2 < sixteenyearsago: #OU SEJA, MAIOR DE 16 ATUALIZO COM O RESULTADO DA API
											status = 1
											message = '{0} verificado via API em {1}'.format(item2['result']['nome_da_pf'], item2['result']['comprovante_emitido_data'])
											item2['result']['data_nascimento'] = datetime.datetime.strptime(item2['result']['data_nascimento'], "%d/%m/%Y").strftime("%Y-%m-%d")
											f.write("UPDATE cliente SET id_status='{7}', motivo ='{0}', Cidade='{2}', SgUF='{3}',DtNascimento ='{4}', Endereco='{5}', Bairro='{6}'  WHERE CPFCNPJ = '{1}';\n".format(message,item2['result']['numero_de_cpf'],endereco['localidade'], endereco['uf'],item2['result']['data_nascimento'], endereco['logradouro'],endereco['bairro'], status))#Gerar query caso o TRUE
										else:# SE NAO, È MENOR. FINJO QUE NÂO VI
											status = 2
											message = 'Data de Nascimento divergente do informado pela Receita Federal {0}'.format( datetime.datetime.now())
											item2['result']['data_nascimento'] = self.result[item2['index']][1].strftime("%Y-%m-%d")
											f.write("UPDATE cliente SET id_status='{7}', motivo ='{0}', Cidade='{2}', SgUF='{3}',DtNascimento ='{4}', Endereco='{5}', Bairro='{6}'  WHERE CPFCNPJ = '{1}';\n".format(message,item2['result']['numero_de_cpf'],endereco['localidade'], endereco['uf'],item2['result']['data_nascimento'], endereco['logradouro'],status))#Gerar query caso o TRUE
								#TODO ELSE do erro do via cep
							else:
								if self.result[item2['index']][3] == None or self.result[item2['index']][3] == '':
									try:
										d2 = time.mktime(datetime.datetime.strptime(item2['result']['data_nascimento'], "%d/%m/%Y").timetuple())
										sixteenyearsago  = date.today()
										sixteenyearsago = sixteenyearsago.replace(year =sixteenyearsago.year -16 )
										sixteenyearsago = time.mktime(sixteenyearsago.timetuple())


									except:
										pass
									if d2 < sixteenyearsago: #OU SEJA, MAIOR DE 16 ATUALIZO COM O RESULTADO DA API
										status = 1
										message = '{0} verificado via API em {1}'.format(item2['result']['nome_da_pf'], item2['result']['comprovante_emitido_data'])
										item2['result']['data_nascimento'] = datetime.datetime.strptime(item2['result']['data_nascimento'], "%d/%m/%Y").strftime("%Y-%m-%d")
										f.write("UPDATE cliente SET id_status='{4}', Nome = '{0}' , motivo ='{1}', DtNascimento ='{3}' WHERE CPFCNPJ = '{2}';\n".format(item2['result']['nome_da_pf'],message,item2['result']['numero_de_cpf'],item2['result']['data_nascimento'],status))#Gerar query caso o TRUE
									else:# SE NAO, È MENOR. FINJO QUE NÂO VI
										status = 2
										message = 'Data de Nascimento divergente do informado pela Receita Federal {0}'.format( datetime.datetime.now())
										item2['result']['data_nascimento'] = self.result[item2['index']][1].strftime("%Y-%m-%d")
										f.write("UPDATE cliente SET id_status='{4}', Nome = '{0}' , motivo ='{1}', DtNascimento ='{3}' WHERE CPFCNPJ = '{2}';\n".format(item2['result']['nome_da_pf'],message,item2['result']['numero_de_cpf'],item2['result']['data_nascimento'],status))#Gerar query caso o TRUE
								else:
									try:

											d2 = time.mktime(datetime.datetime.strptime(item2['result']['data_nascimento'], "%d/%m/%Y").timetuple())

											sixteenyearsago  = date.today()
											sixteenyearsago = sixteenyearsago.replace(year =sixteenyearsago.year -16 )
											sixteenyearsago = time.mktime(sixteenyearsago.timetuple())

									except:
										pass
									if d2 < sixteenyearsago: #OU SEJA, MAIOR DE 16 ATUALIZO COM O RESULTADO DA API
										status = 1
										message = '{0} verificado via API em {1}'.format(item2['result']['nome_da_pf'], item2['result']['comprovante_emitido_data'])
										item2['result']['data_nascimento'] = datetime.datetime.strptime(item2['result']['data_nascimento'], "%d/%m/%Y").strftime("%Y-%m-%d")
										f.write("UPDATE cliente SET id_status='{3}', motivo ='{0}', DtNascimento ='{2}' WHERE CPFCNPJ = '{1}';\n".format(message,item2['result']['numero_de_cpf'],item2['result']['data_nascimento'],status))#Gerar query caso o TRUE
									else:# SE NAO, È MENOR. FINJO QUE NÂO VI
										status = 2
										message = 'Data de Nascimento divergente do informado pela Receita Federal {0}'.format( datetime.datetime.now())
										item2['result']['data_nascimento'] = self.result[item2['index']][1].strftime("%Y-%m-%d")
										f.write("UPDATE cliente SET id_status='{3}', motivo ='{0}', DtNascimento ='{2}' WHERE CPFCNPJ = '{1}';\n".format(message,item2['result']['numero_de_cpf'],item2['result']['data_nascimento'],status))#Gerar query caso o TRUE

						elif item2['status']==False:

							try:
								item2['code']
								if item2['code'] == 1:

									if item2['viaCep'] is True:
										endereco = await self.viaCEP(item2["CEP"])
										try:
											err = endereco['erro']
										except:
											f.write("UPDATE cliente SET id_status='2', motivo = '{0}', Cidade='{2}', SgUF='{3}', Endereco='{4}', Bairro='{5}' WHERE id = {1};\n".format(item2['message'],item2['id'],endereco['localidade'], endereco['uf'], endereco['logradouro'], endereco['bairro']))
											#TODO ELSE do erro do via cep
									else:
										f.write("UPDATE cliente SET id_status='2', motivo = '{0}' WHERE id = {1};\n".format(item2['message'],item2['id']))
								elif item2['code'] == 2:
									if item2['viaCep'] is True:
										endereco = await self.viaCEP(item2["CEP"])
										try:
											err = endereco['erro']
										except:
											f.write("UPDATE cliente SET id_status='2', motivo = '{0}', Cidade='{2}', SgUF='{3}', Endereco ='{4}', Bairro='{5}' WHERE id = {1};\n".format(item2['message'],item2['id'],endereco['localidade'], endereco['uf'], endereco['logradouro'], endereco['bairro']))
											#TODO ELSE do erro do via cep
									else:
										f.write("UPDATE cliente SET id_status='2', motivo = '{0}' WHERE id = {1};\n".format(item2['message'],item2['id']))
								elif item2['code'] == 3:
									if item2['viaCep'] is True:
										endereco = await self.viaCEP(item2["CEP"])
										try:
											err = endereco['erro']
										except:
											f.write("UPDATE cliente SET id_status='2', motivo = '{0}', Cidade='{2}', SgUF='{3}', Endereco='{4}', Bairro='{5}' WHERE id = {1};\n".format(item2['message'],item2['id'],endereco['localidade'], endereco['uf'], endereco['logradouro'], endereco['bairro']))
										#TODO ELSE do erro do via cep
									else:
										f.write("UPDATE cliente SET id_status='2', motivo = '{0}' WHERE id = {1};\n".format(item2['message'],item2['id']))
							except:

								if item2['return']=='NOK':

									if "CPF Nao Encontrado na Base de Dados Federal." in item2['message'] or  "CPF não existe na base até o momento!" in item2['message']:
										if item2['viaCep'] is True:
											endereco = await self.viaCEP(item2["CEP"])
											try:
												err = endereco['erro']
											except:
												f.write("UPDATE cliente SET id_status='3', motivo = '{0}', Cidade='{2}', SgUF='{3}', Endereco='{4}', Bairro='{5}' WHERE CPFCNPJ = '{1}';\n".format(item2['message'],item2['CPF'],endereco['localidade'], endereco['uf'], endereco['logradouro'], endereco['bairro']))
												#TODO ELSE do erro do via cep
										else:
											f.write("UPDATE cliente SET id_status='3', motivo = '{0}' WHERE CPFCNPJ = '{1}';\n".format(item2['message'],item2['CPF']))
									elif "Data Nascimento invalida." in item2['message']:
										try:
											check = item2['CPF']

											if check and (self.result[item2['index']][3] == None or self.result[item2['index']][3] == "" ):
												params={}
												if item2['viaCep']:

													params['CPF'] = item2['CPF']
													params['index'] = item2['index']
													params['viaCep'] =item2['viaCep']
													params['CEP'] = item2['CEP']
												else:
													params['CPF'] = item2['CPF']
													params['viaCep'] =item2['viaCep']

												await self.failsafe_api_validation_request(params)

											else:
												if item2['viaCep'] is True:
													endereco = await self.viaCEP(item2["CEP"])
													try:
														err = endereco['erro']
													except:
														f.write("UPDATE cliente SET id_status='2', motivo = '{0}', Cidade='{2}', SgUF='{3}' WHERE CPFCNPJ = '{1}';\n".format(item2['message'],item2['CPF'],endereco['localidade'], endereco['uf']))
														#TODO ELSE do erro do via cep
												else:
													f.write("UPDATE cliente SET id_status='2', motivo = '{0}' WHERE CPFCNPJ = '{1}';\n".format(item2['message'],item2['CPF']))

										except:
											pass



										
									elif  "Token Inválido ou sem saldo para a consulta." in item2['message'] :
										self.svc_api.hubd.consultas -= 1 
										message = []
										message.append('Token Inválido ou sem saldo para a consulta."')
										self.feedback(metodo="Runner",status=1,message = message)
										message = None
										sys.exit(item2['message'])
							else:
								pass

	def get_id(self): 
		
		# returns id of the respective thread 
		if hasattr(self, '_thread_id'): 
			return self._thread_id 
		for id, thread in threading._active.items(): 
			if thread is self: 
				return id

	def raise_exception(self): 
		message = []
		message.append( "Serviço finalizado via Watcher")
		self.feedback(metodo="Watcher", status =5, message = message, erro = False, comments = "Finalizado via Watcher" )
		message = None
		thread_id = self.get_id() 
		res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 
				ctypes.py_object(SystemExit)) 
		if res > 1: 
			ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
			print('Finalizando Serviço')

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
			"class":"servicoDeValidacao",
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
		
		feedback['time'] = str(datetime.datetime.now())
		#with self._lock:
		self.Manager.callback(feedback)
