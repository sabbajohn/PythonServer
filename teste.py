#!/usr/bin/python3
# coding= utf-8


class Controle(object):

	
	def __init__(self):
		
		self.Key = Key()
		self.DB = DB()
		
		
		self.API= API()
	
		self.LINK = LINK()
		self.logs=logs()
		self.files=files()
		"""self.modulos(self) """

	
class Key(Controle):

	def __init__(self):
	
		self.env =("KEY","env")
		self.root=("KEY","root")
		self.user=("KEY","user")
		
		
class DB(Controle):

	def __init__(self):
		self.MSQL_R = self.MSQL_R()
		self.MSQL_W = self.MSQL_W()
	class MSQL_R:
		
		
		host=("MSQL_R","host")
		user=("MSQL_R","user")
		passwd=("MSQL_R","passwd")
		database=("MSQL_R","database")
		raise_on_warnings=("MSQL_R","raise_on_warnings")
		
			
					
	class MSQL_W:
			host=("MSQL_W","host")
			user=("MSQL_W","user")
			passwd=("MSQL_W","passwd")
			database=("MSQL_W","database")
			raise_on_warnings=("MSQL_W","raise_on_warnings")
	
class API(Controle):
	def __init__(self):
		self.mandril = self.mandrill()
		self.hubd = self.hubd()
		self.soa = self.soa()
		self.comtele = self.comtele()
		
	class mandrill:
		
			api_key=("MANDRILL","api_key")
	
	class hubd:
		
			url=("HUBD","url")
			api_key=("HUBD","api_key")
	
	class soa:
		
			url=("SOA","url")
			user=("SOA","user")
			key=("SOA","key")
		
	class comtele:
		
			api_key=("COMTELE","api_key")
		
class LINK(Controle):
	def __init__(self):
		self.link_site=("LINKS","link_site")
		self.link_de_compra=("LINKS","link_de_compra")
		self.contact_mail=("LINKS","contact_mail")
		
	
class logs(Controle):

	def __init__(self):	
		self.manager_log=("LOGS","manager_log")
		self.sdu_log=("LOGS","sdu_log")
		self.svc_log=("LOGS","svc_log")
		self.sms_log=("LOGS","sms_log")
		self.api_log=("LOGS","api_log")
		self.startup_log=("LOGS","startup_log")
		self.watch_log=("LOGS","watch_log")
	
class files(Controle):
	def __init__(self):
		self.query=("FILES","query")
		self.responses=("FILES","responses")
		self.responses_api=("FILES","responses_api")
		self.responses_sms=("FILES","responses_sms")

class modulos(Controle):
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
				delay				=float(("SVC","delay"))
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
				delay				= float(("SRC","delay"))
				keepAlive			= True
				lasttimerunning		=None
				nextrun				=None
				firstTime			=True
				stop				=False

 

controle = Controle()
print(controle)
		