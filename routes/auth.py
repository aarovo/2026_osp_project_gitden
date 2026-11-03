import hashlib

from flask import Blueprint, redirect, render_template, request, url_for
from database import DBhandler

DB = DBhandler()

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login")
def login():
    return render_template("login.html")

@auth_bp.route("/signup")
def signup():
    return render_template("signup.html")

@auth_bp.route("/signup_post", methods=["POST"])
def signup_post():
    data = request.form
    pw_hash = hashlib.sha256(data["pw"].encode("utf-8")).hexdigest()

    if DB.insert_user(data, pw_hash):
        return redirect(url_for("auth.login"))
    return render_template("signup.html", error="이미 사용 중인 ID입니다.")