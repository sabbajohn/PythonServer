#!/usr/bin/python3
# coding: utf-8
import sys
import os
import datetime
from datetime import date
import json
import re


def soNumero(info):
	info = re.sub("[^0-9]",'',info)
	return info