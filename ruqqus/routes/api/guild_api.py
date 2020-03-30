import time
from flask import *
from ruqqus.classes import *
from ruqqus.helpers.wrappers import *
from ruqqus.helpers.base36 import *
from secrets import token_hex
from ruqqus.routes.login import valid_password_regex, valid_username_regex
from ruqqus.__main__ import db, app
import re


@app.route("/api/v1/guilds", methods=["GET"])
@admin_level_required(2)
def get_all_guilds_api(v):
    guilds=[]
    for g in db.query(Board).all():
        guilds.append(g.json())
    return jsonify({"Guilds": {guilds}})

@app.route("/api/v1/guild/<id>", methods=["GET"])
@admin_level_required(2)
def get_guild_api(v, id):
    return jsonify(db.query(Board).filter_by(id=base36decode(id)).first().json())

@app.route("/api/v1/guild", methods=["POST"])
@admin_level_required(2)
def create_guild_api(v):
    pass
    # TODO add create guild
    #return jsonify(comment)

@app.route("/api/v1/guild/<id>", methods=["PUT"])
@admin_level_required(2)
def update_guild_api(v, id):
    """TODO : update logic"""
    return jsonify(db.query(Board).filter_by(id=base36decode(id)).first().json())

@app.route("/api/v1/guild/<id>", methods=["DELETE"])
@admin_level_required(2)
def delete_guild_api(v, id):
    pass
    #db.delete(db.query(Board).filter_by(id=base36decode(id)).first())
    #db.commit()
    #return "", 200