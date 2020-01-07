from urllib.parse import urlparse
from time import time

from ruqqus.helpers.wrappers import *
from ruqqus.helpers.base36 import *
from ruqqus.helpers.sanitize import *
from ruqqus.helpers.get import *
from ruqqus.classes import *

from flask import *
from ruqqus.__main__ import app, db


@app.route("/badge_grant", methods=["GET"])
@admin_level_required(4)
def badge_grant_get(v):

    badge_types=db.query(BadgeDef).filter_by(kind=3).order_by(BadgeDef.rank).all()

    return render_template("badge_grant.html",
                           v=v,
                           badge_types=badge_types
                           )
