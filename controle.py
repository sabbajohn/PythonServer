#!/usr/bin/python3
# coding= utf-8


class Controle(object):
	def __init__(self,I):
		self.Config =I.Config
		self.Config_ENV = I.Config_ENV
		
		self.Key = Key(self)
		self.DB = DB(self)
		self.API= API(self)
		self.LINK = LINK(self)
		self.logs=logs(self)
		self.files=files(self)
		self.modulos = modulos(self)
 
	
class Key(Controle):

	def __init__(self,Controle):
		
		
	
		
		self.env  =Controle.Config.get("KEY","env")
		self.root =Controle.Config.get("KEY","root")
		self.user =Controle.Config.get("KEY","user")
		
		
class DB(Controle):

	def __init__(self,Controle):
		

		self.MYSQL_R = self.MYSQL_R(Controle)
		self.MYSQL_W = self.MYSQL_W(Controle)
	class MYSQL_R(object):
		
		def __init__(self,Controle):
		
		 
			self.host=Controle.Config_ENV.get("MYSQL_R","host")
			self.user=Controle.Config_ENV.get("MYSQL_R","user")
			self.passwd=Controle.Config_ENV.get("MYSQL_R","passwd")
			self.database=Controle.Config_ENV.get("MYSQL_R","database")
			self.raise_on_warnings=Controle.Config_ENV.get("MYSQL_R","raise_on_warnings")
		
			
					
	class MYSQL_W(object):
		def __init__(self,Controle):
			
			self.host=Controle.Config_ENV.get("MYSQL_W","host")
			self.user=Controle.Config_ENV.get("MYSQL_W","user")
			self.passwd=Controle.Config_ENV.get("MYSQL_W","passwd")
			self.database=Controle.Config_ENV.get("MYSQL_W","database")
			self.raise_on_warnings=Controle.Config_ENV.get("MYSQL_W","raise_on_warnings")
	
class API(Controle):
	def __init__(self,Controle):
	
		
		self.mandril = self.mandrill(Controle)
		self.hubd = self.hubd(Controle)
		self.soa = self.soa(Controle)
		self.comtele = self.comtele(Controle)
		self.viacep = self.viacep(Controle)
	
			

	
	class viacep:
		def __init__(self,Controle):
			self.tag="VIACEP"
			self.consultas = int(Controle.Config_ENV.get(self.tag,"consultas"))
	
	class comtele:
		def __init__(self,Controle):
			self.tag="COMTELE"
			self.api_key=Controle.Config_ENV.get(self.tag,"api_key")
			self.enviados=Controle.Config_ENV.get(self.tag,"enviados")
		
			
	class mandrill:
		def __init__(self,Controle):
			self.tag="MANDRILL"
			self.api_key=Controle.Config_ENV.get(self.tag,"api_key")
			self.enviados=Controle.Config_ENV.get(self.tag,"enviados")
		
	class hubd:
		def __init__(self,Controle):
				self.tag="HUBD"
				self.url=Controle.Config_ENV.get(self.tag,"url")
				self.api_key=Controle.Config_ENV.get(self.tag,"api_key")
				self.consultas = int(Controle.Config_ENV.get(self.tag,"consultas"))
	class soa:
		def __init__(self,Controle):
			self.tag="SOA"
			self.url=Controle.Config_ENV.get(self.tag,"url")
			self.user=Controle.Config_ENV.get(self.tag,"user")
			self.key=Controle.Config_ENV.get(self.tag,"key")
			self.consultas = int(Controle.Config_ENV.get(self.tag,"consultas"))
	
		#TODO: Adicionar watch
	

	

class LINK(Controle):
	def __init__(self,Controle):
	
		self.link_site=Controle.Config_ENV.get("LINK","link_site")
		self.link_de_compra=Controle.Config_ENV.get("LINK","link_de_compra")
		self.contact_mail=Controle.Config_ENV.get("LINK","contact_mail")
			
		
	
class logs(Controle):

	def __init__(self,Controle):

		self.manager_log=Controle.Config.get("LOGS","manager_log")
		self.sdu_log=Controle.Config.get("LOGS","sdu_log")
		self.svc_log=Controle.Config.get("LOGS","svc_log")
		self.sms_log=Controle.Config.get("LOGS","sms_log")
		self.api_log=Controle.Config.get("LOGS","api_log")
		self.startup_log=Controle.Config.get("LOGS","startup_log")
		self.watch_log=Controle.Config.get("LOGS","watch_log")
	
class files(Controle):
	def __init__(self,Controle):

		self.query=Controle.Config.get("FILES","query")
		self.responses=Controle.Config.get("FILES","responses")
		self.responses_api=Controle.Config.get("FILES","responses_api")
		self.responses_sms=Controle.Config.get("FILES","responses_sms")

class modulos(Controle):
	def __init__(self,Controle):

		self.SMS = self.SMS(Controle)
		self.SVC = self.SVC(Controle)
		self.SDU = self.SDU(Controle)
		self.SRC = self.SRC(Controle)

	class SMS:
		def __init__(self,Controle):
		  
				
			self.init				= Controle.Config.getboolean("SMS","sms_init")
			self.init_time			=None
			self.delay				=None
			self.keepAlive			= True
			self.lasttimerunning	=None
			self.nextrun			=None
			self.firstTime			=True
			self.stop				=False
			
	class SVC:
		def __init__(self,Controle):
		
			self.init= Controle.Config.getboolean("SVC","svc_init")
			self.init_time			=None
			self.delay				=float(Controle.Config.get("SVC","delay"))
			self.keepAlive			= True
			self.lasttimerunning	=None
			self.nextrun			=None
			self.firstTime			=True
			self.stop				=False
			self.query 				= Controle.Config.get("SVC",Controle.Config.get("SVC", "set")) 	
			
	
	class SDU:
			
		def __init__(self,Controle):
			self.init= Controle.Config.getboolean("SDU","sdu_init")
			self.init_time			=None
			self.delay				=None
			self.keepAlive			= True
			self.lasttimerunning	=None
			self.nextrun			=None
			self.firstTime			=True
			self.stop				=False
			
	class SRC:
		
		def __init__(self,Controle):
			self.init				= Controle.Config.getboolean("SRC","src_init")
			self.init_time			= None
			self.delay				= float(Controle.Config.get("SRC","delay"))
			self.keepAlive			= True
			self.lasttimerunning	=None
			self.nextrun			=None
			self.firstTime			=True
			self.stop				=False
			self.querys				= Controle.Config.get("SRC","query")

 
