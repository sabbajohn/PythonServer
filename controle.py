#!/usr/bin/python3
# coding= utf-8
from Initialize import Initialize

class Controle(Initialize):
	def __init__(self):
		
		self.Config 
		self.Config_ENV 
	
	class Key(Controle):
		def __init__(self,Controle):
			self.Controle = Controle

			env =self.Config.get("KEY","env")
			root=self.Config.get("KEY","root")
			user=self.Config.get("KEY","user")
		
		
	class DB():
		def __init__(self,Controle):
			self.Controle = Controle
		class MSQL_R:
			def __init__(self):
				host=self.Config_ENV.get("MSQL_R","host")
				user=self.Config_ENV.get("MSQL_R","user")
				passwd=self.Config_ENV.get("MSQL_R","passwd")
				database=self.Config_ENV.get("MSQL_R","database")
				raise_on_warnings=self.Config_ENV.get("MSQL_R","raise_on_warnings")
			
				
						
		class MSQL_W:
			def __init__(self):
				host=self.Config_ENV.get("MSQL_W","host")
				user=self.Config_ENV.get("MSQL_W","user")
				passwd=self.Config_ENV.get("MSQL_W","passwd")
				database=self.Config_ENV.get("MSQL_W","database")
				raise_on_warnings=self.Config_ENV.get("MSQL_W","raise_on_warnings")
			
				
				
	class API:
		def __init__(self,Controle):
			self.Controle = Controle
			
		class mandrill:
			def __init__(self):
				api_key=self.Config_ENV.get("MANDRILL","api_key")
		
		class hubd:
			def __init__(self):
				url=self.Config_ENV.get("HUBD","url")
				api_key=self.Config_ENV.get("HUBD","api_key")
		
		class soa:
			def __init__(self):
				url=self.Config_ENV.get("SOA","url")
				user=self.Config_ENV.get("SOA","user")
				key=self.Config_ENV.get("SOA","key")
			
		class comtele:
			def __init__(self):
				api_key=self.Config_ENV.get("COMTELE","api_key")
				
	
				
	class LINK:
		def __init__(self,Controle):
			self.Controle = Controle
			link_site=self.Config_ENV.get("LINKS","link_site")
			link_de_compra=self.Config_ENV.get("LINKS","link_de_compra")
			contact_mail=self.Config_ENV.get("LINKS","contact_mail")
			
		
	class logs:
		def __init__(self,Controle):
			self.Controle = Controle
			manager_log=self.Config.get("LOGS","manager_log")
			sdu_log=self.Config.get("LOGS","sdu_log")
			svc_log=self.Config.get("LOGS","svc_log")
			sms_log=self.Config.get("LOGS","sms_log")
			api_log=self.Config.get("LOGS","api_log")
			startup_log=self.Config.get("LOGS","startup_log")
			watch_log=self.Config.get("LOGS","watch_log")
		
	class files:
		def __init__(self,Controle):
			self.Controle = Controle
			query=self.Config.get("FILES","query")
			responses=self.Config.get("FILES","responses")
			responses_api=self.Config.get("FILES","responses_api")
			responses_sms=self.Config.get("FILES","responses_sms")
	
	class modulos:
		def __init__(self,Controle):
			self.Controle = Controle
			class SMS:
				def __init__(self, modulos):
					self.moulos = modulos
					init			= self.Config.getboolean("SMS","sms_init")
					init_time			=None
					delay				=None
					keepAlive			= True
					lasttimerunning		=None
					nextrun				=None
					firstTime			=True
					stop				=False
				
			class SVC:
				def __init__(self, modulos):
					self.moulos = modulos
					init= self.Config.getboolean("SVC","svc_init")
					init_time			=None
					delay				=float(self.Config.get("SVC","delay"))
					keepAlive			= True
					lasttimerunning		=None
					nextrun				=None
					firstTime			=True
					stop				=False
			
			class SDU:
				def __init__(self, modulos):
					self.moulos = modulos
					init= self.Config.getboolean("SDU","sdu_init")
					init_time			=None
					delay				=None
					keepAlive			= True
					lasttimerunning		=None
					nextrun				=None
					firstTime			=True
					stop				=False
				
			class SRC:
				def __init__(self, modulos):
					self.moulos = modulos
					init				= self.Config.getboolean("SRC","src_init")
					init_time			= None
					delay				= float(self.Config.get("SRC","delay"))
					keepAlive			= True
					lasttimerunning		=None
					nextrun				=None
					firstTime			=True
					stop				=False
			
			
		