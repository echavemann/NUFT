import time
import datetime
import boto3
import os
import time
import shutil
import yaml
#aws globals

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

#Enables all AWS functions 
def activate_aws(config_file):
    [KEY,SECRET] = get_keys(config_file, 'twitter', ['api_key', 'secret_key'])
    client = boto3.client('s3',
                      aws_access_key_id=KEY,
                      aws_secret_access_key=SECRET)
    return client

#Add this line to your program:

#[KEY,SECRET] = activate_aws('config.yaml')


#uploads the file in path with name name to bucket bucket
def upload(client,name, bucket):
    client.upload_file(name, bucket, name)

#Downloads the file named name from bucket bucket to an entry in folder named new_name
def download(client, name, bucket,new_name):
    client.download_file(bucket, name, new_name)

#Downloads a file and syncs your local file with it. Names must be the same. 
def downsync(client,source, bucket):
    download(client,source, bucket, 'temp')
    shutil.copyfile('temp', source)
    os.remove('temp')
#Syncs cloud file with local file of the same name. Stores the file as 'log' so you can see what you overwrote.
def upsync(client,source, bucket):
    download(client,source, bucket, 'log')
    upload(client,source, bucket)
#Call this function in your loop to store backups of the dynamic data which are named their timestamps.
def store(client,name, bucket):
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    timern = str(datetime.date.today()) +' ' + str(current_time)
    download(client,name, bucket, timern)
    upload(client,timern, bucket)
    os.remove(timern)
