# PythonServer
    Hoje o Validador.py esta em funcionamento somene, seguindo os esforços para fazer com que os posts recebidos no server.py sejam encaminhadas para
    validador.
    
    Alguns metodos foram copiados para arquivos separados para que em breve toda esta estrutura possa ser organizada em classes
    
    Proximo desafio:
        Escrever as saidas de relatorio a medida que as respostas vão chegando...


        Instanciar objeto e deixar que suas respesctivas threads:
        Inicializo a estrutura de dados vazia...
        O pool de requisições alimenta a estrutura
        cada thread insere um nó em uma ponta ao finalizar;
        Uma subrotina Relatorios consumirá na outra ponta da estrutura os nós enquanto eles existirem.     
       _______________                 ___________  
      |     Pool      |               |  FILA     |  
      |      de       |-------------->|___________|                _____________  
      |  requisições  |                |___________|              |             |
      |_______________|                 |___________| ----------> | Relatórios  |
                                                                  |_____________|

        
Modulos necessários em req.txt

