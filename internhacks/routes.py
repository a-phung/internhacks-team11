from flask import render_template, url_for, flash, redirect, request
from internhacks.forms import RegistrationForm, LoginForm
from internhacks.models import User
from internhacks import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/upload")
@login_required
def upload():
    return render_template("upload.html", title="Upload File")

@app.route("/account")
@login_required
def account():
    return render_template("account.html", title="Account")

@app.route("/register", methods=["GET", "POST"])
def register():
    # Redirect user if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Hash password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Create user instance - check form model for validation
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # Add user to database
        db.session.add(user)
        # Save database
        db.session.commit()
        flash(f"Your account has been created! You are now able to log in.", "success")
        # Redirect user to login page
        return redirect(url_for("login"))
    return render_template("register.html", title="Registration", form=form)

bcrypt.generate_password_hash('password').decode('utf-8')


@app.route("/login", methods=["GET", "POST"])
def login():
    # Redirect user if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        # Query database by given email
        user = User.query.filter_by(email=form.email.data).first()
        # Check user exists and checks password
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Login user
            login_user(user, remember=form.remember.data)
            flash("You are now logged in!", "success")
            # Redirect user based on URL params
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            # If no user or incorrect password
            flash("Login Unsuccessful. Please check email and password.", "danger")
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))