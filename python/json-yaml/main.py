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
    with open(filename, "r") as fp:
        data = json.load(fp)
    return data

def json_print(data):
    print(json.dumps(data, sort_keys=True, indent=4, separators=(',',":")))

def json_write(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, sort_keys=True, indent=4, separators=(',',":"))
        #json.dump(data, f)

def main():
    pass

if __name__ == "__main__":
    main()
