#!/usr/bin/env python
import ConfigParser
import traceback

class myconfig :
	def __init__(self,conf_file):
		config = ConfigParser.ConfigParser()
		try:
			config.read(conf_file)
			self.return_value = 0
		except Exception,err:
			print "get conf file failed"
			traceback.print_exc()
			self.return_value = 1
		self.config_obj = config

	def print_conf(self):
		for x in self.config_obj.sections() :
			for item in self.config_obj.options(x):
				print "%s.%s:%s" % (x,item,self.config_obj.get(x,item))

