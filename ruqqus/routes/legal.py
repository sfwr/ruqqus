from flask import *
from os import environ
import requests

from ruqqus.helpers.get import *
from ruqqus.helpers.wrappers import *
from ruqqus.__main__ import app, limiter

@app.route("/legal", methods=["GET"])
@auth_desired
def legal_1(v):
    return render_template("legal/legal.html")

@app.route("/legal/2", methods=["POST"])
@is_not_banned
@validate_formkey
def legal_2(v):

    if request.form.get("about_yourself","") not in ["law_enforcement","gov_official"]:
        return render_template("legal/legal_reject.html")

    elif request.form.get("request_type","")=="user_info_baseless":
        return render_template("legal/legal_reject2.html")


    if request.form.get("request_type","")=="user_info":
        return render_tempalte("legal/legal_user.html", v=v)


    
    

@app.route("/legal/final", methods=["POST"])
@is_not_banned
@validate_formkey
def legal_final(v):

    url=environ.get("BASIN_URL")

    data={x: request.form[x] for x in request.form if x !="formkey"}

    basin=requests.post(url,
                    form=data,
                    files=request.files)

    return render_template("legal/legal_done.html", v=v)
    
