# PythonServer

This README would normally document whatever steps are necessary to get your application up and running.
What is this repository for?

    Gerenciador de Serviços, sendo eles atualmente:
        Validação de Cadastro de Clientes (SVC)
        Atualização de Registros no Banco de Dados (SDU)
        Encaminhamento de SMS (SMS)
        Recuperação de Carrinhos Abandonados (SRC)

    Version 4.01b
    Learn Markdown

How do I get set up?

    Summary of set up
    Configuration
    Dependencies
    Database configuration
    How to run tests
    Deployment instructions

Contribution guidelines
 	
	Writing tests
    Code review
    Other guidelines
	
	Configurar "Get started quickly"
		-https://bitbucket.org/sabbajohn/pythonserver/src/master/

	Callback e Exceptions
		- Re-Analizar as tratativas de erros e exceçõe
		- Quase tudo tratado, alguns pontos a serem definidos. 
		- status 3 Encerrar serviço ou tentar conectar novamente com BD?!

	 WATCH e CWATCH 
		 - Poder setar configurações de Query e Delay atraves do cwatch,
		 - Status geral do sistemas
		 - Ultimos Registros
	


	Implementar Deploy e Mecanismo de Balanceamento
		- utilizar modulo Chapter 7 como base
	Desenvolver Interface gráfica para modulo cwatch.py
    
    Assegurar que independente do erro o Manager jamais se encerre, assim como o WATCH, para garantir que os serviços possam ser gerenciados via cwatch, e reinicializados caso necessário.

Who do I talk to?

    Repo owner or admin
    Other community or team contact


