#!/usr/bin/python3
# coding: utf-8
import sys
import os
from datetime import datetime
from datetime import date
import json
import re


def soNumero(info):
	info = re.sub("[^0-9]",'',info)
	return info

def todict(obj, classkey=None):
		if isinstance(obj, dict):
			data = {}
			for (k, v) in obj.items():
				data[k] = self.todict(v, classkey)
			return data
		elif hasattr(obj, "_ast"):
			return self.todict(obj._ast())
		elif hasattr(obj, "__iter__") and not isinstance(obj, str):
			return [self.todict(v, classkey) for v in obj]
		elif hasattr(obj, "__dict__"):
			data = dict([(key, self.todict(value, classkey)) 
			for key, value in obj.__dict__.items() 
				if not callable(value) and not key.startswith('_')])
			if classkey is not None and hasattr(obj, "__class__"):
				data[classkey] = obj.__class__.__name__
			return data
		else:
			return obj

def saveGoogleLog( carrinho, response):
		weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
		today = datetime.now().weekday()
		weekday = weekDays[today]
		log = {
				"env"  : "production",
				"fn"   : "SRC-II",
				"type" : "BOLETO-SRC", 
				"cliente":{
					"sexo":carrinho['Sexo'],
					"cidade":carrinho['Cidade'],
					"uf":carrinho['SgUF'],
					"nascimento":str(carrinho[14])
				},
				"payment":{
					"payment_method_id":"BOLETO-SRC",
					"status":"approved",
					"transaction_amount":carrinho['boleto']['valor'],
					"weekday":weekday,
					
				},
				
			}
		with open("/tmp/megasorte-venda.log","a+") as f:
			l = json.dumps(log)
			f.write(l)
			f.write('\n')
		f.close
		return
def formataValor(val):
    
	return format(val, '.2f').replace(".",",")