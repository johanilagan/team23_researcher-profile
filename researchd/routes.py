from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from .forms import LoginForm, RegisterForm
from .models import User
from . import db

auth = Blueprint("auth", __name__)
main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("homepage.html")

@main.route("/profile")
@login_required
def my_profile():
    return render_template("profile_page.html", researcher=current_user, is_owner=True)

@main.route("/profile/<int:researcher_id>")
def researcher_profile(researcher_id):
    researcher = User.query.filter_by(uid=researcher_id).first_or_404()
    is_owner = current_user.is_authenticated and current_user.uid == researcher.uid
    return render_template("profile_page.html", researcher=researcher, is_owner=is_owner)

@main.route("/search")
def search():
    q = request.args.get("q", "").strip()
    
    # Basic query: adjust to your ORM/search logic
    if q:
        results = User.query.filter(
            (User.first_name.ilike(f"%{q}%")) |
            (User.last_name.ilike(f"%{q}%")) |
            (User.institution.ilike(f"%{q}%")) |
            (User.position.ilike(f"%{q}%"))
        ).all()
    else:
        results = User.query.all()  # show all users if no query

    return render_template("search.html", results=results, q=q)

@main.route("/help")
def help():
    return render_template("help_centre.html")

@main.route("/contact")
def contact():
    return render_template("contact.html")

@main.route("/privacy")
def privacy():
    return render_template("privacy.html")

@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("main.home"))
        flash("Invalid credentials", "danger")
    return render_template("login.html", form=form)

@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # check if email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Email already registered. Please login.", "warning")
            return redirect(url_for("auth.register"))
        
        # create new user
        user = User(
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            institution=form.institution.data,
            position=form.position.data
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Account created! Please login.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.home"))
