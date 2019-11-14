#!/usr/bin/python3
# coding: utf-8

PROD = {
	"mysql_read" : {
		"host":"10.255.242.39",
		"user":"bwadmin",
		"passwd":"8bNmFLiIPhVRrM",
		"database":"megasorte",
		'raise_on_warnings': True

	},
	"mysql_write" : {
		"host":"10.255.242.21",
		"user":"bwadmin",
		"passwd":"8bNmFLiIPhVRrM",
		"database":"megasorte",
		"raise_on_warnings": True
	},
	"API":{
			"socket":"10.255.242.11:5000",
			"uwsgitop":"127.0.0.1:9191" 

		}
}

BETA = {
	"mysql_read" : {
		"host":"megasorte-homol-read.cwixh7j3qfsl.us-east-1.rds.amazonaws.com",
		"user":"bwadmin",
		"passwd":"8bNmFLiIPhVRrM",
		"database":"megasorte",
		'raise_on_warnings': True

	},
	"mysql_write" : {
		"host":"10.255.237.4",
		"user":"bwadmin",
		"passwd":"8bNmFLiIPhVRrM",
		"database":"megasorte",
		"raise_on_warnings": True
	},

	"API":{
			"socket":"10.255.237.29:5000",
			"uwsgitop":"127.0.0.1:9191" 
		}
}