import time
import datetime
import boto3
import os
import time
import shutil

#aws globals
KEY = ''
SECRET = ''

#aws client creation using boto3
client = boto3.client('s3',
                      aws_access_key_id=KEY,
                      aws_secret_access_key=SECRET)


#uploads the file in path with name name to bucket bucket
def upload(name, bucket):
    client.upload_file(name, bucket, name)

#Downloads the file named name from bucket bucket to an entry in folder named new_name
def download(name, bucket,new_name):
    client.download_file(bucket, name, new_name)

#Downloads a file and syncs your local file with it. Names must be the same. 
def downsync(source, bucket):
    download(source, bucket, 'temp')
    shutil.copyfile('temp', source)
    os.remove('temp')
#Syncs cloud file with local file of the same name. Stores the file as 'log' so you can see what you overwrote.
def upsync(source, bucket):
    download(source, bucket, 'log')
    upload(source, bucket)
#Call this function in your loop to store backups of the dynamic data which are named their timestamps.
def store(name, bucket):
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    timern = str(datetime.date.today()) +' ' + str(current_time)
    download(name, bucket, timern)
    upload(timern, bucket)
    os.remove(timern)
