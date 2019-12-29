import boto3
from os import environ, remove
from PIL import Image

BUCKET="i.ruqqus.com"

#setup AWS connection
S3=boto3.client("s3",
                aws_access_key_id=environ.get("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=environ.get("AWS_SECRET_ACCESS_KEY")
                )

def upload_file(name, file):

    #temp save for exif stripping
    tempname=name.replace("/","_")

    file.save(tempname)
    
    image=Image.open(tempname)
    raw_image=list(image.getdata())
    no_exif=Image.new(image.mode, image.size)
    no_exif.putdata(raw_image)
    no_exif.save(tempname)
    
    S3.upload_file(tempname,
                      Bucket=BUCKET,
                      Key=name,
                      ExtraArgs={'ACL':'public-read',
                                 "ContentType":"image/png"
                      }
                     )

    remove(tempname)

def delete_file(name):

    S3.delete_object(Bucket=BUCKET,
                     Key=name)

    
