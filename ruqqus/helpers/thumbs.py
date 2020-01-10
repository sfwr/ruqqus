import requests
from os import environ
from urllib.parse import urlparse

from .get import *
from ruqqus.__main__ import db

def thumbnail_thread(post, can_show_thumbnail=False):

    #step 1: see if post is image

    print("thumbnail thread")

    if can_show_thumbnail:
        print("image post")
        x=requests.head(post.url)

        if x.headers["Content-Type"].split("/")[0]=="image":
            post.is_image=True
            db.add(post)
            db.commit()

            return

    else:
        url=f"https://api.apiflash.com/v1/urltoimage"
        params={'access_key':environ.get("APIFLASH_KEY"),
                'format':'png',
                'height':720,
                'width':1280,
                'response_type':'image',
                'thumbnail_width':300,
                'url':self.url,
                'css':"iframe {display:none;}"
                }
        x=requests.get(url, params=params)
        print("have thumb from apiflash")

        name=f"posts/{self.base36id}/thumb.png"
        tempname=name.replace("/","_")

        with open(tempname, "wb") as file:
            for chunk in x.iter_content(1024):
                file.write(chunk)

        print("thumb saved")

        aws.upload_from_file(name, tempname)
        post.has_thumb=True
        db.add(post)
        db.commit()

        print("thumb all success")
