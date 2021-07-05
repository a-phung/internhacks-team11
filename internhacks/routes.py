from flask import render_template, url_for, flash, redirect
from internhacks.forms import RegistrationForm, LoginForm
from internhacks.models import User
from internhacks import app, db, bcrypt

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created! You are now able to log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Registration", form=form)

bcrypt.generate_password_hash('password').decode('utf-8')


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # TODO: Connect to database to verify login
        flash("You are now logged in!", "success")
        return redirect(url_for("home"))
        # Else:
        #     flash("Login Unsuccessful. Please check username and password", "danger")
    return render_template("login.html", title="Login", form=form)