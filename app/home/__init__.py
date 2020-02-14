from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from extensions import db
from models import Users, Posts
from datetime import datetime

home = Blueprint("home", __name__, template_folder="templates", static_folder="static", static_url_path="/home/static")

@home.route("/")
@login_required
def index():
    posts = Posts.query.all()
    return render_template("home/home.html", posts=posts, current_user=current_user)

# CREATE POST
@home.route("/create_post", methods=["POST"])
@login_required
def create_post():
    if request.method == "POST":
        post = request.form["post"]
        if post:
            posted_at = datetime.now().replace(microsecond=0)

            add = Posts(post=post, posted_at=posted_at, poster=current_user)
            db.session.add(add)
            db.session.commit()
            flash("You Created A Post!", "success")
        else:
            flash("ERROR: Empty Fields!", "danger")
            
    return redirect(url_for("home.index"))

# DELETE POST
@home.route("/delete_post", methods=["POST"])
@login_required
def delete_post():
    if request.method == "POST":
        id = request.form["id"]

        post = Posts.query.filter_by(id=id).first()
        db.session.delete(post)
        db.session.commit()

    
    flash("You Deleted A Post!", "success")
    return redirect(url_for("home.index"))

# EDIT POST
@home.route("/edit_post", methods=["POST", "GET"])
@login_required
def edit_post():
    if request.method == "POST":
        id = request.form["id"]
        edited_post = request.form["post"]
        post = Posts.query.filter_by(id=id).first()
        post.post = edited_post
        post.posted_at = datetime.now().replace(microsecond=0)
        db.session.commit()
        flash("Post Edited!", "success")
        return redirect(url_for("home.index"))

    id = request.args.get("id")
    post = request.args.get("post")
    return render_template("home/edit.html", id=id, post=post)




