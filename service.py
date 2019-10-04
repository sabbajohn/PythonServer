import os
import queue
import threading
import sys
import socket
import getopt
import subprocess
import urllib3
import requests
from itertools import islice

"""          POS---------
                           ---                        <--------
                               -----> MIRCROSERVICE                         RECEITA(API)
                              -              |↑        -------->
                              -              ||
                           ---               ||
              SITE---------                  ||
                                             ↓|
                                          Banco de Dados

  * As informacoes serao oriunda das maquinas POS, SITE e Banco de Dados, ao receber essas requisicoes serao criadas filas com prioridade para fazer requisicoes a API de consulta da Receita Federal
  * As Requisicoes oriundas da POS terao prioridade sobre as demais
  * Durante o tempo ocioso deverá validar os cadastros do banco de dados

  * Enquanto houver dados nas filas as requisições a API deverão ser feitas




  """





def FileHandler(file):
        with open(filename, 'r') as infile:
                lines_gen = islice(infile, N)
                for line in lines_gen:
                        #cria as threads de requisição








def requestData(dados):
        URL = 127.0.0.1
        token = 987654321
        cpf =dados['cpf']
        nascimento =dados['cpf']
        PARAMS{"cpf": cpf,
        "data_de_nascimento": nascimento,
        "Token":token
        }
        r=requests.get(url = URL, params = PARAMS)
        resp = r.json()
        #Analisa Resposta e gera as querys ....
        #Caso Forbidden parar e notificar( Provavelmente credito)
        #Caso timeout tentar outra vez








#GLOBALS
""" listen             = False
command            = False
upload             = False
execute            = ""
target             = ""
upload_destination = ""
port               = 0
port_settings =[('pos',4444),('web',4445),('extra',4446)]
port_settings = dict(port_settings)

 """

""" def server_loop():
        global target
        global port
        if not len(target):
                target= "0.0.0.0"
                server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.bind((target,port))
                server.listen(5)

                while True:
                        client_socket, addr = server.accept()

                        # spin off a thread to handle our new client
                        client_thread = threading.Thread(target=client_handler,args=(client_socket,))
                        client_thread.start()
 """""" def run_command(command):

        # trim the newline
        command = command.rstrip()

        # run the command and get the output back
        try:
                output = subprocess.check_output(command,stderr=subprocess.STDOUT, shell=True)
        except:
                output = "Failed to execute command.\r\n"

        # send the output back to the client
        return output

def client_handler(client_socket):
        global upload
        global execute
        global command

        # check for upload
        if len(upload_destination):

                # read in all of the bytes and write to our destination
                file_buffer = ""

                # keep reading data until none is available
                while True:
                        data = client_socket.recv(1024)

                        if not data:
                                break
                        else:
                                file_buffer += data

                # now we take these bytes and try to write them out
                try:
                        file_descriptor = open(upload_destination,"wb")
                        file_descriptor.write(file_buffer)
                        file_descriptor.close()

                        # acknowledge that we wrote the file out
                        client_socket.send("Successfully saved file to %s\r\n" % upload_destination)
                except:
                        client_socket.send("Failed to save file to %s\r\n" % upload_destination)



        # check for command execution
        if len(execute):

                # run the command
                output = run_command(execute)

                client_socket.send(output)


        # now we go into another loop if a command shell was requested
        if command:

                while True:
                        # show a simple prompt
                        client_socket.send("<BHP:#> ")

                        # now we receive until we see a linefeed (enter key)
                        cmd_buffer = ""
                        while "\n" not in cmd_buffer:
                                cmd_buffer += client_socket.recv(1024)


                        # we have a valid command so execute it and send back the results
                        response = run_command(cmd_buffer)

                        # send back the response
                        client_socket.send(response)

# this is for incoming connections
 """
