from flask import *
from os import environ
import requests

from ruqqus.__main__ import app, limiter

APIFLASH_KEY=environ.get("APIFLASH_KEY")

@app.route('/thumbs/<image_id>', methods=["GET"])
def thumbs(image_id):

    url=f"https://api.apiflash.com/v1/urltoimage/cache/{image_id}.jpeg?access_key={APIFLASH_KEY}"

    x=requests.get(url)

    resp = make_response(x.content)
    resp.headers.add("Content-Type", "image/jpeg")

    return resp
