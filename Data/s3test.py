
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
    
def sync(source, destination, bucket):
    download(source, bucket, 'temp')
    shutil.copyfile(source, 'temp')
    upload(destination, bucket)
    os.remove('temp')
    
sync('s3test.py', 's3test.py', 'nuft')
