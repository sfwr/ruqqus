import time
from flask import *
from sqlalchemy import *

from ruqqus.helpers.wrappers import *

from ruqqus.__main__ import app, db, cache
from ruqqus.classes.boards import Board




@cache.memoize(timeout=60)
@app.route("/guild_info/<id>", methods=["GET"])
def guild_info(id=None):
    if not id:
        return abort(404)

    guild = db.query(Board).filter_by(id=id).first()

    if not guild:
        return abort(404)

    return jsonify(guild)



