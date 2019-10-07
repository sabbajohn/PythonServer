import asyncio
import time
import aiohttp
import json
import mysql.connector
import datetime
from aiofile import AIOFile, LineReader, Writer
import cpf


responses = []
async def download_site(session, url):
    async with session.get(url) as response:
        response = await response.read()
        response_fix =json.loads(response)
        print(response_fix)
        responses.append(response_fix)
       


async def download_all_sites(sites):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in sites:
            task = asyncio.ensure_future(download_site(session, url))
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
    executor.execute("SELECT CPFCNPJ, DtNascimento, id FROM cliente where id_status = 0 order by id DESC LIMIT 40 ")
    result = executor.fetchall()
    lista = []
    for x in result:
        if x[0]!= None and x[1]!=None:
            if len(x[0]) > 11:
                checa_cpfcnpj = cpf.isCnpjValid(x[0])
            else:
                checa_cpfcnpj = cpf.isCpfValid(x[0])

            if checa_cpfcnpj==True:
                lista.append ("https://ws.hubdodesenvolvedor.com.br/v2/cpf/?cpf={0}&data={1}&token={Bota o token aqui}".format(x[0], x[1].strftime("%d/%m/%Y")))
            else:
                responses.append('Cliente {0} não foi validado pois o CPF/CNPJ: {1} esta incorreto '.format(x[2],x[0]))
        else:
            if x[0]== None:
                
                responses.append('Cliente {0} não foi validado pois o CPF/CNPJ esta em branco'.format(x[2]))
            else:    
                if x[1]== None:
                    
                    responses.append("Cliente {0} não foi validado pois 0 campo Dtnascimento esta em branco".format(x[2]))


    return lista   


def query_generator(data):
    with open("query.txt","a+") as f:
        for item in data:
            if data['status']=='TRUE':
                f.write("UPDATE cliente SET Nome = {0}, id_status={1}".format())#Gerar query caso o TRUE


if __name__ == "__main__":
    db = db_handler()
    sites = list_generator(db) 
    start_time = time.time()
    asyncio.get_event_loop().run_until_complete(download_all_sites(sites))
    duration = time.time() - start_time
    with open("response.json","a+") as f: #Analizar Resposatas e Gerar Querys 
        for item in responses:
            f.write("%s\n"%item)  
    
    print(f"Total de {len(sites)} dados consultados em {duration} seconds")



"""


     Exemplo de uso da API
https://ws.hubdodesenvolvedor.com.br/v2/cpf/?cpf=21315050862&data=02/05/1978&token={bota o token aqui} 
status_id {
    1 - ok
    2 - suspenso
    0 - nao verificado
}



"""


