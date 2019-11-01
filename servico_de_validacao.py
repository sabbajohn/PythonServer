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



sys.path.insert(1,'/home/objetiva/PythonServer/Class')
import cpf

if sys.version_info[0] < 3:

	raise Exception("[!]Must be using Python 3, You can install it using: # apt-get install python3")
try:
   import asyncio
	
except:
	try:
		comando = os.system
		comando('sudo pip3 install asyncio')
		print('[!] Tentando Instalar as Dependencias')	
	except:
		if IOError:	
			sys.exit("[!] Please install the asyncio library: sudo pip3 install asyncio")
		else:
			sleep(7) 
			comando('python3 servico_de_validacao.py')

try:
   import aiohttp
except:
	try:
		comando = os.system
		comando('sudo pip3 install aiohttp')
		print('[!] Tentando Instalar as Dependencias')
	except:

		if IOError:	
			sys.exit("[!] Please install the aiohttp library: sudo pip3 install aiohttp")	
		
		else:  
			sleep(10)   
			comando('python3 servico_de_validacao.py')	
			
try:
   import mysql.connector
except:
	try:
		comando = os.system
		comando('sudo pip3 install mysql')
		print('[!] Tentando Instalar as Dependencias')
	except:
		if IOError:	
			sys.exit("[!] Please install the mysql library: sudo pip3 install mysql")	
		
		else:  
			sleep(10)   
			comando('python3 servico_de_validacao.py')	
			

try:
  from aiofile import AIOFile, LineReader, Writer

except:
	try:
			
		comando = os.system
		comando('sudo pip3 install aiofile')
		print('[!] Tentando Instalar as Dependencias')
	except:

		if IOError:	
			sys.exit("[!] Please install the aiofile library: sudo pip3 install aiofile")	
		
		else:  
			sleep(10)   
			comando('python3 servico_de_validacao.py')	






PYTHONASYNCIODEBUG=1
failsafe_tasks=[]
failsafe_cpf = []
responses = []
pendentes_f = []
result=None	
contador_failsafe = 0

async def api_validation_request(session, url,index):
	async with session.get(url) as response:
		response = await response.read()
		response_fix =json.loads(response)
		response_fix['CPF'] = url[49:60]
		response_fix['index'] = index
		""" print(response_fix) """
		if len(response_fix)>0:
			await query_generator(response_fix)
		
		else:
			pass





def db_handler():
	log = logging.getLogger('db_handler')
	log.info('iniciando conexão com Banco de Dados.')
	try:
		mydb = mysql.connector.connect(
			host="10.255.237.4",
			user="bwadmin",
			passwd="8bNmFLiIPhVRrM",
			database="megasorte"

		)
		log.info('Conexão esstabelecida com Sucesso!')
		return mydb
	except mysql.connector.Error as err:
		log.info('Erro ao conecar com o Banco de Dados.')
		sleep(3)
		sys.exit("[!]Não foi possivel conectar a base de dados! Erro {}".format(err))  
	
   

async def list_generator(database):
	global result
	log = logging.getLogger('list_generator')
	log.info('Buscando registros pendentes na base de dados.')
	executor= database.cursor()
	executor.execute("SELECT  CPFCNPJ, DtNascimento, id, Nome FROM cliente_dev where id_status =0 order by Nome asc ,id desc LIMIT 30")
	result = executor.fetchall()
	log.info('{0} itens serão analisados.'.format(len(result)))
	log.info('Aguarde!')
	lista = []

	for x in result:
		if x[0]!= None and x[1]!=None:
			if len(x[0]) > 11:
				checa_cpfcnpj = cpf.isCnpjValid(x[0])
			else:
				checa_cpfcnpj = cpf.isCpfValid(x[0])

			if checa_cpfcnpj==True:
				lista.append("https://ws.hubdodesenvolvedor.com.br/v2/cpf/?cpf={0}&data={1}&token=63764620RjLiAJcVnv115125088".format(x[0], x[1].strftime("%d/%m/%Y")))
			else:
				data = {}
				data['status'] = False
				data['id'] = x[2]
				data['code'] = 1
				data['message'] ="Cliente {0} não foi validado pois o CPF/CNPJ: {1} esta incorreto ".format(x[2],x[0])
				
				await query_generator(data)
		else:
			if x[0]== None:
				data = {}
				data['status'] = False
				data['id'] = x[2]
				data['code'] = 2
				data['message'] ='Cliente {0} não foi validado pois o CPF/CNPJ esta em branco'.format(x[2])
				await query_generator(data)
				
			else:	
				if( x[1]== None and (x[3]==None or x[3]=="" )):
					
					await failsafe_api_validation_request(x[0])
				else:	
					if	x[1]== None:
						data = {}
						data['status'] = False
						data['id'] = x[2]
						data['code'] = 3
						data['message'] ="Cliente {0} não foi validado pois 0 campo Dtnascimento esta em branco".format(x[2])
						await query_generator(data)

	
	return lista 	



async def failsafe_api_validation_request(CPF):
	
		
	global contador_failsafe
	contador_failsafe = contador_failsafe+1
	log = logging.getLogger('failsafe_api_validation_request')
	log.info('Realizando requisição à API soawebservices')
	
	url = "http://www.soawebservices.com.br/restservices/producao/cdc/pessoafisicaestendida.ashx"
	data={
	'Credenciais': {
		'Email': 'ti@bwabrasil.com.br',
		'Senha': 'prucdNTE'
	},
	"Documento": str(CPF)
	}
	params = json.dumps(data).encode('utf8')
	async with aiohttp.ClientSession() as s:
		async with s.post(url, data=params) as r:

			""" req =  request.Request(url, data=params,headers={'content-type': 'application/json'} ) # this will make the method "POST"
			response = request.urlopen(req) """
		
			response =  await r.read()
			response_fix=json.loads(response)
			response_fix['failsafe'] = True
			if len(response_fix)>0:
				await query_generator(response_fix)
	
		

async def query_generator(resp):
	global result
	caracteres = ['.','-']
	data=[]
	failsafe=[]
	if len(resp)>0:
		try:
			r = resp['failsafe']
			if r:
				if(resp['failsafe']==True):
					failsafe.append(resp)
					with open("response.json","a+") as f: #Analizar Resposatas e Gerar Querys 
						for item in failsafe:
							f.write("%s\n"%item)
					with open("query.txt","a+") as f:
						for item in failsafe:
							if item['Status'] == True:
								item['DataNascimento'] = datetime.datetime.strptime(item['DataNascimento'], "%d/%m/%Y").strftime("%Y-%m-%d")
								message = 'Verificado via API '
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
			with open("response.json","a+") as f: #Analizar Resposatas e Gerar Querys 
				for item2 in data:
					f.write("%s\n"%item2)  
			
			with open("query.txt","a+") as f:
				for item2 in data:
					try:
						r = item2['result']['numero_de_cpf']
						if r:
							item2['result']['numero_de_cpf'] = item2['result']['numero_de_cpf'].replace(caracteres,'')	
					except :
						pass

					if item2['status']==True:
						
						message = 'Verificado via API através do codigo {0} em {1}'.format(item2['result']['comprovante_emitido'], item2['result']['comprovante_emitido_data'])
						f.write("UPDATE cliente SET id_status='1', Nome = '{0}' , motivo ='{1}'  WHERE CPFCNPJ = '{2}';\n".format(item2['result']['nome_da_pf'],message,item2['result']['numero_de_cpf']))#Gerar query caso o TRUE
					elif item2['status']==False:
						try:
							item2['code']
							if item2['code'] == 1:
								f.write("UPDATE cliente SET id_status='2', motivo = '{0}' WHERE id = {1};\n".format(item2['message'],item2['id']))
							elif item2['code'] == 2:
								f.write("UPDATE cliente SET id_status='2', motivo = '{0}' WHERE id = {1};\n".format(item2['message'],item2['id']))
							elif item2['code'] == 3:
								f.write("UPDATE cliente SET id_status='2', motivo = '{0}' WHERE id = {1};\n".format(item2['message'],item2['id']))
						except:

							if item2['return']=='NOK':
								
								if "CPF Nao Encontrado na Base de Dados Federal." in item2['message']:
									f.write("UPDATE cliente SET id_status='3', motivo = '{0}' WHERE CPFCNPJ = {1};\n".format(item2['message'],item2['CPF']))
								elif "Data Nascimento invalida." in item2['message']:
									try:
										check = item2['CPF']
										if check and (result[item2['index']][3] == None or result[item2['index']][3] == "" ):
											
											await failsafe_api_validation_request(item2['CPF'])
										
										else:
											f.write("UPDATE cliente SET id_status='2', motivo = '{0}' WHERE CPFCNPJ = {1};\n".format(item2['message'],item2['CPF']))
											
									except:
										pass
										
							

									#f.write("UPDATE cliente SET id_status='2', motivo = '{0}' WHERE CPFCNPJ = {1};\n".format(item['message'],item['CPF']))
								elif  "Token Inválido ou sem saldo para a consulta." in item['message'] :
									sys.exit(item2['message'])	
						else:
							pass

async def query_generator2(resp):
	global result
	caracteres = ['.','-']
	data=[]
	failsafe=[]
	if len(resp)>0:
		try:
			r = resp['failsafe']
			if r:
				if(resp['failsafe']==True):
					failsafe.append(resp)
					with open("response.json","a+") as f: #Analizar Resposatas e Gerar Querys 
						for item in failsafe:
							f.write("%s\n"%item)
					with open("query.txt","a+") as f:
						for item in failsafe:
							if item['Status'] == True:
								message = 'Verificado via API '
								f.write("UPDATE cliente SET id_status='1', Nome = '{0}' , motivo ='{1}', DtNascimento=0{2}  WHERE CPFCNPJ = '{3}';\n".format(item['Nome'],message,item['DataNascimento'], item['Documento']))#Gerar query caso o TRUE
							if item['Status'] == False:
								f.write("UPDATE cliente SET id_status='3', ' , motivo ='{0}  WHERE CPFCNPJ = '{1}';\n".format(item['Mensagem'], item['Documento']))#Gerar query caso o TRUE
							else:
								pass
			else:
				pass
				
		except:
			pass
				
			
			data.append(resp)
			with open("response.json","a+") as f: #Analizar Resposatas e Gerar Querys 
				for item2 in data:
					f.write("%s\n"%item2)  
			
			with open("query.txt","a+") as f:
				for item2 in data:
					try:
						r = item2['result']['numero_de_cpf']
						if r:
							item2['result']['numero_de_cpf'] = item2['result']['numero_de_cpf'].replace(caracteres,'')	
					except :
						pass

					if item2['status']==True:
						
						message = 'Verificado via API através do codigo {0} em {1}'.format(item2['result']['comprovante_emitido'], item2['result']['comprovante_emitido_data'])
						f.write("UPDATE cliente SET id_status='1', Nome = '{0}' , motivo ='{1}'  WHERE CPFCNPJ = '{2}';\n".format(item2['result']['nome_da_pf'],message,item2['result']['numero_de_cpf']))#Gerar query caso o TRUE
					elif item2['status']==False:
						try:
							item2['code']
							if item2['code'] == 1:
								f.write("UPDATE cliente SET id_status='2', motivo = '{0}' WHERE id = {1};\n".format(item2['message'],item2['id']))
							elif item2['code'] == 2:
								f.write("UPDATE cliente SET id_status='2', motivo = '{0}' WHERE id = {1};\n".format(item2['message'],item2['id']))
							elif item2['code'] == 3:
								f.write("UPDATE cliente SET id_status='2', motivo = '{0}' WHERE id = {1};\n".format(item2['message'],item2['id']))
						except:

							if item2['return']=='NOK':
								
								if "CPF Nao Encontrado na Base de Dados Federal." in item2['message']:
									f.write("UPDATE cliente SET id_status='3', motivo = '{0}' WHERE CPFCNPJ = {1};\n".format(item2['message'],item2['CPF']))
								elif "Data Nascimento invalida." in item2['message']:
									try:
										check = item2['CPF']
										if check and (result[item2['index']][3] == None or result[item2['index']][3] == "" ):
											
											await failsafe_api_validation_request(item2['CPF'])
											
												
											
									except:
										pass
							

									#f.write("UPDATE cliente SET id_status='2', motivo = '{0}' WHERE CPFCNPJ = {1};\n".format(item['message'],item['CPF']))
								elif  "Token Inválido ou sem saldo para a consulta." in item['message'] :
									sys.exit(item2['message'])	
						else:
							pass

async def runner(executor):
	index = 0
	log = logging.getLogger('Iniciando Solicitações a API hubdodesenvolvedor ')
	log.info('starting')
	tasks=[]
	log.info('Criando tarefas')
	loop = asyncio.get_event_loop()
	async with aiohttp.ClientSession() as session:
		with concurrent.futures.ThreadPoolExecutor() as pool:
			for url in pendentes:#Não to usando os Workers, para utilizar devo quebrar a lista usando slices
				
				task = asyncio.ensure_future(api_validation_request(session, url, index))
				tasks.append(task)
				index = index +1 

			await asyncio.gather(*tasks, return_exceptions=True)
		
			log.info('exiting')


if __name__ == "__main__":
	logging.basicConfig(
		level=logging.INFO,
		format='PID %(process)5s %(name)18s: %(message)s',
		stream=sys.stderr,
 	)
	start_time = time.time()
	
	
	log = logging.getLogger('main')
	log.info('Inicializando serviço de Validação de cadastros...')
	db = db_handler()
	
	loop = asyncio.get_event_loop()
	pendentes=loop.run_until_complete(list_generator(db))
 
	

	
	executor = concurrent.futures.ThreadPoolExecutor(
		max_workers=3,
	)
	event_loop = asyncio.get_event_loop()
	try:
		event_loop.run_until_complete(
			runner(executor)
		)
	finally:
		event_loop.close()

	duration = time.time() - start_time

	
	log.info("Foram efetuadas {0} requisições à API soawebservices".format(contador_failsafe))
	log.info(f"Total de {len(pendentes)} dados consultados em {duration} seconds")
	log.info("Encerrando serviço")






