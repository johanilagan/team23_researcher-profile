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
def profile():
    return render_template("profile_page.html", user=current_user)

@main.route("/search")
def search():
    return render_template("search.html")

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
