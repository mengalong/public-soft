#!/usr/bin/env python
#coding=gbk
import json
import os,sys
import traceback
import logging
import optparse
import mydatabase

#create the log instance
def create_log_instance(log_path, logfile):
	#create loghandler
	log = logging.getLogger()

	if not os.path.exists(log_path):
		os.makedirs(log_path)
	if not os.path.exists(logfile):
		fl = file(logfile,"w")
		fl.close()
	try :
		loghandler = logging.FileHandler(logfile)
		fmt = logging.Formatter(u'%(levelname)-8s %(asctime)s %(filename)s LINE:%(lineno)d PID:%(process)d THD:%(thread)d : %(message)s',u'%Y-%m-%d %H:%M:%S')
		loghandler.setFormatter(fmt)
		log.addHandler(loghandler)
		log.setLevel(logging.NOTSET)
	except Exception, err:
		print "Error: create log handler:%s" % (err)
		traceback.print_exc()
		return 1
	return log

#parser the argv
def parser_arg(argv,log):
	try:
		usage = "Usage: %prog <OBJECT> <ACTION> [options]\n\t%prog <OBJECT> <ACTION> --help"
		parser = optparse.OptionParser(usage, version="%prog 1.0")
		parser.add_option("--id",  dest="id", help="id", metavar="ID")
		parser.add_option("--key", dest="key", help="the key", metavar="KEY")
		parser.add_option("--value", dest="value", help="the value", metavar="VALUE")
		parser.add_option("--data",  dest="data", help="data", metavar="DATA")
		parser.add_option("--cluster", dest="cluster", help="cluster id", metavar="CLUSTER")
		parser.add_option("--pretty","-p", action="store_true", dest="pretty", help="print json pretty", metavar="VALUE")
		
		(options, args) = parser.parse_args()
		options.obj = argv[0]
		options.action = argv[1]
	except Exception,err:
		print "Error in parser_arg:%s" % (err)
		str = traceback.format_exc()
		log.critical(str)
		return 1
	return options

def print_usage(common_config):
	print "Usage: %s <object> <action> [options]" % (sys.argv[0])
	print
	print "Valid object:"
	for obj in common_config["para"]["support_obj"]:
		print "\t" + obj
	print "Valid action:"
	for action in common_config["para"]["support_action"]:
		print "\t" + action
def print_usage_detail_object(obj,action,common_config):
	opt=""
	for tmp_action in common_config["para"]["valid_action_para"][action]:
		opt = opt + " --" + tmp_action + "=" + tmp_action
	opt = opt + " [-p/--pretty]"
	print "Usage:%s %s %s %s" % (sys.argv[0], obj, action, opt)
	
#check if the para is valid
def check_para(para,conf_all):
	#check obj
	if para.obj not in conf_all["para"]["support_obj"]:
		print "unspport obj:" + para.obj
		print_usage(conf_all)
		return 1
	#check action
	if para.action not in conf_all["para"]["support_action"]:
		print "unsupport action:" + para.action
		print_usage(conf_all)
		return 1

	#check action param
	#print conf_all["para"]["valid_action_para"][para.action]
	#print type(para)
	#print getattr(para, "key")
	for param in conf_all["para"]["valid_action_para"][para.action]:
		if param == "" :
			continue
		if hasattr(para,param) and getattr(para, param) != None:
			continue
		else:
			print "miss option: \"--" + param + "\""
			print_usage_detail_object(para.obj, para.action,conf_all)
			return 1
	return 0

def get_json_conf(file_name="NULL"):
	try:
		tmp_conf_fh = open(file_name, "r")
	#	json_obj = json.load(tmp_conf_fh)
		tmp_str = tmp_conf_fh.read()
		tmp_str = json.dumps(eval(tmp_str))
		json_obj = json.loads(tmp_str)
	except Exception, err:
		print "Error in %s:%s" % (__file__, err)
		traceback.print_exc()
		return(1)
	tmp_conf_fh.close()
	return json_obj

def is_valid_json(str):
	try:
		data = json.loads(str, encoding="gbk")
	except Exception,err:
		return 1
	return 0

def is_key_in_dict(key,dictobj):
	if key in dictobj:
		return 0
	else:
		return 1

def json_print_string(jsonstr):
	if is_key_in_dict("_id", jsonstr) == 0:
		del jsonstr["_id"]
	ss = json.dumps(jsonstr,encoding="gbk",ensure_ascii=False)
	print ss.encode("gbk")

def json_print_pretty(jsonstr):
	if is_key_in_dict("_id", jsonstr) == 0:
		del jsonstr["_id"]
	ss = json.dumps(jsonstr,encoding="gbk",ensure_ascii=False,sort_keys=True,indent=4)
	print ss.encode("gbk")

#字符串转换成json串，考虑编码
def json_dump(jsonstr):
	str = json.dumps(jsonstr, encoding="gbk", ensure_ascii=False)
	return str

#json 字符串转换成json对象
def json_load(jsonstr):
	obj = json.loads(jsonstr)
	data = eval(obj.encode("utf8"))
	return data
