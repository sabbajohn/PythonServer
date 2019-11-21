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
# this runs a command and returns the output


# if we don't listen we are a client....make it so.
def client_sender(buffer):
		global target
		global port
		global client

		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		if target == "" and not port > 0:
			target = "127.0.0.1"
			port = 5001
		try:
				# connect to our target host
				client.connect((target,port))
				# if we detect input from stdin send it 
				# if not we are going to wait for the user to punch some in
				print(colored("Connected","green"))
				try:
					if len(buffer):
						
						client.send(bytes(buffer,'utf-8'))
				
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
						
						if "help" in response :
							usage()
							client.send(bytes("\n","utf-8"))
							continue
							# wait for more input
						elif "status" in response:
						
							response=response.strip("<>() \n SERVICES:#").replace('\'', '\"')
							response = json.loads("{"+response+"}")
							if response['status']== "True":
								print(colored("status","blue"),colored(response['status'], "green"))
							else:
								print(colored("status","blue"),colored(response['status'], "red"))
							
							print(colored("init","blue"),colored(response['init'], "blue"))
							print(colored("init_time","blue"),colored(response['init_time'], "blue"))
							if response['keepAlive']== "True":
								print(colored("keepAlive","blue"),colored(response['keepAlive'], "green"))
							else:
								print(colored("keepAlive","blue"),colored(response['keepAlive'], "red"))
							
							print(colored("lasttimerunning","blue"),colored(response['lasttimerunning'], "blue"))
							print(colored("nextrun","blue"),colored(response['nextrun'], "blue"))
							print(colored("firstTime","blue"),colored(response['firstTime'], "blue"))

							if response['stop']== "True":
								print(colored("stop","blue"),colored(response['stop'], "red"))
							else:
								print(colored("stop","blue"),colored(response['stop'], "green"))

							
							client.send(bytes("\n","utf-8"))
							continue
						else:
							if response.count("SERVICES:#>") >= 2:
								response = response.strip("SERVICES:#")
							print(response , end="")
							pass
							

						buffer = input('')
						buffer += "\n"
						if 'help' in buffer:
							usage()

						elif 'exit' in buffer:
							client.send(bytes(buffer,"utf-8"))
							print(colored("Finalizando Conexão","red"))
							os.kill(os.getpid(),signal.SIGINT)
						else:
							client.send(bytes(buffer,"utf-8"))
						
					
						

						

				except EOFError:
					pass	
				
				except (ConnectionResetError,BrokenPipeError) as e:
					print(colored(type(e), "red", "on_grey"))	
					print(colored(e, "yellow"))
					print(colored("Conexão perdida!","red"))
					os.kill(os.getpid(),signal.SIGINT)
				else:
					client.send(bytes("exit",'utf-8'))
		
		except (ConnectionResetError,BrokenPipeError) as e:

			print(colored(type(e), "red", "on_grey"))	
			print(colored(e, "yellow"))
			print(colored("Não foi possivel conectar","red"))
			sys.exit()

		except Exception as e:
			print(colored(type(e), "red", "on_grey"))
			print(colored(e, "yellow"))
			print(colored("Saindo apos Erro","red"))
			sys.exit()


def usage():
	print("")
	print("")
	print(colored("\t\tClient Services watcher", 'blue', 'on_white'))
	print("")
	print("")
	
	print(colored("Usage","green"), ": cwatch.py 		-> For default configs 127.0.0.1:5001")
	print(colored("Usage","green"), ": cwatch.py -t target_host -p port")
	print("")
	print("SERVICES:")
	print(colored("   SMS","cyan"),colored(" -> ","green") ,colored("Serviço de Envio de SMS's			"),colored(" #> ","green"), "sms")
	print(colored("   SVC","cyan"), colored(" -> ","green"), colored("Serviço de Validação de Cadastros		"),colored(" #> ","green"), "svc")
	print(colored("   SDU","cyan"), colored(" -> ","green"), colored("Serviço de Atualização de Dados		"),colored(" #> ","green"), "sdu")
	print(colored("   SRC","cyan"), colored(" -> ","green"), colored("Serviço de Recuperação de Carrinhos		"),colored(" #> ","green"), "sdu")
	
	print("ACTIONS:")
	print("	mode	[up/down]		-> Inicia serviço breve/ Impede e finaliza execução de serviço")
	print("	start				-> Inicia execução do serviço imediatamente")
	print("Ex:")
	print("	#>sms				-> Retorna infomações sobre SMS")
	print("	#>sms mode down			-> Para execução do serviço SMS (stop = True ; keepAlive = False)")
	print("	#>sms mode up			-> Prepara inicialização do SMS (stop = False ; keepAlive = True)")
	print("	#>sms mode up			-> Inicializa serviço imediatamente")
	print("")
	print(colored("[!!!]CAUTION[!!!]","red", "on_grey"))
	print(colored("	[!]","red","on_grey" ), colored("A execução destes comando pode causar perda de dados! Use com sabedoria!", "red"))
	print("")
	print(colored("	#> SELFDESTROY			-> Finalizará todos os serviços Imediatamente!\n", "red"))
	return


	
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