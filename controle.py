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
		self.servicos = servicos(self)
	""" TODO:
		! Concluir metodo get/set das variaveis de controle assim como escrita dela no arquivo de configuração
	 """
	def setControle(self,*args, **kwargst):
		by_module = False
		by_struct = False
		modulo_list={
			"KEY":('env', 'root', 'user'),
			"BD":{ 
				"MYSQL_W":("host","user","passwd","database","raise_on_warnings"), 
				"MYSQL_R":("host","user","passwd","database","raise_on_warnings")
			}, 
			"API":{
				"viacep":("consultas"),
				"mandrill":('api_key',"enviados"),
				"comtele":('api_key',"enviados"),
				"soa":("url","user", "passwd", "consultas"),
				"hubd":("url", "api_key", "consultas")
			},
			"LINK":("link_site","link_de_compra","contact_mail"),
			"logs":("manager_log","sdu_log","svc_log","sms_log","api_log","startup_log","watch_log"), 
			"files":("query","responses","responses_api","responses_sms"),	
			"logs":("manager_log","sdu_log","svc_log","sms_log","api_log","startup_log","watch_log"), 

			"servicos":{
				"WATCH":("adress","port"),
				"SMS":("init","init_time","delay","keepAlive","lasttimerunning","nextrun","first_time","stop"),
				"SVC":("init","init_time","delay","keepAlive","lasttimerunning","nextrun","first_time","stop","query"),
				"SDU":("init","init_time","delay","keepAlive","lasttimerunning","nextrun","first_time","stop"),
				"SRC":("init","init_time","delay","keepAlive","lasttimerunning","nextrun","first_time","stop","query"),

				}
			}
		try:
			modulo = kwargst.get('modulo')
			try:
				atributo =kwargst.get('atributo')
				valor =kwargst.get('valor')
			except:
				raise Exception("É preciso definir atributo e valor a ser modificado!")
			return
			try:
				submodulo = kwargst.get('submodulo')
			except:
				submodulo = False
			by_module = True
		except:
			try:
				struct = kwargst.get('dict_items')
				by_struct = True
			except:
				raise Exception("Parametros invalidos")
				return
		
		if by_struct:
			keys = [x for x in struct for y in modulo_list if x==y]

			for module in keys:
				if "bd" in module:
					pass
				if "api" in module:
					submodulo = [x for x in struct[module]]
					if "viacep" in submodulo:
						self.API.viacep.consultas = struct[module]['consultas']

					if "mandrill" in submodulo:
						pass
					if "comtele" in submodulo:
						pass
					if "soa" in submodulo:
						pass
					if "hubd" in submodulo:
						pass
					
					pass
				if "servicos" in module: 
					pass

 
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
	
		
		self.mandrill = self.mandrill(Controle)
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

class servicos(Controle):
	def __init__(self,Controle):

		self.SMS = self.SMS(Controle)
		self.SVC = self.SVC(Controle)
		self.SDU = self.SDU(Controle)
		self.SRC = self.SRC(Controle)

	class WATCH:
		def __init__(self,Controle):
			self.addr				=  Controle.Config.get("WATCH","addr")
			self.port				=  int(Controle.Config.get("WATCH","port"))
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
	

 
