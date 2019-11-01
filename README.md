# PythonServer
Aqui estão sendo desenvolvidos scripts para validação de regsitros por meio de API's
por se tratarem de um alto volume de registros os mesmos não podem ser realizados de
forma síncrona, para solucionar tal problema está sendo utilizado a biblioteca ASYNCIO
	Diagrama:

	   _______________                 ___________  
      |     Pool      |               |  FILA     |  
      |      de       |-------------->|___________|                _____________  
      |  requisições  |                |___________|              |             |
      |_______________|                 |___________| ----------> | Relatórios  |
                                                                  |_____________|
As validações são realizadas verificando informações como CEP, CPF e data de nascimento,
e por fim gera querys para serem executadas no banco de dados





