#!/usr/bin/env python
#-*-encoding:gbk-*-
import pymongo
import string
import json
import common
import sys


class mydatabase :
	def __init__(self, config, log, para, conf_common) :
		self.username = config.get("database", "username")
		self.password = config.get("database", "password")
		self.hostname = config.get("database", "hostname")
		self.port = config.get("database", "port")
	
		self.log = log	
		#config: config.ini config.get(section,param)
		#conf_common: common.conf getattr(conf_common,"xxx")
		#para: --id xx para.action/ getattr(para,action)
		self.para = para
		self.config = config
		self.conf_common = conf_common
		if int(config.get("global","debug")) == 1:
			self.database_name = config.get("database", "database_name")
			self.collection_name = config.get("database", "collection_name")
		else :
			#if defined the cluster ,use it
			if getattr(para,"cluster") != None:
				self.database_name = getattr(para, "cluster")
			else:
				self.database_name = config.get("database", "database_name")
			self.collection_name = getattr(para, "obj")
		self.connect()

	def print_env(self):
		print "username:%s" % (self.username)
		print "password:%s" % (self.password)
		print "database_name:%s" % (self.database_name)
		print "database_collection:%s" % (self.collection_name)
	def print_list(self):
		for x in self.db_collection.find() :
			print x	
	def connect(self):
		#create a connection  with mongoClient
		db_conn = pymongo.Connection(self.hostname, 1105);
		self.db_conn = db_conn

		#Getting a database
		self.db_database = self.db_conn[self.database_name]
		self.db_collection = self.db_database[self.collection_name]

	#if exists,return 0, else return 1
	def is_exists(self,str):
		ret = self.db_collection.find(str).count()
		if ret > 0:
			return 0
		else:
			return 1
	
	#list the all info
	def do_list(self):
		#list all the instance
		for item in self.db_collection.find({},{"id":1}):
			print item["_id"]
		ret_obj = {
			"return_value":0,
			"return_desc":"list succ"
		}
		return ret_obj

	def do_del(self):
		#del the defined id
		ret = self.db_collection.remove({"_id":self.para.id})
		ret_obj = {
			"return_value":0,
			"return_desc":"list succ"
		}
		return ret_obj


	def do_add(self):
		ret_obj = {
			"return_value" : 1,
			"return_desc" : "add failed"
		}
		#add new instance
		if common.is_valid_json(self.para.data) != 0:
			loginfo = "unvalid json string: " + self.para.data
			print loginfo
			ret_obj["return_value"] = 1
			return ret_obj

		#字符串转换成dict类型
		#ss = eval(self.para.data)
		ss = self.para.data

		#处理编码
		str = common.json_dump(ss)
		data = common.json_load(str)

		data["_id"] = self.para.id;
		query = {"_id":self.para.id}
		if self.is_exists(query) == 1:
			ret = self.db_collection.insert(data)
			if ret == self.para.id:
				ret_obj["return_value"] = 0
				return ret_obj
			else:
				print "add failed"
				ret_obj["return_value"] = 1
				return ret_obj
		else:
			print "The record is exists,cannot add! id=" + data["_id"]
			ret_obj["return_value"] = 1
			return ret_obj
	#get all the meta info
	def do_get_meta_all(self):
		ret_obj = {
			"return_value" : 1,
			"return_desc" : "get-meta-all failed"
		}
		data = {"_id":self.para.id}
		if self.is_exists(data) == 1:
			loginfo = "Cannot find the record which id="+bytes(self.para.id)
			print loginfo
			self.log.info(loginfo)
			return ret_obj
		meta_string = self.db_collection.find_one(data)
		if self.para.pretty == True:
			common.json_print_pretty(meta_string)
		else:
			common.json_print_string(meta_string)

		ret_obj["return_value"] = 0
		ret_obj["return_desc"] = "get-meta-all success"
		return ret_obj
	#get meta attr
	def do_get_meta_attr(self):
		ret_obj = {
			"return_value" : 1,
			"return_desc" : "get-meta-attr failed"
		}
		query = {"_id":self.para.id}

		if self.is_exists(query) == 1:
			loginfo = "Cannot find the record which query is:" + bytes(query)
			print logfinfo
			self.log.info(loginfo)
			return ret_obj

		meta_string = self.db_collection.find_one(query)
		tmp_obj = meta_string
		#need to check if the key is exists
		for key in self.para.key.split("."):
			if common.is_key_in_dict(key, tmp_obj) != 0:
				loginfo = "the key:\"%s\" doesnot exists!" % (self.para.key)
				print loginfo
				self.log.info(loginfo)
				return ret_obj
			else:
				tmp_obj = tmp_obj[key]

		if type(tmp_obj) != dict:
			print tmp_obj
		else:
			if self.para.pretty == True:
				common.json_print_pretty(tmp_obj)
			else:
				common.json_print_string(tmp_obj)
		return ret_obj

	def do_set_meta_all(self):
		ret_obj = {
			"return_value" : 1,
			"return_desc" : "get-meta-attr failed"
		}

		#check if the data is valid json string
		if common.is_valid_json(self.para.data) != 0:
			loginfo = "The data string is unvalid json string!"
			print loginfo
			self.log.info(loginfo)
			return ret_obj

		#字符编码转换
		ss = common.json_dump(self.para.data)
		data_obj = common.json_load(ss)

		#check if _id is exists and the recored is exists
		if common.is_key_in_dict("_id", data_obj) == 0:
			loginfo = "the key _id cannot be exists in the data string"
			print loginfo
			self.log.info(loginfo)
			return ret_obj

		#override data_obj["_id"]
		data_obj["_id"] = self.para.id

		query = {"_id":self.para.id}
		if self.is_exists(query) != 0:
			loginfo = "The id \"%s\" doesnot in database" % (self.para.id)
			print loginfo
			self.log.info(loginfo)
			return ret_obj

		#这里比较危险可能，set-meta-all 的时候是先删除再insert
		self.db_collection.remove(query)
		#exec the sql
		ret = self.db_collection.insert(data_obj)
		if ret != self.para.id:
			print "update failed"
			return ret_obj
		else:
			ret_obj["return_value"] = 0
		return ret_obj
	#set-meta-attr
	def do_set_meta_attr(self):
		ret_obj = {
			"return_value" : 1,
			"return_desc" : "get-meta-attr failed"
		}

		query = {"_id":self.para.id}
		if self.is_exists(query) != 0:
			loginfo = "The id \"%s\" doesnot in database" % (self.para.id)
			print loginfo
			log.info(loginfo)
			return ret_obj
		if common.is_valid_json(self.para.value) == 0:
			ss = common.json_dump(self.para.value)
			data_obj = common.json_load(ss)
		else:
			data_obj = self.para.value
		#exec the sql
		ret = self.db_collection.update(query,{"$set":{self.para.key:data_obj}})
		ret_obj["return_value"] = 0
		ret_obj["return_desc"] = "set meta attr success"
		return ret_obj
