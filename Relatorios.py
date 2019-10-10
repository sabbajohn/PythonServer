import mysql.connector
import sys
class Relatorios(object):
    def query_generator(resp):
        if len(resp)>0:
            
            
            data = resp
            
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

    def responses(responses):
        with open("response_api.json","a+") as f: 
            for item in responses:
                f.write("%s\n"%item)  

    def __init__(self):
       self