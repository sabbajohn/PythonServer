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

... 
É o Beta é um pouquinho alem do descrito acima, so um pouquinho...

algumas coisas ainda por fazer...
TODO
	* Configurar "Get started quickly"
		- https://bitbucket.org/objetiva/python-services/src
		
	* Capturar execeções e gerenciar as threads!
		- Em andamento, ainda ha varias exceções a serem tratadas e conhecidas

	* Aprimorar o banco para que seja estabelecida uma unica conexão e esta seja partilhada pelos serviços 
		- metodos execute, commit,... devem ser efetuado dentro da classe de dados

	* Definir arquivos de Configuração e ENV
		- Arquivos prontos, substituindo gradativamento no codigo

	* Implementar biblioteca de notificação de erros.

	* Implementar mecanismos de deploy
		- utilizar modulo Chapter 7 como base

	* Desenvolver Interface gráfica

	[!]BONUS[!] : 
		* Multithreads vs Multi Process






