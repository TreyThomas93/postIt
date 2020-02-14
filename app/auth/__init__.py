from extensions import db, login_manager, mail
from flask_login import login_required, current_user, login_user, logout_user
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_mail import Message
import bcrypt
from models import Users
import os

authorize = Blueprint("authorize", __name__, template_folder="templates", static_folder="static", static_url_path="/auth/static")

login_manager.login_view = "authorize.login"
login_manager.login_message = "You Must Be Logged In To Access!"
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

## LOGIN/LOGOUT ##
@authorize.route("/login", methods=["POST", "GET"])
def login():
    msg = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = Users.query.filter_by(username=username).first()
        if user:
            if bcrypt.hashpw(password.encode('utf-8'), user.password):
                login_user(user)
                return redirect(url_for("home.index"))
                
        msg = "Invalid Username and/or Password."
        flash(msg, "danger")
        return render_template("auth/login.html")
    else:
        msg = request.args.get("msg")
        flash(msg, "success")
        return render_template("auth/login.html")

@authorize.route("/logout", methods=["POST", "GET"])
def logout():
    logout_user()
    return redirect(url_for("authorize.login", msg="Logged Out!"))

## REGISTER ##
@authorize.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if username and password and confirm_password and email:
            username_exists = Users.query.filter_by(username=username).first()
            email_exists = Users.query.filter_by(email=email).first()
            if not username_exists and not email_exists:
                if password == confirm_password:
                    add = Users(username=username, password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()), email=email)
                    db.session.add(add)
                    db.session.commit()
                    flash("Thanks For Registering! Please Login!", "success")
                    return redirect(url_for("authorize.login"))
                else:
                    flash("ERROR: Passwords Do Not Match!", "danger")
            else:
                    flash("ERROR: Username and/or Email Already Exists!", "danger")
        else:
            flash("ERROR: Empty Fields!", "danger")

    return render_template("auth/register.html")

## PASSWORD RESET/TOKEN ##
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request",
    sender="noreply@demo.com",
    recipients=[user.email])

    msg.body = f"""To reset your password, please visit the following link: 
{url_for("authorize.reset_token", token=token, _external=True)}
    
If you didn't make this request, simply ignore and no changes will be made.
    """

    mail.send(msg)

@authorize.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        if email:
            exists = Users.query.filter_by(email=email).first()
            if exists:
                send_reset_email(exists)
                flash("An email was sent to reset your password!", "info")
                return redirect(url_for("authorize.login"))
            else:
              flash("ERROR: Email Does Not Exist!", "danger")  
        else:
            flash("ERROR: Empty Fields!", "danger")

    return render_template("auth/forgot_password.html")

@authorize.route("/reset_token/<token>", methods=["GET", "POST"])
def reset_token(token):
    user = Users.verify_reset_token(token)
    if not user:
        flash("Token is invalid or expired!", "danger")
        return redirect(url_for("authorize.forgot_password"))
    return render_template("auth/reset_password.html", email=user.email, token=token)

@authorize.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        email = request.form["email"]
        token = request.form["token"]
        new_password = request.form["new_password"]
        confirm_new_password = request.form["confirm_new_password"]
        if new_password and confirm_new_password:
            user = Users.query.filter_by(email=email).first()
            if user:
                if new_password == confirm_new_password:
                    user.password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                    db.session.commit()
                    flash("Your password has been updated! You can now login!", "info")
                    return render_template("auth/login.html")
                else:
                    flash("ERROR: Passwords do not match!", "danger")
        else:
            flash("ERROR: Empty Fields!", "danger")

    return redirect(url_for("authorize.reset_token", token=token))