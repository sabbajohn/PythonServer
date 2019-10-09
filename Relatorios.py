import mysql.connector

class Relatorios(object):
    def query_generator(data):
        with open("query_api.txt","a+") as f:
            for item in data:
                if item['status']==True:
                    message = 'Verificado via API através do codigo {0} em {1}'.format(item['result']['comprovante_emitido'], item['result']['comprovante_emitido_data'])
                    f.write("UPDATE cliente SET id_status='1', nome = '{0}' , motivo ='{1}'  WHERE CPFCNPJ = '{2}';\n".format(item['result']['nome_da_pf'],message,item['result']['numero_de_cpf']))#Gerar query caso o TRUE
                elif item['status']==False:
                    if item['code'] == 1:
                        f.write("UPDATE cliente SET id_status=2, motivo = '{0}' WHERE CPFCNPJ = {1};\n".format(item['message'],item['id']))
                    elif item['code'] == 2:
                        f.write("UPDATE cliente SET id_status=3, motivo = '{0}' WHERE CPFCNPJ = {1};\n".format(item['message'],item['id']))
                    elif item['code'] == 3:
                        f.write("UPDATE cliente SET id_status=3, motivo = '{0}' WHERE CPFCNPJ = {1};\n".format(item['message'],item['id']))

    def responses(responses):
        with open("response_api.json","a+") as f: 
            for item in responses:
                f.write("%s\n"%item)  

    def __init__(self):
       self