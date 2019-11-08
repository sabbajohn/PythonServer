#!/usr/bin/python3
# coding: utf-8
import sys
import os

if sys.version_info[0] < 3:
	try:
		comando = os.system
		comando( 'sudo apt-get install python3')
	except :
		if IOError:	
			raise Exception("[!]Must be using Python 3, You can install it using: # apt-get install python3")
try:
	os.system("pip3 install -r req.txt")
except:
	if IOError:	
		try:
			os.system("sudo apt-get install python3-pip")
		except :
			if IOError:
				print("Não foi Possivel instalar algumas das dependencias!")
			
	""" try:
		comando = os.system
		comando( 'sudo pip3 -V')
	except:
		if IOError:	
			comando = os.system
			comando( 'sudo apt-get install python3-pip') """
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

except:
	try:
		comando = os.system
		comando('sudo pip3 install mysql')
		print('[!] Tentando Instalar as Dependencias\n')
	except:
		if IOError:
			try:
				comando('sudo apt-get install python3-mysql\n')
			except :
				if IOError:	
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



	