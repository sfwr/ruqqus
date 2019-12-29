import boto3
from os import environ
from PIL import Image

BUCKET="i.ruqqus.com"

#setup AWS connection
S3=boto3.client("s3",
                aws_access_key_id=environ.get("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=environ.get("AWS_SECRET_ACCESS_KEY")
                )

def upload_file(name, file):
    
    image=Image.frombuffer(data=file.read())
    raw_image=list(image.getdata())
    no_exif=Image.new(image.mode, image.size)
    no_exif.putdata(raw_image)
    
    S3.upload_fileobj(no_exif,
                      Bucket=BUCKET,
                      Key=name,
                      ExtraArgs={'ACL':'public-read',
                                 "ContentType":"image/png"
                      }
                     )

def delete_file(name):

    S3.delete_object(Bucket=BUCKET,
                     Key=name)

    
