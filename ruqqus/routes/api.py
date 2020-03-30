import time
from flask import *
from ruqqus.classes import *
from ruqqus.helpers.wrappers import *
from ruqqus.helpers.base36 import *
from secrets import token_hex
from ruqqus.routes.login import valid_password_regex, valid_username_regex
from ruqqus.__main__ import db, app
import re



@app.route("/api/v1/users"methods=["GET"])
@admin_level_required(2)
def get_all_users_api(v):
    user=[]
    for u in db.query(User).all():
        user.append(u.json())
    return jsonify({"users": {user}})



@app.route("/api/v1/user/<id>", methods=["GET"])
@admin_level_required(2)
def get_user_api(v, id):
    return jsonify(db.query(User).filter_by(id=id).first().json())

@app.route("/api/v1/user", methods=["POST"])
@admin_level_required(2)
def create_user_api(v):
    user_data = {'username': request.args.get("username",""),
                 'email': request.args.get("email",""),
                 'password': request.args.get("password",""),
                 'admin_level': request.args.get("admin_level",0),
                 'creation_ip': request.remote_addr,
                 'reserved': request.args.get("reserved","")
                 'referred_by' request.args.get("referred_by","")
     }

    user = db.query(User).filter(User.username.ilike(user_data['username']), User.email.ilike(user_data['email']),
                                 User.is_activated == True).first()
    if user:
        return jsonify({'Error': "User Already Exists"})

    if not user_data['password'] == request.form.get("password_confirm"):
        return jsonify({"Error": "Passwords don't match"})

    #check username/pass conditions
    if not re.match(valid_username_regex, user_data["username"]):
        return jsonify({"Error": "Invalid username"})

    if not re.match(valid_password_regex, user_data["password"]):

        return jsonify({"Error": "Password must be 8 characters or longer"})

    new_user = User(username=user_data["username"],
                    password=user_data["password"],
                    email=user_data["email"],
                    created_utc=int(time.time()),
                    creation_ip=user_data["creation_ip"],
                    referred_by=user_data["referred_by"],
                    tos_agreed_utc=int(time.time())
                    )
    db.add(new_user)
    db.commit()

    return jsonify(db.query(User).filter_by(username=user_data["username"]).first().json())

@app.route("/api/v1/user/<id>", methods=["PUT"])
@admin_level_required(2)
def update_user_api(v, id):
    """TODO : update logic"""
    return jsonify(db.query(User).filter_by(id=id).first().json())

@app.route("/api/v1/user/<id>", methods=["DELETE"])
@admin_level_required(2)
def delete_user_api(v, id):
    pass
    #db.delete(db.query(User).filter_by(id=id).first())
    #db.commit()
    #return "", 200

