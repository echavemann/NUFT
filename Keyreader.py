import enum
import yaml


#Given string config_file pointing to the file, string service, and list of strings keys, 
#Returns a list of values for the given keys for the given service.

#Now with exceptions and better sanitizing!
def get_keys(config_file, service, keys):
    with open(config_file, 'r') as stream:
        cfg = yaml.safe_load(stream)
    cfg = cfg[service]
    cfg = cfg.split()
    for i, key in enumerate(keys):
        string = key + ':'
        t = cfg[i]
        cfg[i] = cfg[i].replace(string,'')
        if t == cfg[i]:
            raise Exception('Key not found in config file!')
        
    return cfg
