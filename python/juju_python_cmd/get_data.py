import pymongo
import re
import json
import sys

#app_name = sys.argv[1]
if len(sys.argv)>1:
	app_name = sys.argv[1]
else:
	app_name = "zookeeper"

def load_json(filename):
    data = None
    with open(filename, "r") as fp:
        data = json.load(fp)
    return data

def json_print(data):
    print(json.dumps(data, sort_keys=True, indent=4, separators=(',',":")))

class MyDatabase :
	def __init__(self, config):
		self.database_config = config.get('database')
	

	def print_config(self):
		print("username:%s" %  self.username)
		print("password:%s" % self.password)
		print("hostname:%s" % self.hostname)
		print("port:%s" %  self.port)

	def connect(self):
		#create a connection  with mongoClient
		client = pymongo.MongoClient(self.database_config["url"], tls=True,
									connectTimeoutMS=self.database_config["timeout"],
									username=self.database_config["username"],
									password=self.database_config["password"],
									tlsAllowInvalidCertificates=True,
									tlsCertificateKeyFile=self.database_config["serverPem"])
		self.db_conn = client.acpoc


class GetStatus:
	def __init__(self, db_obj):
		self.db_conn = db_obj.db_conn
		self.collections = {}
		self.collections["applications"] = self.db_conn.applications
		self.collections["units"] = self.db_conn.units
		self.collections["machines"] = self.db_conn.machines
		self.collections["statuses"] = self.db_conn.statuses

	def get_statuses(self):
		collection = self.db_conn.statuses
		
		pattern_str = "#%s" % app_name
		pattern = re.compile(pattern_str, re.IGNORECASE)
		datas = collection.find({"_id":{"$regex":pattern}})
		for item in datas:
			print(item)

	def get_machines(self):
		collection = self.db_conn.machines
		datas = collection.find().limit(10)
		for item in datas:
			#print(item)
			json_print(item)

	def get_units(self):
		collection = self.db_conn.units
		datas = collection.find({"application" : app_name})
		for item in datas:
			json_print(item)

	def get_applications(self):
		collection = self.db_conn.applications
		datas = collection.find({"name":app_name})
		for item in datas:
			print(item)
			print(item["_id"])
			print(type(item))
			#print(json.loads(item))
			#json_print(item)
	
	def get_application(self, app_name):
		datas = {
			"app":"",
			"machines":{},
			"status":{},
			"units":{},
			"model-uuid":""
		}
		# app info
		appdatas = self.collections["applications"].find({"name":app_name})
		for item in appdatas:
			datas["app"] = item
			datas["model-uuid"] = item["model-uuid"]

		# unit info
		units = self.collections["units"].find({"application" : app_name})
		for item in units:
			datas["units"][item["name"]] = item

		# machine info
		#pattern_str = ":"
		#pattern = re.compile(pattern_str, re.IGNORECASE)
		#machines = self.collections["machines"].find({"_id":{"$regex": pattern}})
		machines = self.collections["machines"].find()
		for item in machines:
			key_item = "id-%s" % item["machineid"]
			datas["machines"][key_item] = item
		
		# status info
		pattern_str = "a#%s|u#%s/" % (app_name, app_name)
		pattern = re.compile(pattern_str, re.IGNORECASE)
		statuses = self.collections["statuses"].find({"_id":{"$regex":pattern}})
		for item in statuses:
			datas["status"][item["_id"]] = item

	
		#json_print(datas["status"])
		#json_print(datas["machines"])
		#json_print(datas["units"])
		#print(datas["app"])
		self.gen_datas(datas)	
		#print(len(datas["machines"].keys()))
		#json_print(datas["machines"]["id-99"])
		# status info
	
	def gen_datas(self, datas):
		versions = []
		out_data = []
		for unit_name, unit_info in datas["units"].items():
			status_charm_key = "%s:u#%s#charm" % (datas["model-uuid"], unit_name)
			agent_status = datas["status"][status_charm_key]["status"]
			agent_info = datas["status"][status_charm_key]["statusinfo"]
			
			status_task_key = "%s:u#%s" % (datas["model-uuid"], unit_name)
			task_status = datas["status"][status_task_key]["status"]

			workload_key = "%s:u#%s#charm#sat#workload-version" % (datas["model-uuid"], unit_name)
			versions.append(datas['status'][workload_key]["statusinfo"])
			
			machine_id = unit_info["machineid"]
			machine_key = "id-%s" % machine_id
			machine_ip = datas["machines"][machine_key]["addresses"][0]["value"]

			out_data.append("%-10s\t%-10s\t%-10s\t%-10s\t%-10s\t%-10s" % (unit_name, agent_status, 
								task_status, machine_id, machine_ip, agent_info))
		
		versions.sort()
		app_version = versions[0]
		app_info = "%-10s\t%-10s\t%-10s\t%-5s\t%-10s\t%-10s\t%-5s\t%-10s" % (app_name, app_version, 
								"NULL-status",datas["app"]["unitcount"], "NULL-package-name", 
								"NULL-local", datas["app"]["charmmodifiedversion"], datas["app"]["series"])
		print(app_info)
		for item in out_data:
			print(item)

	def print_data_info(self, datas):
		
		print("%-10s\t%-10s\t%-10s\t%-5s\t%-10s\t%-10s\t%-5s\t%-10s" % (app_name, "NULL-version", 
								"NULL-status",datas["app"]["unitcount"], "NULL-package-name", 
								"NULL-local", datas["app"]["charmmodifiedversion"], datas["app"]["series"]))
		versions = []
		for unit_name, unit_info in datas["units"].items():
			status_charm_key = "%s:u#%s#charm" % (datas["model-uuid"], unit_name)
			agent_status = datas["status"][status_charm_key]["status"]
			agent_info = datas["status"][status_charm_key]["statusinfo"]
			
			status_task_key = "%s:u#%s" % (datas["model-uuid"], unit_name)
			task_status = datas["status"][status_task_key]["status"]

			workload_key = "%s:u#%s#charm#sat#workload-version" % (datas["model-uuid"], unit_name)
			versions.append(datas['status'][workload_key]["statusinfo"])
			
			machine_id = unit_info["machineid"]
			machine_key = "id-%s" % machine_id
			machine_ip = datas["machines"][machine_key]["addresses"][0]["value"]

			print("%-10s\t%-10s\t%-10s\t%-10s\t%-10s\t%-10s" % (unit_name, agent_status, 
						task_status, machine_id, machine_ip, agent_info))
		versions.sort()
		app_version = versions[0]
		print(app_version)
			

# user params
db_config = {
	"database": {
		"url":"localhost:17017",
		"username":"admin",
		"password":"password-for-mongo",
		"hostname":"localhost",
		"port": 17017,
		"serverPem":"keys/server.pem",
		"timeout" : 20000
	}
}

db_obj = MyDatabase(db_config)
db_obj.connect()
status_obj = GetStatus(db_obj)

'''
print("========== statuses")
status_obj.get_statuses()
print("========= machines")
status_obj.get_machines()
print("========= units")
status_obj.get_units()
print("======== applications")
status_obj.get_applications()
'''

status_obj.get_application(app_name)


