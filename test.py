#!/usr/bin/python3
# coding: utf-8
import sys
import os
import time
import json
import cpf
from time import sleep
import datetime
import asyncio.coroutines
import logging
import concurrent.futures
import urllib
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
			comando('python3 Validador.py')

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
			comando('python3 Validador.py')	
			
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
			comando('python3 Validador.py')	
			

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
			comando('python3 Validador.py')	








responses = []
async def api_validation_request(executor, url):
		
		response =urllib.request.urlopen(url)
		response_fix =json.loads(response)
		response_fix['CPF'] = url[49:60]
		print(response_fix)
		if len(response_fix)>0:
			QG.send(response_fix)
			
		
		else:
			pass


async def list_of_requests_pending(executor,sites):
	log = logging.getLogger('list_of_requests_pending')
	log.info('starting')

	log.info('creating executor tasks')

		
	loop = asyncio.get_event_loop()
	tasks = [
		loop.run_in_executor(executor,api_validation_request, url)
		for url in sites
	]
		
	""" await asyncio.gather(*tasks, return_exceptions=True) """
	log.info('waiting for executor tasks')
	completed, pending = await asyncio.wait(tasks)
	results = [t.result() for t in completed]
    log.info('results: {!r}'.format(results))
	log.info('exiting')

def db_handler():
	try:
		mydb = mysql.connector.connect(
		host="localhost",
		user="objetiva",
		passwd="spqQVJ161",
		database="megasorte"
	   
		)   
		return mydb
	except mysql.connector.Error as err:
		sys.exit("[!]Não foi possivel conectar a base de dados! Erro {}".format(err))  
	
   

def list_generator(database):
	executor= database.cursor()
	executor.execute("SELECT CPFCNPJ, DtNascimento, id FROM cliente where id_status = 0 order by id ASC LIMIT 1000 ")
	result = executor.fetchall()
	lista = []
	for x in result:
		if x[0]!= None and x[1]!=None:
			if len(x[0]) > 11:
				checa_cpfcnpj = cpf.isCnpjValid(x[0])
			else:
				checa_cpfcnpj = cpf.isCpfValid(x[0])

			if checa_cpfcnpj==True:
				lista.append ("https://ws.hubdodesenvolvedor.com.br/v2/cpf/?cpf={0}&data={1}&token=63764620RjLiAJcVnv115125088".format(x[0], x[1].strftime("%d/%m/%Y")))
			else:
				data = {}
				data['status'] = False
				data['id'] = x[2]
				data['code'] = 1
				data['message'] ="Cliente {0} não foi validado pois o CPF/CNPJ: {1} esta incorreto ".format(x[2],x[0])
				
				
				QG.send(data)
		else:
			if x[0]== None:
				data = {}
				data['status'] = False
				data['id'] = x[2]
				data['code'] = 2
				data['message'] ='Cliente {0} não foi validado pois o CPF/CNPJ esta em branco'.format(x[2])
				
				QG.send(data)
				
			else:	
				if x[1]== None:
					data = {}
					data['status'] = False
					data['id'] = x[2]
					data['code'] = 3
					data['message'] ="Cliente {0} não foi validado pois 0 campo Dtnascimento esta em branco".format(x[2])
					
					QG.send(data)
					


	return lista   


def query_generator():
	try:
		while True:
			
			resp = (yield) 
			data=[]
			data.append(resp)
			if(resp):
				with open("response.json","a+") as f: #Analizar Resposatas e Gerar Querys 
					for item in data:
						f.write("%s\n"%item)  

				with open("query.txt","a+") as f:
					for item in data:
						if item['status']==True:
							message = 'Verificado via API através do codigo {0} em {1}'.format(item['result']['comprovante_emitido'], item['result']['comprovante_emitido_data'])
							f.write("UPDATE cliente SET id_status='1', nome = '{0}' , motivo ='{1}'  WHERE CPFCNPJ = '{2}';\n".format(item['result']['nome_da_pf'],message,item['result']['numero_de_cpf']))#Gerar query caso o TRUE
						elif item['status']==False:
							try:
								item['code']
								if item['code'] == 1:
									f.write("UPDATE cliente SET id_status='2', motivo = '{0}' WHERE id = {1};\n".format(item['message'],item['id']))
								elif item['code'] == 2:
									f.write("UPDATE cliente SET id_status='2', motivo = '{0}' WHERE id = {1};\n".format(item['message'],item['id']))
								elif item['code'] == 3:
									f.write("UPDATE cliente SET id_status='2', motivo = '{0}' WHERE id = {1};\n".format(item['message'],item['id']))
							except:
								if item['return']=='NOK':
									if "CPF Nao Encontrado na Base de Dados Federal." in item['message']:
										f.write("UPDATE cliente SET id_status='3', motivo = '{0}' WHERE CPFCNPJ = {1};\n".format(item['message'],item['CPF']))
									elif "Data Nascimento invalida." in item['message']:
										f.write("UPDATE cliente SET id_status='2', motivo = '{0}' WHERE CPFCNPJ = {1};\n".format(item['message'],item['CPF']))
									elif  "Token Inválido ou sem saldo para a consulta." in item['message'] :
										sys.exit(item['message'])	
							else:
								pass
							
	except GeneratorExit:
		pass
	
		   
		
if __name__ == "__main__":
	logging.basicConfig(
		level=logging.INFO,
		format='PID %(process)5s %(name)18s: %(message)s',
		stream=sys.stderr,
	)
	QG = query_generator()
	QG.__next__()
	db = db_handler()
	
	sites = list_generator(db) 
	start_time = time.time()
	
	
	executor = concurrent.futures.ThreadPoolExecutor(
		max_workers=4,
	)
	event_loop = asyncio.get_event_loop()
	try:
		event_loop.run_until_complete(
			list_of_requests_pending(executor,sites)
		)
	finally:
		event_loop.close()
		duration = time.time() - start_time
	
	
	
	print(f"Total de {len(sites)} dados consultados em {duration} seconds")



"""


	 Exemplo de uso da API
https://ws.hubdodesenvolvedor.com.br/v2/cpf/?cpf=21315050862&data=02/05/1978&token={token}
status_id {
	1 - ok
	2 - suspenso
	0 - nao verificado
	3 - campos pendentes
}


Posso Transformar esse metodo em uma classe, fazenfo com que ela seja gerenciada por um outro script, rodando em outras subrotinas:
- Retira o handler do banco de dados para uma outra classe;

- Passa como parametro para desta classe a lista de pendentes com uso do slice
- a cada ciclo do slice ela retorna a variavel respones que pode ser recebida por um metodo de relatorios retirando desta a query_generator e a escrita do arquivo  responses.json
- 




"""


