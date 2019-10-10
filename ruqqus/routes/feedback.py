from ruqqus.helpers.wrappers import *
from flask import *
from ruqqus.__main__ import app, db


@app.route("/feedback", methods=["GET"])
@auth_required
@validate_formkey
def feedback_form(v):
    return render_template("feedback.html")


@app.route("/feedback", methods=["POST"])
@auth_required
@validate_formkey
def feedback_form_submit(v):
    return render_template("feedback.html", msg="Form submitted successfully")


@app.route("/feedback/admin", methods=["GET", "POST"])
@admin_level_required(3)
@validate_formkey
def feedback_admin_show_all(v):
    feedback = db.query(Feedback).all()
    return render_template("feedback.html", feedback)



@app.route("/feedback/admin/<id>", methods=["GET", "POST"])
@admin_level_required(3)
@validate_formkey
def feedback_admin_single(v):
    feedback = db.query(Feedback).filter_by(id=id).first()

    if not feedback:
        return render_template("feedback.html", error="Invalid Feedback ID")

    return render_template("feedback.html", feedback)