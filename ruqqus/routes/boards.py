from urllib.parse import urlparse
import mistletoe
import re

from ruqqus.helpers.wrappers import *
from ruqqus.helpers.base36 import *
from ruqqus.helpers.sanitize import *
from ruqqus.helpers.filters import *
from ruqqus.helpers.markdown import *
from ruqqus.classes import *
from flask import *
from ruqqus.__main__ import app, db, limiter

valid_board_regex=re.compile("^\w{3,25}")

@app.route("/create_board", methods=["GET"])
@is_not_banned
def create_board_get(v):
    return render_template("make_board.html", v=v)

@app.route("/api/board_available/<name>", methods=["GET"])
def api_board_available(name):
    if db.query(Board).filter(Board.name.ilike(name)).first():
        return jsonify({"board":name, "available":False})
    else:
        return jsonify({"board":name, "available":True})

@app.route("/create_board", methods=["POST"])
@is_not_banned
@validate_formkey
def create_board_post(v):

    board_name=request.form.get("name")
    board_name=board_name.lstrip("+")

    if v.karma<100:
        return render_template("message.html", title="Unable to make board", text="You need more rep to do that")

    if not v.is_activated:
        return render_template("message.html", title="Unable to make board", text="Please verify your email first")
    #check name
    if db.query(Board).filter(Board.name.ilike(board_name)).first():
        abort(409)

    description = request.form.get("description")
    description_md=mistletoe.markdown(description)
    description_html=sanitize(description_md, linkgen=True)

    

    new_board=Board(name=board_name,
                    description=description,
                    description_html=description_html)

    db.add(new_board)
    db.commit()

    return redirect(new_board.permalink)

@app.route("/board/<name>", methods=["GET"])
@app.route("/+<name>", methods=["GET"])
@auth_desired
def board_name(name, v):

    board=db.query(Board).filter(Board.name.ilike(name)).first()

    if not board:
        abort(404)

    if not board.name==name:
        return redirect(board.permalink)

    sort=request.args.get("sort","hot")
    page=int(request.args.get("page", 1))
             
    return board.rendered_board_page(v=v,
                                     sort=sort,
                                     page=page)

#@app.route("/board/<name>/<pid>", methods=["GET"])

