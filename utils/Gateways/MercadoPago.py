#!/usr/bin/python3
# coding: utf-8
import sys
import os
from datetime import datetime
import json
import requests
import random
from utils import funcoes
from datetime import timedelta  

class MercadoPago(object):
    def __init__(self, M):
		try:
			self.Manager
		except NameError:
			self.Manager 			= M
			self.database 			= self.Manager.database