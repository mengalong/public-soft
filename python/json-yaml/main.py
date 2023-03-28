#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import yaml
import sys

def load_yaml(filename):
    data = None
    with open(filename, "r", encoding="utf-8") as fp:
        data = yaml.load(fp, Loader=yaml.CLoader)
    return data

def write_yaml(filename, data):
    with open(filename, "w", encoding="utf-8") as fp:
        yaml.dump(data, fp, allow_unicode=True)

def load_json(filename):
    data = None
    with open(filename, "r", encoding="utf-8") as fp:
        data = json.load(fp)
    return data

#separators参数用于指定分隔符的字符串，包括键和值之间的分隔符以及不同键值对之间的分隔符
#默认情况下，这些分隔符是逗号和冒号。指定一个空字符串将禁用所有分隔符，
#这将生成一个紧凑的JSON文件，而不是一个易于阅读的JSON文件。
def print_json_obj(data):
    #print(json.dumps(data, sort_keys=True, indent=4, separators=(',',":")))
    print(json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False, separators=(',',":")))

def write_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, sort_keys=True, ensure_ascii=False, indent=4, separators=(',',":"))

def test_it():
	s_json = "data/s.json"
	d_json = "data/d.json"
	s_yaml = "data/s.yaml"
	d_yaml = "data/d.yaml"
	json_obj = load_json(s_json)
	print("age:%s name:%s" % (json_obj["age"], json_obj["name"]))

	json_obj["age"] = 90
	write_json(d_json, json_obj)

	yaml_obj = load_yaml(s_yaml)

	print("package:%s category:%s" % ("p1", yaml_obj["packages"]["p1"]["category"]))
	yaml_obj["packages"]["p1"]["category"] = "new-modify"
	write_yaml(d_yaml, yaml_obj)


	print("============== new json ===============")
	json_obj_new = load_json(d_json)
	print_json_obj(json_obj_new)

	print("============= new yaml ===============")
	yaml_obj_new = load_yaml(d_yaml)
	print_json_obj(yaml_obj_new)

def main():
	test_it()

if __name__ == "__main__":
    main()
