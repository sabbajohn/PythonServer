#!/usr/bin/python3
# coding: utf-8


import os
import sys
import psutil
import time
from time import sleep
import datetime
from datetime import date
import logging
import getpass
import re

import subprocess

class Startup(object):
	def __init__(self, *args, **kwargs):
		self.USER = getpass.getuser()
		
		
		self.procs = ['sms.py','server.py','servico_de_validacao.py','Databaseupdate.py']
		self.delays={'validacao':600}
		self.start_time = 0
		self.i()
	
	def i(self):

		
		while True:
			if not self.checkIfProcessRunning(self.procs[0]):
					os.system('python3 sms.py &')
				
			else:
				pass
			if not self.checkIfProcessRunning(self.procs[1]):
					os.system('uwsgi --http 10.255.237.29:5000 --wsgi-file server.py --callable app --processes 4 --threads 2 --stats 127.0.0.1:9191 &')
			
			else:
				pass
			if not self.checkIfProcessRunning(self.procs[2]):
				if self.start_time ==0:
					self.start_time = time.time()
					os.system('nohup python3 servico_de_validacao.py &')
				elif time.time()- self.start_time > self.delays['validacao']:
					self.start_time = time.time()
					os.system('nohup python3 servico_de_validacao.py &')
			else:
				pass
			if not self.checkIfProcessRunning(self.procs[3]) and not self.checkIfProcessRunning(self.procs[2]):
				
					modtime =os.path.getmtime("/home/"+self.USER+"/PythonServer/queries/query.txt")
					#modificationTime = time.strftime('%H:%M:%S', time.time(mod))
					if modtime < self.start_time:
						pass
					else:

						os.system('python3 Databaseupdate.py &')
			
			else:

				pass
			

			
		sleep(3)

	def checkIfProcessRunning(self,processName):
		'''
		Check if there is any running process that contains the given name processName.
		'''
		#Iterate over the all the running process

		ps = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE).communicate()[0]
		processes = ps.decode().split('\n')
		# this specifies the number of splits, so the splitted lines
		# will have (nfields+1) elements
		nfields = len(processes[0].split()) - 1
		
		for row in processes[1:]:
			try:
				proc = row.split(None, nfields)
				if len(proc)>0:

					# Check if process name contains the given name string.
					if processName.lower() in proc[10].lower():
						return True
				else: 
					pass
			except:
				pass
		return False 

		
	
	
Startup()
