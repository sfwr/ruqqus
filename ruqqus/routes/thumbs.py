from flask import *
from os import environ
import requests

from ruqqus.helpers.get import *
from ruqqus.__main__ import app, limiter

APIFLASH_KEY=environ.get("APIFLASH_KEY")

@app.route('/thumbs/<pid>', methods=["GET"])
def thumbs(pid):

    post=get_post(pid)

    if not post.thumb_id:
        abort(404)

    url=f"https://api.apiflash.com/v1/urltoimage/cache/{post.thumb_id}.jpeg?access_key={APIFLASH_KEY}"

    x=requests.get(url)

    resp = make_response(x.content)
    resp.headers.add("Content-Type", "image/jpeg")

    return resp
