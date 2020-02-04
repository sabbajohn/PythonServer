#!/usr/bin/python3
# coding: utf-8

import sys
import socket
import getopt
import threading
import subprocess
import json
import time
from termcolor import colored
import signal
import os


# define some global variables
command				= True
target			 	= ""
upload_destination 	= ""
port			 	= 0
client 				= None

servico_msg			= None
servico				= None
# this runs a command and returns the output


# if we don't listen we are a client....make it so.
def client_sender(buffer):
		global target
		global port
		global client
		global servico_msg
		global servico

		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		if target == "" and not port > 0:
			target = "0.0.0.0"
			port = 5000
		try:
				# connect to our target host
				client.connect((target,port))
				# if we detect input from stdin send it 
				# if not we are going to wait for the user to punch some in
		except Exception as e: 
			
			print(colored(e, "yellow"))
			print(colored("Não foi possivel conectar","red"))
			os.kill(os.getpid(),signal.SIGINT)
		else:
			print(colored("Connected","green"))
			Menu()
		
					
						

						

			
				
""" except (ConnectionResetError,BrokenPipeError) as e:
	print(colored(type(e), "red", "on_grey"))	
	print(colored(e, "yellow"))
	print(colored("Conexão perdida!","red"))
	os.kill(os.getpid(),signal.SIGINT) """

""" except (ConnectionResetError,BrokenPipeError) as e: """

		
			


def formata(parameter_list):
	pass

def query_svc():
	data = {
		"servico"	: servico,
		"action"	: "query_list"
	}
	client.send(bytes(json.dumps(data).encode()))
	while recv_len:
		data	 = str(client.recv(4096),encoding="utf-8").rstrip()
		recv_len = len(data)
		response+= data
		
		if recv_len < 4096:
				break
		if len(response):
			keys = response.keys()
		for key in keys:
			print(colored("{}".format(key), "blue"))
			for i, x in enumerate(response[key]):
				print(colored("{}:{}".format(i,x), "green"))
	print(colored("Querys SVC", "blue"))
	print(colored("1) Definir Querys a serem executadas","cyan") )
	print(colored("2) Adcionar nova Query","cyan") )
	print(colored("3) Voltar ao menu do Serviço","cyan") )
	print(colored("00) Voltar ao Menu Principal","cyan") )
	buffer = input('')
	if "1" in buffer:
		value = input('')
		data = {
		"servico"	: servico,
		"action"	: "query_set",
		"value"		: value
	}
		client.send(bytes(json.dumps(data).encode()))
	elif "2" in buffer:
		value = input('')
		data = {
		"servico"	: servico,
		"action"	: "query_add",
		"value"		: value
	}
		client.send(bytes(json.dumps(data).encode()))
	elif "3" in buffer:
		pass
	elif "00" in buffer:
		menuDeServicos()


def acao(action):
	data = {
		"servico"	: servico,
		"action"	: action
	}
	client.send(bytes(json.dumps(data).encode()))
	while True:
						
		# now wait for data back
		recv_len = 1
		response = ""
		
		while recv_len:
				data	 = str(client.recv(4096),encoding="utf-8").rstrip()
				recv_len = len(data)
				response+= data
				
				if recv_len < 4096:
						break
		if len(response):
			print(response)
			print('entrou aqui')
		menuDeServicos()
def usage():
	print("")
	print("")
	print(colored("\t\tClient Services watcher", 'blue', 'on_white'))
	print("")
	print("")
	
	print(colored("Usage","green"), ": cwatch.py 		-> For default configs 127.0.0.1:5001")
	print(colored("Usage","green"), ": cwatch.py -t target_host -p port")
	print("")

	return

def menuDeServicos():
	global servico_msg
	global servico
	print(colored("{0}:".format(servico_msg), "blue"))
	print(colored("1) Informações","cyan") )
	print(colored("2) Agendar Inicialização","cyan") )
	print(colored("3) Parar","cyan") )
	if "SVC" in servico:
		print(colored("4)Define Querys a serem executadas","cyan") )		
	else:
		print(colored("4) Executar Agora","cyan") )
	print(colored("5) Recarregar","cyan") )	
	print(colored("00)Voltar para Menu Principal","cyan") )
	print(colored("0) Exit","cyan"))
	print('\n')
	print(colored("{}:#>".format(servico),"green"))
	buffer = input('')
	if '1' in buffer:
		acao("info")
	elif '2' in buffer:
		acao("up")
	elif '3' in buffer:
		acao("parar")
	elif '4' in buffer and not "SVC" in servico:
		acao('executar_agora')
	elif "SVC" in servico and '4' in buffer:
		query_svc()
	elif '5' in buffer:
		acao('recarregar')
	
	elif '00' in buffer:
		Menu()
	elif buffer == '0':
		client.send(bytes(buffer,"utf-8"))
		print(colored("Finalizando Conexão","red"))
		os.kill(os.getpid(),signal.SIGINT)
	else:
		menuDeServicos()

def Menu():
	global servico_msg
	global servico
	print(colored("Selecione um serviço:", "green"))
	print(colored("1) -  SMS","cyan") )
	print(colored("2) -  SVC","cyan") )
	print(colored("3) -  SDU","cyan") )
	print(colored("4) -  SRC","cyan") )
	print(colored("5) -  Reload","yellow"))
	print(colored("6) -  Stop ALL","red"))
	print(colored("0) -  Exit","cyan"))
	print('\n')
	print(colored("SERVICES:#>"))
	buffer = input('')
	if '1' in buffer:
		servico_msg = "Serviço de Envio de SMS"
		servico = 'SMS'
		menuDeServicos()
	elif '2' in buffer:
		servico_msg = "Serviço de Validação de Cadastros"
		servico = 'SVC'
		menuDeServicos()
	elif '3' in buffer:
		servico_msg = "Serviço de Atualização de Dados"
		servico = 'SDU'
		menuDeServicos()
	elif '4' in buffer:
		servico_msg = "Serviço de Recuperação de Carrinhos"
		servico = 'SRC'
		menuDeServicos()
	elif '5' in buffer:
		reload()
	elif '6' in buffer:
		stop()
	elif  buffer == '0':
		client.send(bytes(buffer,"utf-8"))
		print(colored("Finalizando Conexão","red"))
		os.kill(os.getpid(),signal.SIGINT)
	else:
		Menu()

def exit_gracefully(signum, frame):
	lock_= threading.Lock()
	signal.signal(signal.SIGINT, original_sigint)
	try:
		quest = input("\nReally quit? (y/n)> ").lower().startswith('y')
		if quest:
			client.send(bytes("exit",'utf-8'))
			# teardown the connection
			client.close()
			sys.exit('Encerrando Cliente...')
			
	except KeyboardInterrupt:
		print("Ok ok, Encerrando Cliente...")
		client.send(bytes("exit",'utf-8'))
		# teardown the connection
		client.close()
		sys.exit(1)
	except Exception as e:
		client.send(bytes("exit",'utf-8'))
		# teardown the connection
		client.close()
		sys.exit('Encerrando Cliente...')

	# restore the exit gracefully handler here    
	signal.signal(signal.SIGINT, exit_gracefully)

def main():
		
		global port
		
		
		global target

		if not len(sys.argv[1:]):
			pass	
		else:		
		# read the commandline options
			try:
					opts, args = getopt.getopt(sys.argv[1:],"h:t:p:i:",["help","target","port"])
			except getopt.GetoptError as err:
					print (str(err))
					usage()
					
					
			for o,a in opts:
					
					if o in ("-h","--help"):
							usage()
					elif o in ("-t", "--target"):
							target = a
					elif o in ("-p", "--port"):
							port = int(a)
					else:
							assert False,"Unhandled Option"  
		usage()
		print("")
		print("")
		# read in the buffer from the commandline
		# this will block, so send CTRL-D if not sending input
		# to stdin
		print(colored("Ctrl+D para iniciar...","yellow"))
		buffer = sys.stdin.read()
		
		# send data off
		client_sender(buffer)   

		# we are going to listen and potentially 
		# upload things, execute commands and drop a shell back
		# depending on our command line options above

original_sigint = signal.getsignal(signal.SIGINT)
signal.signal(signal.SIGINT, exit_gracefully)
main()