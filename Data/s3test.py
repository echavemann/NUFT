import boto3

KEY = ''
SECRET = ''

s3 = boto3.resource('s3')
for bucket in s3.buckets.all():
    print(bucket.name)

bucket = s3.bucket('nuft')

    
