import time
from flask import *
from sqlalchemy import *

from ruqqus.helpers.wrappers import *
from ruqqus.helpers.get import *

from ruqqus.__main__ import app, db, cache
from ruqqus.classes.boards import Board


@app.route("/api/guild/<boardname>", methods=["GET"])
@cache.memoize(timeout=60)
def guild_info(boardname):
    guild = get_guild(boardname)

    return jsonify(guild.json)



