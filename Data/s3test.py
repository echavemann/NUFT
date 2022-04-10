
import boto3
import os
import time
import shutil

KEY = ''
SECRET = ''

client = boto3.client('s3',
                      aws_access_key_id=KEY,
                      aws_secret_access_key=SECRET)

def upload(name, bucket):
    client.upload_file(name, bucket, name)

def download(name, bucket,new_name):
    client.download_file(bucket, name, new_name)
    
def downsync(source, bucket):
    download(source, bucket, 'temp')
    shutil.copyfile('temp', source)
    os.remove('temp')

def upsync(source, bucket):
    download(source, bucket, 'temp')
    upload(source, bucket)
