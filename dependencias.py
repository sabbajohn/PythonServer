#!/usr/bin/python3
# coding: utf-8
import sys
import os
import subprocess

if sys.version_info[0] < 3:
	print("[!] Versão Requerida: Python3")
	print("[!] Versão Disponivel: {0}".format(sys.version_info[0]))
	try:
		comando = os.system
		comando( 'sudo apt-get install python3')
	except :
		if IOError:	
			raise Exception("[!]Must be using Python 3, You can install it using: # apt-get install python3")
else:
	print("[OK] Versão Requerida: Python3")
	pass


try:
	print("[!] Verificando Disponibilidade PIP3 ")
	result = subprocess.check_output(['sudo pip3 -V'], stderr=subprocess.STDOUT,text=True)
	if  "pip3: not found" in result:
		print("[!] PIP3 Não esta disponivel ")
		print("[*] Tentarei instala-lo para você ")
		os.system( 'sudo apt-get install python3-pip -y') 
except:
	if IOError:	
		 os.system( 'sudo apt-get install python3-pip') 
		
try:
	result = subprocess.check_output(["pip3 install -r req.txt"], stderr=subprocess.STDOUT,text=True)
	if "Exception:" in result:
		print("[!] Erro ao instalar Pacotes")

except:
	if OSError:	
		try:
			os.system("sudo apt-get install python3-pip")
		except :
			if IOError:
				print("Não foi Possivel instalar algumas das dependencias!")

try:
	import asyncio
	
except:
	try:
		comando = os.system
		comando('sudo pip3 install asyncio\n')
		print('[!] Tentando Instalar as Dependencias\n')	
	except:
		if IOError:	
			print("[!] Please install the asyncio library: sudo pip3 install asyncio\n")
	

try:
	import aiohttp
except:
	try:
		comando = os.system
		comando('sudo pip3 install aiohttp')
		print('[!] Tentando Instalar as Dependencias\n')
	except:

		if IOError:	
			print("[!] Please install the aiohttp library: sudo pip3 install aiohttp\n")	
		
		else:  
			pass
			
try:
	import mysql.connector
	print('[OK] MYSQL Disponivel')
except:
	try:
		print('[!] Verificando MYSQL\n')
		result = subprocess.check_output(['sudo pip3 install mysql'], stderr=subprocess.STDOUT,text=True)
		if "erro code 1" in result:
			print("[!] mysql Não esta disponivel ")
			print("[*] Tentarei instala-lo para você ")
			print('[!] Tentando Instalar as Dependencias\n')
			try:
				os.system('sudo apt-get install python3-mysql -y')
			except:
				if IOError:
					print("[!] Please install the mysql library: sudo pip3 install mysql\n")
				else:
					pass
	
	except:
		print("[!] Please install the mysql library: sudo pip3 install mysql\n")


try:
	from aiofile import AIOFile, LineReader, Writer
except:
	try:
		
		comando = os.system
		comando('sudo pip3 install aiofile')
		print('[!] Tentando Instalar as Dependencias\n')
	except:

		if IOError:	
			print("[!] Please install the aiofile library: sudo pip3 install aiofile\n")	
try:
	from flask import Flask, request, jsonify
except:
	try:
		comando = os.system
		comando('pip3 install flask')
		print('[!] Tentando Instalar as Dependencias\n')	
	except :
		if IOError:	
			print("[!] Please install the flask library: pip install flask\n")
		

	
	
try:
	from flask_restful import Resource, Api
except:
	try:
		comando = os.system
		comando('pip3 install flask_restful')
		print('[!] Tentando Instalar as Dependencias\n')
	except:
		if IOError:	
			print("[!] Please install the flask_restful library: pip3 install flask_restful\n")	
		
		
		
try:
	import urllib.request
except:
	try:
		comando = os.system
		comando('pip3 install urllib')
		print('[!] Tentando Instalar as Dependencias')
	except:
		if IOError:	
			print("[!] Please install the urllib library: pip3 install urllib\n")


print('[***] Concluido')