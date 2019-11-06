
import sys
import datetime
from Class import db
import getpass
USER = getpass.getuser()


class Relatorios(object):

	def query_generator(self, resp):
		executor = self.database.getCursor()
		if len(resp)>0:
		
			
			data = resp
			
			with open("/home/"+USER+"/PythonServer/queries/query_api.txt","a+") as f:
				for item in data:
					if item['status']==True:
						message = 'Verificado via API através do codigo {0} em {1}'.format(item['result']['comprovante_emitido'], item['result']['comprovante_emitido_data'])
						try:
							print("[!] Tentando atualizar a base de dados!")
							
							executor.execute("UPDATE cliente SET id_status='1', nome = '{0}' , motivo ='{1}'  WHERE CPFCNPJ = '{2}';\n".format(item['result']['nome_da_pf'],message,item['result']['numero_de_cpf']))
							self.database.mydb.commit()
						except:
							print("[!][!][!] Não foi possivel, mas voce pode efutar a atualização manualmente através do arquivo query.txt!")
							pass
						

						f.write("UPDATE cliente SET id_status='1', nome = '{0}' , motivo ='{1}'  WHERE CPFCNPJ = '{2}';\n".format(item['result']['nome_da_pf'],message,item['result']['numero_de_cpf']))#Gerar query caso o TRUE
					elif item['status']==False:
						try:
							item['code']
							if item['code'] == 1:
								try:
									print("[!] Tentando atualizar a base de dados!")
									executor.execute("UPDATE cliente SET id_status='2', motivo = '{0}' WHERE id = {1};\n".format(item['message'],item['id']))
									self.database.mydb.commit()
								except:
									print("[!][!][!] Não foi possivel, mas voce pode efutar a atualização manualmente através do arquivo query.txt!")
									pass
								

								f.write("UPDATE cliente SET id_status='2', motivo = '{0}' WHERE id = {1};\n".format(item['message'],item['id']))
							elif item['code'] == 2:
								try:
									print("[!] Tentando atualizar a base de dados!")
									executor.execute("UPDATE cliente SET id_status='2', motivo = '{0}' WHERE id = {1};\n".format(item['message'],item['id']))
									self.database.mydb.commit()
								except:
									print("[!][!][!] Não foi possivel, mas voce pode efutar a atualização manualmente através do arquivo query.txt!")
									pass
								

								f.write("UPDATE cliente SET id_status='2', motivo = '{0}' WHERE id = {1};\n".format(item['message'],item['id']))
							elif item['code'] == 3:
								try:
									print("[!] Tentando atualizar a base de dados!")
									executor.execute("UPDATE cliente SET id_status='2', motivo = '{0}' WHERE id = {1};\n".format(item['message'],item['id']))
									self.database.mydb.commit()
								except:
									print("[!][!][!] Não foi possivel, mas voce pode efutar a atualização manualmente através do arquivo query.txt!")
									pass
								

								f.write("UPDATE cliente SET id_status='2', motivo = '{0}' WHERE id = {1};\n".format(item['message'],item['id']))
								self.database.mydb.commit()
						except:
							if item['return']=='NOK':
								if "CPF Nao Encontrado na Base de Dados Federal." in item['message']:
									try:
										print("[!] Tentando atualizar a base de dados!")
										executor.execute("UPDATE cliente SET id_status='3', motivo = '{0}' WHERE CPFCNPJ = {1};\n".format(item['message'],item['CPF']))
										self.database.mydb.commit()
									except:
										print("[!][!][!] Não foi possivel, mas voce pode efutar a atualização manualmente através do arquivo query.txt!")
										pass

									f.write("UPDATE cliente SET id_status='3', motivo = '{0}' WHERE CPFCNPJ = {1};\n".format(item['message'],item['CPF']))
								elif "Data Nascimento invalida." in item['message']:
									try:
										print("[!] Tentando atualizar a base de dados!")
										executor.execute("UPDATE cliente SET id_status='2', motivo = '{0}' WHERE CPFCNPJ = {1};\n".format(item['message'],item['CPF']))
										self.database.mydb.commit()
									except:
										print("[!][!][!] Não foi possivel, mas voce pode efutar a atualização manualmente através do arquivo query.txt!")
										pass
									

									f.write("UPDATE cliente SET id_status='2', motivo = '{0}' WHERE CPFCNPJ = {1};\n".format(item['message'],item['CPF']))
								elif  "Token Inválido ou sem saldo para a consulta." in item['message'] :
									sys.exit(item['message'])	
						else:
							self.database.mydb.commit()
							pass

	def responses(self,responses):
		with open("/home/"+USER+"/PythonServer/responses/response_api.json","a+") as f: 
			for item in responses:
				f.write("{0}:{1}\n".format(datetime.datetime.now() ,item))

	def __init__(self):
	 self.database = db()
	   