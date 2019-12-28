import boto3
from os import environ

BUCKET="i.ruqqus.com"

#setup AWS connection
S3=boto3.client("s3",
                aws_access_key_id=environ.get("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=environ.get("AWS_SECRET_ACCESS_KEY")
                )

def upload_file(name, file):

    S3.upload_fileobj(file,
                      Bucket=BUCKET,
                      Key=name)

def delete_file(name):

    S3.delete_object(Bucket=BUCKET,
                     Key=name)

    
