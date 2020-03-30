import time
from flask import *
from ruqqus.classes import *
from ruqqus.helpers.wrappers import *
from ruqqus.helpers.base36 import *
from secrets import token_hex
from ruqqus.routes.login import valid_password_regex, valid_username_regex
from ruqqus.__main__ import db, app
import re


@app.route("/api/v1/posts", methods=["GET"])
@admin_level_required(2)
def get_all_posts_api(v):
    posts=[]
    for p in db.query(Submission).all():
        posts.append(p.json())
    return jsonify({"Posts": {posts}})

@app.route("/api/v1/post/<id>", methods=["GET"])
@admin_level_required(2)
def get_post_api(v, id):
    return jsonify(db.query(Submission).filter_by(id=base36decode(id)).first().json())

@app.route("/api/v1/post/<id>", methods=["PUT"])
@admin_level_required(2)
def update_post_api(v, id):
    """TODO : update logic"""
    return jsonify(db.query(User).filter_by(id=base36decode(id)).first().json())

@app.route("/api/v1/post/<id>", methods=["DELETE"])
@admin_level_required(2)
def delete_post_api(v, id):
    pass
    #db.delete(db.query(Submission).filter_by(id=base36decode(id)).first())
    #db.commit()
    #return "", 200