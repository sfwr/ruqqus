from urllib.parse import urlparse
import mistletoe

from ruqqus.helpers.wrappers import *
from ruqqus.helpers.base36 import *
from ruqqus.helpers.sanitize import *
from ruqqus.helpers.filters import *
from ruqqus.helpers.markdown import *
from ruqqus.classes import *
from flask import *
from ruqqus.__main__ import app, db

@app.route("/api/board_available/<name>", methods=["GET"])
def api_board_available(name):
    if db.query(Board.name).filter(Board.name.ilike(name)).count():
        return jsonify({"board":name, name:False})
    else:
        return jsonify({"board":name, name:True})


@app.route("/board/<name>", methods=["GET"])
@app.route("/+<name>", methods=["GET"])
@auth_desired
def board_name(name, v):

    board=db.query(Board).filter(Board.name.ilike(name)).first()

    if not board:
        abort(404)

    if not board.name ==name:
        return redirect(board.permalink)

    return board.rendered_board_page(v,
                                     sort=request.args.get("sort","hot"),
                                     page=int(request.args.get("page", 1))
                                     )
#@app.route("/board/<name>/<pid>", methods=["GET"])

