import asyncio
import time
import aiohttp
import json
import mysql.connector
import datetime
from aiofile import AIOFile, LineReader, Writer


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
    executor.execute("SELECT CPFCNPJ, DtNascimento FROM cliente where id_status = 0 order by id DESC LIMIT 30 ")
    result = executor.fetchall()
    lista = []
    for x in result:
        if x[0]!= None and x[1]!=None:
            lista.append ("https://ws.hubdodesenvolvedor.com.br/v2/cpf/?cpf={0}&data={1}&token=63764620RjLiAJcVnv115125088".format(x[0], x[1].strftime("%d/%m/%Y")))
    return lista   




if __name__ == "__main__":
    db = db_handler()
    sites = list_generator(db) 
    start_time = time.time()
    asyncio.get_event_loop().run_until_complete(download_all_sites(sites))
    duration = time.time() - start_time
    with open("response.json","a+") as f:
        for item in responses:
            f.write("%s\n"%item)
    
    print(f"Total de {len(sites)} dados consultados em {duration} seconds")



"""


     Exemplo de uso da API
https://ws.hubdodesenvolvedor.com.br/v2/cpf/?cpf=21315050862&data=02/05/1978&token=63764620RjLiAJcVnv115125088 




"""


