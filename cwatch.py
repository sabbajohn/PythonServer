#!/usr/bin/python3
# coding: utf-8

import sys
import socket
import getopt
import threading
import subprocess
import json
from termcolor import colored	


# define some global variables
command			= True
target			 = ""
upload_destination = ""
port			   = 0

# this runs a command and returns the output

def run_command(command):
		
		# trim the newline
		command = command.rstrip()
		
		# run the command and get the output back
		try:
				output = subprocess.check_output(command,stderr=subprocess.STDOUT, shell=True)
		except:
				output = "Failed to execute command.\r\n"
		
		# send the output back to the client
		return output

# if we don't listen we are a client....make it so.
def client_sender(buffer):
		global target
		global port

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
								data	 = str(client.recv(4096),encoding="utf-8")
								recv_len = len(data)
								response+= data
								
								if recv_len < 4096:
										break
						
						if "help" in response :
							usage(),
							continue
							# wait for more input
						else:
							if "status" in response:
								response=response.strip("<>() \n SERVICES:#").replace('\'', '\"')
								resp = json.loads(response)
								print (resp)
							#TODO: Organizar saida dos dados a partir do  json!!!
							print(response)

						buffer = input("")
						buffer += "\n"
						client.send(bytes(buffer,"utf-8"))
							
						
					
						

						

				except not EOFError:
					print(sys.exc_info())
					# just catch generic errors - you can do your homework to beef this up
					client.send(bytes("exit",'utf-8'))
					print(colored("[*] Exception! Exiting.", "red"))
					# teardown the connection
					client.close()
					return
			
					
				else:
					client.send(bytes("exit",'utf-8'))
		except:
			print(colored("Não foi possivel conectar","red"))
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
main()