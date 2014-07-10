#!/usr/bin/env python
#-*-coding:gbk-*-
import os,sys
import ConfigParser
import logging
import ConfigParser
import traceback
import optparse
import json

#prepare some environment
procdir = os.path.dirname(sys.argv[0])
abspath = os.path.abspath(sys.argv[0])
basedir = os.path.dirname(abspath)
libdir = basedir + "/../lib"

#add custom lib path
sys.path.append(libdir)
import mydatabase
import myconfig
import common

conf_file = basedir + "/../conf/cmapi.ini"
log_path = basedir + "/../log"
global config

if __name__ == "__main__":

	#read conf
	config_instance = myconfig.myconfig(conf_file)
	config = config_instance.config_obj
	if config_instance.return_value != 0:
		exit(1)
	#test:print the conf item and value
	#config_instance.print_conf()

	#create log handler
	logfile_name = config.get("logconf","logname")
	logfile = basedir + "/../log/%s" % (logfile_name)
	log = common.create_log_instance(log_path, logfile)

	#test: print a log
	#log.info("test!!")

	#read the common conf
	common_file = "%s/../conf/%s" % (basedir, config.get("global", "common_conf"))
	common_config = common.get_json_conf(common_file)
	if common_config == 1:
		exit(1)
	#test: print the conf obj
	#print json.dumps(common_config,indent=4)
	#print common_config["para"]["support_obj"]
	
	if len(sys.argv) < 3:
		common.print_usage(common_config)
		exit(1)

	#get para
	para = common.parser_arg(sys.argv[1:], log)
	if para == 1:
		exit(1)
	#test: print the para detail
	#print para.data


	#check param
	ret = common.check_para(para, common_config)
	if ret != 0 :
		exit(1)
	#create db instance

	#create database handler
	try :
		db = mydatabase.mydatabase(config, log, para, common_config)
	except Exception,err:
		print "Error in create database instance:%s" % (err)
		str = traceback.format_exc()
		log.critical(str)
		exit(1)

	#test: print db
	#db.print_env()

	#do the real function by action
	if para.action == "list":
		ret = db.do_list()
	elif para.action == "del":
		ret = db.do_del()
	elif para.action == "add":
		ret = db.do_add()
	elif para.action == "get-meta-all":
		ret = db.do_get_meta_all()
	elif para.action == "get-meta-attr":
		ret = db.do_get_meta_attr()
	elif para.action == "set-meta-all":
		ret = db.do_set_meta_all()
	elif para.action == "set-meta-attr":
		ret = db.do_set_meta_attr()
	else:
		print "unknow case!"
	exit(ret["return_value"])

