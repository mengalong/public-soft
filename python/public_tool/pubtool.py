#!/usr/bin/env python
#coding=gbk
import commands
import time
import json
import os,sys
import traceback
import logging
import optparse



'''
functions: exec the cmd
args:
    retry_time : int, retry time when the cmd exec failed
    cmd : the cmd you want to exec
returns:
    {
        "return_value" : 0/other
        "return_desc" : "the output of the cmd"
    }
'''
def run_cmd(retry_time, cmd):
	retry = 0
	status = ""
	output = ""
	while retry <= retry_time:
		status,output = commands.getstatusoutput(cmd)
		if status != 0:
			time.sleep(0.5)
			retry += 1
		else:
			break
	return_obj = {
		"return_value" : status,
		"return_desc" : output
	}
	return return_obj

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

#get json conf
def get_json_conf(file_name="NULL"):
	try:
		tmp_conf_fh = open(file_name, "r")
		tmp_str = tmp_conf_fh.read()
		tmp_str = json.dumps(eval(tmp_str))
		json_obj = json.loads(tmp_str)
	except Exception, err:
		print "Error in %s:%s" % (__file__, err)
		traceback.print_exc()
		return(1)
	tmp_conf_fh.close()
	return json_obj


#
def is_key_in_dict(key,dictobj):
        if key in dictobj:
                return 0
        else:
                return 1

def get_content_from_file(file_name):
	ret_obj = {
		"return_value" : 1,
		"return_desc" : "get conf content failed.file=%s" %(file_name)
	}
	try:
		fh = open(file_name,"r")
	except Exception,err:
		print err
		return ret_obj

	str_content = fh.read()
	ret_obj["return_value"] = 0
	ret_obj["return_desc"] = str_content
	return ret_obj
