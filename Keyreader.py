import yaml
#Github Copilot wrote this entire thing ngl.


#Given string config_file pointing to the file, string service, and list of strings keys, 
#Returns a list of values for the given keys for the given service.
def get_keys(config_file, service, keys):
    with open(config_file, 'r') as stream:
        cfg = yaml.safe_load(stream)
    cfg = cfg[service]
    return [cfg[key] for key in keys]
