import time
from flask import *
from sqlalchemy import *

from ruqqus.helpers.wrappers import *
from ruqqus.helpers.get import *

from ruqqus.__main__ import app, db, cache
from ruqqus.classes.boards import Board


@app.route("/api/v1/guild/<boardname>", methods=["GET"])
def guild_info(boardname):
    guild = get_guild(boardname)

    return jsonify(guild.json)


@app.route("/api/v1/user/<username>", methods=["GET"])
def user_info(username):

    user=get_user(username)
    return jsonify(user.json)

@app.route("/api/v1/post/<pid>", methods=["GET"])
@auth_desired
def post_info(pid):

    post=get_post(pid)
    return jsonify(post.json)

@app.route("/api/v1/comment/<cid>", methods=["GET"])
@auth_desired
def comment_info(cid)

    comment=get_comment(cid)
    return jsonify(comment.json)
