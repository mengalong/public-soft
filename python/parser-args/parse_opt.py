#!/usr/bin/env python
#-*-coding:gbk-*-
import os,sys
import traceback
import optparse

class parser_arg:
	def __init__(self):
		self.name = "parser_arg"
	def do_parser(self,argv):
		try:
			usage = "Usage: %prog <OBJECT> <ACTION> [options]\n\t%prog <OBJECT> <ACTION> --help"
			parser = optparse.OptionParser(usage, version="%prog 1.0")
			parser.add_option("--id",  dest="id", help="id", metavar="ID")
			parser.add_option("--key", dest="key", help="the key", metavar="KEY")
			parser.add_option("--pretty","-p", action="store_true", dest="pretty", help="print json pretty", metavar="VALUE")
			(options, args) = parser.parse_args()
		except Exception,err:
			str = traceback.format_exc()
			print str
			return 1
		return options
				

if __name__ == "__main__":
	parser_obj = parser_arg()
	options = parser_obj.do_parser(sys.argv[1:])
	print options
