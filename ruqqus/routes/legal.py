from flask import *
from os import environ
import requests

from ruqqus.helpers.get import *
from ruqqus.__main__ import app, limiter

@app.route("/legal", methods=["GET"])
@auth_desired
def legal_1(v):
    return render_template("legal.html")

@app.route("/legal/2", methods=["POST"])
@is_not_banned
def help_legal_2(v):

    if request.form.get("about_yourself","") not in ["law_enforcement","gov_official"]:
        return render_template("legal_reject.html")

    elif request.form.get("request_type","")=="user_info_baseless":
        return render_template("legal_reject2.html")


    if request.form.get("request_type","")=="user_info":
        return render_tempalte("legal_user.html", v=v)


    
    


