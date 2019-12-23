from flask import *
from os import environ
import requests

from ruqqus.helpers.get import *
from ruqqus.helpers.wrappers import *
from ruqqus.mail.mail import send_mail
from ruqqus.__main__ import app, limiter

@app.route("/legal", methods=["GET"])
@auth_desired
def legal_1(v):
    return render_template("legal/legal.html", v=v)

@app.route("/legal/2", methods=["POST"])
@is_not_banned
@validate_formkey
def legal_2(v):

    if request.form.get("about_yourself","") not in ["law_enforcement","gov_official"]:
        return render_template("legal/legal_reject.html", v=v)

    elif request.form.get("request_type","")=="user_info_baseless":
        return render_template("legal/legal_reject2.html", v=v)


    if request.form.get("request_type","")=="user_info_legal":
        return render_template("legal/legal_user.html", v=v)


    
    

@app.route("/legal/final", methods=["POST"])
@is_not_banned
@validate_formkey
def legal_final(v):

    data={x: request.form[x] for x in request.form if x !="formkey"}

    send_mail(environ.get("admin_email"),
              "Legal request submission",
              render_template_string("<div>{% for k in data %}<h1>{{ k }}<h1><p>{{ data[k] }}</p></div>",
                                     data=data),
              files=request.files
              )

    return render_template("legal/legal_done.html",
                           success=(basin.status_code==200),
                           v=v)
    
