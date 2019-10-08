
import cpf

class Tarefas_DB(object):
    
    def list_generator(self, database, responses):
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
                    lista.append ("https://ws.hubdodesenvolvedor.com.br/v2/cpf/?cpf={0}&data={1}&token={token}".format(x[0], x[1].strftime("%d/%m/%Y")))
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
