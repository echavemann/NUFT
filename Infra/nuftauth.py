import time
import datetime
#import boto3
import os
import time
import shutil
import yaml

#Just use this one function to get keys from config file.
#FILE MUST BE YAML
def get_keys(config_file, service, keys):
    with open(config_file, 'r') as stream:
        cfg = yaml.safe_load(stream)
    cfg = cfg[service]
    ret = []
    for key in (keys):
        if key not in cfg.keys():
            raise Exception('Missing key: ' + key)
        ret.append(cfg[key])
    return ret
