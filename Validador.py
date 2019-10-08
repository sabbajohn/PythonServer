import asyncio
import time
import aiohttp
import json
import mysql.connector
import datetime
from aiofile import AIOFile, LineReader, Writer
import cpf


responses = []
async def api_validation_request(session, url):
    async with session.get(url) as response:
        response = await response.read()
        response_fix =json.loads(response)
        print(response_fix)
        responses.append(response_fix)
       


async def list_of_requests_pending(sites):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in sites:
            task = asyncio.ensure_future(api_validation_request(session, url))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)

def db_handler():
    mydb = mysql.connector.connect(
    host="localhost",
    user="objetiva",
    passwd="spqQVJ161",
    database="megasorte"
    )
   
    return mydb
   

def list_generator(database):
    executor= database.cursor()
    executor.execute("SELECT CPFCNPJ, DtNascimento, id FROM cliente where id_status = 0 order by id DESC LIMIT 100 ")
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
                
                responses.append(data)
        else:
            if x[0]== None:
                data = {}
                data['status'] = False
                data['id'] = x[2]
                data['code'] = 2
                data['message'] ='Cliente {0} não foi validado pois o CPF/CNPJ esta em branco'.format(x[2])
                responses.append(data)
                
            else:    
                if x[1]== None:
                    data = {}
                    data['status'] = False
                    data['id'] = x[2]
                    data['code'] = 3
                    data['message'] ="Cliente {0} não foi validado pois 0 campo Dtnascimento esta em branco".format(x[2])
                    responses.append(data)
                    


    return lista   


def query_generator(data):
    with open("query.txt","a+") as f:
        for item in data:
            if item['status']==True:
                message = 'Verificado via API através do codigo {0} em {1}'.format(item['result']['comprovante_emitido'], item['result']['comprovante_emitido_data'])
                f.write("UPDATE cliente SET id_status='1', nome = '{0}' , motivo ='{1}'  WHERE CPFCNPJ = '{2}';\n".format(item['result']['nome_da_pf'],message,item['result']['numero_de_cpf']))#Gerar query caso o TRUE
            elif item['status']==False:
                if item['code'] == 1:
                    f.write("UPDATE cliente SET id_status=2, motivo = '{0}' WHERE id = {1};\n".format(item['message'],item['id']))#Gerar query caso o TRUE
                elif item['code'] == 2:
                    f.write("UPDATE cliente SET id_status=3, motivo = '{0}' WHERE id = {1};\n".format(item['message'],item['id']))#Gerar query caso o TRUE
                elif item['code'] == 3:
                    f.write("UPDATE cliente SET id_status=3, motivo = '{0}' WHERE id = {1};\n".format(item['message'],item['id']))#Gerar query caso o TRUE

if __name__ == "__main__":
    db = db_handler()
    sites = list_generator(db) 
    start_time = time.time()
    asyncio.get_event_loop().run_until_complete(list_of_requests_pending(sites))
    duration = time.time() - start_time
    query_generator(responses)
    with open("response.json","a+") as f: #Analizar Resposatas e Gerar Querys 
        for item in responses:
            f.write("%s\n"%item)  
    
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


