import hashlib
import hmac

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from database import DBhandler

DB = DBhandler()

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = request.form.get("id", "")
        password = request.form.get("pw", "")
        valid_id = user_id and not any(char in user_id for char in "/.#$[]")
        user = DB.get_user(user_id) if valid_id else None
        password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        stored_hash = user.get("pw") if user else None

        if isinstance(stored_hash, str) and hmac.compare_digest(stored_hash, password_hash):
            session.clear()
            session["id"] = user_id
            return redirect(url_for("index"))

        flash("Wrong ID or PW!", "error")
        return redirect(url_for("auth.login"))

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

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
