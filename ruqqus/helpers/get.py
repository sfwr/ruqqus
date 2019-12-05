from ruqqus.classes import *
from .base36 import *
from ruqqus.__main__ import db

def get_user(username):

    x=db.query(User).filter_by(username=username).first()
    if not x:
        abort(404)
    return x

def get_post(pid):

    x=db.query(Submission).filter_by(id=base36decode(pid)).first()
    if not x:
        abort(404)
    return x

def get_comment(cid):

    x=db.query(Comment).filter_by(id=base36decode(cid)).first()
    if not x:
        abort(404)
    return x

def get_board(bid):

    x=db.query(Board).filter_by(id=base36decode(bid)).first()
    if not x:
        abort(404)
    return x
