import requests
from os import environ
from urllib.parse import urlparse

from .get import *
from ruqqus.__main__ import db

def thumbnail_thread(post):

    params={"access_key":enviorn.get("APIFLASH_KEY"),
            "url": post.url,
            "height":720,
            "width":1280,
            "format":"jpeg",
            "response_type":"json",
            "thumbnail_width":300
            }

    x=requests.get("https://api.apiflash.com/v1/urltoimage", params=params)

    post.thumb_id=urlparse(x.json()["url"]).split("/")[-1].split(".")[0]

    db.add(post)
    db.commit()
