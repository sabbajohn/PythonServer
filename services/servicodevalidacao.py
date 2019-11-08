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
from utils.db import DB
from utils import CPF as cpf
import asyncio
import aiohttp
from aiofile import AIOFile, LineReader, Writer


class servicoDeValidacao(object):

	

	async def viaCEP(self,CEP):

		url = "https://viacep.com.br/ws/{0}/json".format(CEP)
		async with aiohttp.ClientSession() as s:
			async with s.get(url) as r:
				endereco = await r.read()
				endereco =json.loads(endereco)
				self.contador_ViaCep = self.contador_ViaCep + 1
				return endereco


	async def api_validation_request(self,session, url,index):
		async with session.get(url) as response:
			response = await response.read()
			response =json.loads(response)
			response['CPF'] = url[49:60]
			response['index'] = index
			if ((result[index][4] == "" or result[index][4] == None) and (result[index][5] == "" or  result[index][5] == None)) and  (result[index][6] !="" and  result[index][6] !=None):
				response['viaCep'] = True
				response['CEP'] =  result[index][6]
			else:
				response['viaCep'] = False
			""" print(response_fix) """
			if len(response)>0:
				self.contador_hd = self.contador_hd+1 
				await self.query_generator(response)
			
			else:
				pass


	async def failsafe_api_validation_request(self,params):
		
			
	
		self.contador_failsafe = self.contador_failsafe+1
		log = logging.getLogger('failsafe_api_validation_request')
		log.info('Realizando requisição à API soawebservices')
		
		url = "http://www.soawebservices.com.br/restservices/producao/cdc/pessoafisicaestendida.ashx"
		data={
		'Credenciais': {
			'Email': 'ti@bwabrasil.com.br',
			'Senha': 'prucdNTE'
		},
		"Documento": str(params['CPF'])
		}
			

		body = json.dumps(data).encode('utf8')
		async with aiohttp.ClientSession() as s:
			async with s.post(url, data=body) as r:

				""" req =  request.Request(url, data=params,headers={'content-type': 'application/json'} ) # this will make the method "POST"
				response = request.urlopen(req) """
			
				response =  await r.read()
				response=json.loads(response)
				response['failsafe'] = True
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

						with open("/home/"+USER+"/PythonServer/responses/response.json","a+") as f: #Analizar Resposatas e Gerar Querys 
							for item in failsafe:
								agora = datetime.datetime.now()
								f.write("{0}:{1}\n".format(agora ,item))
						with open("/home/"+USER+"/PythonServer/queries/query.txt","a+") as f:
							for item in failsafe:
								if item['viaCep'] == True:
									endereco =  await viaCEP(item["CEP"])
									try:
										err = endereco['erro']
									except:
				
										if item['Status'] == True:
											item['DataNascimento'] = datetime.datetime.strptime(item['DataNascimento'], "%d/%m/%Y").strftime("%Y-%m-%d")
											message = '{0} verificado via API em {1}'.format(item['Nome'], datetime.datetime.now())
											f.write("UPDATE cliente SET id_status='1', Nome = '{0}' , motivo ='{1}', DtNascimento='{2}', Cidade = '{4}', SgUF='{5}'  WHERE CPFCNPJ = '{3}';\n".format(item['Nome'],message,item['DataNascimento'], item['Documento'],endereco['localidade'], endereco['uf']))#Gerar query caso o TRUE
										if item['Status'] == False:
											f.write("UPDATE cliente SET id_status='3' , motivo ='{0}', Cidade = '{2}', SgUF='{3}'  WHERE CPFCNPJ = '{1}';\n".format(item['Mensagem'], item['Documento'],endereco['localidade'], endereco['uf']))#Gerar query caso o TRUE
										else:
											pass
									
								else:
									if item['Status'] == True:
										item['DataNascimento'] = datetime.datetime.strptime(item['DataNascimento'], "%d/%m/%Y").strftime("%Y-%m-%d")
										message = '{0} verificado via API em {1}'.format(item['Nome'], datetime.datetime.now())
										f.write("UPDATE cliente SET id_status='1', Nome = '{0}' , motivo ='{1}', DtNascimento='{2}'  WHERE CPFCNPJ = '{3}';\n".format(item['Nome'],message,item['DataNascimento'], item['Documento']))#Gerar query caso o TRUE
									if item['Status'] == False:
										f.write("UPDATE cliente SET id_status='3' , motivo ='{0}'  WHERE CPFCNPJ = '{1}';\n".format(item['Mensagem'], item['Documento']))#Gerar query caso o TRUE
									else:
										pass
				else:
					pass
					
			except:
				pass
					
				
				data.append(resp)
				with open("/home/"+USER+"/PythonServer/responses/response.json","a+") as f: #Analizar Resposatas e Gerar Querys 
					for item2 in data:
						agora = datetime.datetime.now()
						f.write("{0}:{1}\n".format(agora ,item2))
				
				with open("/home/"+USER+"/PythonServer/queries/query.txt","a+") as f:
					for item2 in data:
						try:
							r = item2['result']['numero_de_cpf']
							if r:
								item2['result']['numero_de_cpf'] = item2['result']['numero_de_cpf'].replace(caracteres,'')	
						except :
							pass

						if item2['status']==True:
							if item2['viaCep'] is True:
								endereco = await viaCEP(item2["CEP"])
								try:
									err = endereco['erro']
								except:
									if result[item2['index']][3] == None or result[item2['index']][3] == 'None':

										item2['result']['data_nascimento'] = datetime.datetime.strptime(item2['result']['data_nascimento'], "%d/%m/%Y").strftime("%Y-%m-%d")
										message = '{0} verificado via API em {1}'.format(item2['result']['nome_da_pf'], item2['result']['comprovante_emitido_data'])
										f.write("UPDATE cliente SET id_status='1', Nome = '{0}' , motivo ='{1}', Cidade='{3}', SgUF='{4}',DtNascimento ='{5}'  WHERE CPFCNPJ = '{2}';\n".format(item2['result']['nome_da_pf'],message,item2['result']['numero_de_cpf'],endereco['localidade'], endereco['uf'],item2['result']['data_nascimento']))#Gerar query caso o TRUE
									else:
										item2['result']['data_nascimento'] = datetime.datetime.strptime(item2['data_nascimento'], "%d/%m/%Y").strftime("%Y-%m-%d")
										message = '{0} verificado via API em {1}'.format(item2['result']['nome_da_pf'], item2['result']['comprovante_emitido_data'])
										f.write("UPDATE cliente SET id_status='1', motivo ='{0}', Cidade='{2}', SgUF='{3}',DtNascimento ='{4}'  WHERE CPFCNPJ = '{1}';\n".format(message,item2['result']['numero_de_cpf'],endereco['localidade'], endereco['uf'],item2['result']['data_nascimento']))#Gerar query caso o TRUE
							else:
								if result[item2['index']][3] == None or result[item2['index']][3] == '':
								
									item2['result']['data_nascimento'] = datetime.datetime.strptime(item2['data_nascimento'], "%d/%m/%Y").strftime("%Y-%m-%d")
									message = '{0} verificado via API em {1}'.format(item2['result']['nome_da_pf'], item2['result']['comprovante_emitido_data'])
									f.write("UPDATE cliente SET id_status='1', Nome = '{0}' , motivo ='{1}', DtNascimento ='{3}' WHERE CPFCNPJ = '{2}';\n".format(item2['result']['nome_da_pf'],message,item2['result']['numero_de_cpf'],item2['result']['data_nascimento']))#Gerar query caso o TRUE
								else:
									item2['result']['data_nascimento'] = datetime.datetime.strptime(item2['result']['data_nascimento'], "%d/%m/%Y").strftime("%Y-%m-%d")
									message = '{0} verificado via API em {1}'.format(item2['result']['nome_da_pf'], item2['result']['comprovante_emitido_data'])
									f.write("UPDATE cliente SET id_status='1', motivo ='{0}', DtNascimento ='{2}' WHERE CPFCNPJ = '{1}';\n".format(message,item2['result']['numero_de_cpf'],item2['result']['data_nascimento']))#Gerar query caso o TRUE

						elif item2['status']==False:

							try:
								item2['code']
								if item2['code'] == 1:

									if item2['viaCep'] is True:
										endereco = await viaCEP(item2["CEP"])
										try:
											err = endereco['erro']
										except:
											f.write("UPDATE cliente SET id_status='2', motivo = '{0}', Cidade='{2}', SgUF='{3}' WHERE id = {1};\n".format(item2['message'],item2['id'],endereco['localidade'], endereco['uf']))	
									else:
										f.write("UPDATE cliente SET id_status='2', motivo = '{0}' WHERE id = {1};\n".format(item2['message'],item2['id']))
								elif item2['code'] == 2:
									if item2['viaCep'] is True:
										endereco = await viaCEP(item2["CEP"])
										try:
											err = endereco['erro']
										except:
											f.write("UPDATE cliente SET id_status='2', motivo = '{0}', Cidade='{2}', SgUF='{3}' WHERE id = {1};\n".format(item2['message'],item2['id'],endereco['localidade'], endereco['uf']))	
									else:
										f.write("UPDATE cliente SET id_status='2', motivo = '{0}' WHERE id = {1};\n".format(item2['message'],item2['id']))
								elif item2['code'] == 3:
									if item2['viaCep'] is True:
										endereco = await viaCEP(item2["CEP"])
										try:
											err = endereco['erro']
										except:
											f.write("UPDATE cliente SET id_status='2', motivo = '{0}', Cidade='{2}', SgUF='{3}' WHERE id = {1};\n".format(item2['message'],item2['id'],endereco['localidade'], endereco['uf']))	
									else:
										f.write("UPDATE cliente SET id_status='2', motivo = '{0}' WHERE id = {1};\n".format(item2['message'],item2['id']))
							except:

								if item2['return']=='NOK':
									
									if "CPF Nao Encontrado na Base de Dados Federal." in item2['message'] or  "CPF não existe na base até o momento!" in item2['message']:
										if item2['viaCep'] is True:
											endereco = await viaCEP(item2["CEP"])
											try:
												err = endereco['erro']
											except:
												f.write("UPDATE cliente SET id_status='3', motivo = '{0}', Cidade='{2}', SgUF='{3}' WHERE CPFCNPJ = '{1}';\n".format(item2['message'],item2['CPF'],endereco['localidade'], endereco['uf']))
												
										else:
											f.write("UPDATE cliente SET id_status='3', motivo = '{0}' WHERE CPFCNPJ = '{1}';\n".format(item2['message'],item2['CPF']))
									elif "Data Nascimento invalida." in item2['message']:
										try:
											check = item2['CPF']
										
											if check and (self.result[item2['index']][3] == None or self.result[item2['index']][3] == "" ):
												params={}
												if item2['viaCep']:
												
													params['CPF'] = item2['CPF']
													params['viaCep'] =item2['viaCep']
													params['CEP'] = item2['CEP']
												else:
													params['CPF'] = item2['CPF']
													params['viaCep'] =item2['viaCep']

												await failsafe_api_validation_request(params)
											
											else:
												if item2['viaCep'] is True:
													endereco = await viaCEP(item2["CEP"])
													try:
														err = endereco['erro']
													except:
														f.write("UPDATE cliente SET id_status='2', motivo = '{0}', Cidade='{2}', SgUF='{3}' WHERE CPFCNPJ = '{1}';\n".format(item2['message'],item2['CPF'],endereco['localidade'], endereco['uf']))
												else:
													f.write("UPDATE cliente SET id_status='2', motivo = '{0}' WHERE CPFCNPJ = '{1}';\n".format(item2['message'],item2['CPF']))
												
										except:
											pass
											
								

										#f.write("UPDATE cliente SET id_status='2', motivo = '{0}' WHERE CPFCNPJ = {1};\n".format(item['message'],item['CPF']))
									elif  "Token Inválido ou sem saldo para a consulta." in item['message'] :
										sys.exit(item2['message'])	
							else:
								pass

	async def runner(self,executor):
		index = 0
		log = logging.getLogger('Iniciando Solicitações a API hubdodesenvolvedor ')
		log.info('starting')
		tasks=[]
		log.info('Criando tarefas')
		loop = asyncio.new_event_loop()
		async with aiohttp.ClientSession() as session:
			with concurrent.futures.ThreadPoolExecutor() as pool:
				for i in self.pendentes['pendentes']:
					url = self.pendentes['pendentes'][i]
					task = asyncio.ensure_future(api_validation_request(session, url, i))
					tasks.append(task)
				

				await asyncio.gather(*tasks, return_exceptions=True)
			
				log.info('exiting')

	async def list_generator(self,database):
		self.result, self.contador_dispensadas
		executor = database.getCursor("R")
		
		log = logging.getLogger('list_generator')
		log.info('Buscando registros pendentes na base de dados.')
		executor.execute("SELECT  CPFCNPJ, DtNascimento, id, Nome, Cidade, SgUF,CEP FROM cliente where id_status =0 order by Nome asc ,id desc LIMIT 100")
		self.result = executor.fetchall()
		if len(self.result) > 0:
			log.info('{0} itens serão analisados.'.format(len(self.result)))
		else:
			log.info('Não há itens pendentes no momento!')
			log.info("Encerrando serviço.")
			log.info('#######')
			""" TODO: Sair de forma mais Amigavel sys.exit() é muito grosseiro """
			sys.exit("")

		log.info('Aguarde!')
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
					lista['pendentes'][i]="https://ws.hubdodesenvolvedor.com.br/v2/cpf/?cpf={0}&data={1}&token=63764620RjLiAJcVnv115125088".format(x[0], x[1].strftime("%d/%m/%Y"))
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
					self.contador_dispensadas = self.contador_dispensadas+1 
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
					self.contador_dispensadas = self.contador_dispensadas+1 
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
							self.contador_dispensadas = self.contador_dispensadas+1 
							await self.query_generator(data)
			i = i+1		
		
		return lista 	

	def start(self):
		self.USER = getpass.getuser()
		self.failsafe_tasks=[]
		self.failsafe_cpf = []
		self.responses = []
		self.pendentes_f = []
		self.result=None	
		self.contador_failsafe = 0
		self.contador_hd = 0
		self.contador_dispensadas = 0
		self.contador_ViaCep = 0
		self.database = DB()
		
		logging.basicConfig(
		filename='/home/{0}/PythonServer/logs/servico_de_validacao.log'.format(self.USER),
		filemode='a+',
		level=logging.INFO,
		format='PID %(process)5s %(name)18s: %(message)s',
		#stream=sys.stderr,
 		)
		executor = concurrent.futures.ThreadPoolExecutor(
		max_workers=1,
		)
		self.event_loop = asyncio.new_event_loop()

		start_time = time.time()
		log = logging.getLogger('main')
		log.info('*******')
		log.info('Inicializando serviço de Validação de cadastros...')
		log.info(datetime.datetime.now())
		loop = asyncio.new_event_loop()
		
		pendentes=loop.run_until_complete(self.list_generator(self.database))
		try:
			self.event_loop.run_until_complete(
				self.runner(executor)
			)
		finally:
			self.event_loop.close()

			duration = time.time() - start_time
			log.info("Foram efetuadas {0} requisições à API Soawebservices".format(contador_failsafe))
			log.info("Foram efetuadas {0} requisições à API HubdoDesenvolvedor".format(contador_hd))
			log.info("Foram dispensados {0} registros da validação online por falta de parametros".format(contador_dispensadas))
			log.info("Foram realizadas {0} ao Via Cep".format(contador_ViaCep))
			log.info(f"Total de {len(pendentes['pendentes'])} dados consultados em {duration} seconds")
			log.info("Encerrando serviço.")
			log.info('#######')
			log.info('Inicializando Serviço de atualização da base de dados...')
			sleep(15)
			comando = os.system
			comando("python3 Databaseupdate.py")
			""" INICIAR SERVIÇO DO BANCO DE DADOS.... """
	