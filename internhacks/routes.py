from flask import render_template, url_for, flash, redirect, request, jsonify, g
from internhacks.forms import RegistrationForm, LoginForm, StudyForm, TagForm, SearchForm
from internhacks.models import User, Study, Tag, Bookmark
from internhacks import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from functools import wraps


def admin_required(f):
    """ Custom function decorator for admin access only. """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If user is not admin or logged in
        if not current_user.is_admin or not current_user.is_authenticated:
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/admin")
@admin_required
def admin():
    return render_template("admin/index.html", title="Admin")


@app.route("/study/new", methods=["GET", "POST"])
@admin_required
def new_study():
    form = StudyForm()
    if form.validate_on_submit():
        # Create study instance - check form model for validation
        study = Study(topic=form.topic.data, description=form.description.data, external_url=form.external_url.data, image_url=form.image_url.data)
        # Add study to database
        db.session.add(study)
        # Save database
        db.session.commit()
        flash(f"This case study was created!", "success")
        return redirect(url_for('new_study'))
    return render_template("/admin/create_study.html", title="Create New Case Study", form=form)


@app.route("/tag/new", methods=["GET", "POST"])
@admin_required
def new_tag():
    form = TagForm()
    if form.validate_on_submit():
        # Create tag instance - check form model for validation
        tag = Tag(name=form.name.data)
        # Add tag to database
        db.session.add(tag)
        # Save database
        db.session.commit()
        flash(f"This tag was created!", "success")
        return redirect(url_for('new_tag'))
    return render_template("/admin/create_tag.html", title="Create New Tag", form=form)

@app.route("/tag/all", methods=["GET"])
def view_tags():
    tags = Tag.query.all()
    return jsonify([
        {'id': tag.id, 'name': tag.name} for tag in tags]
    )

@app.route("/study/all", methods=["GET"])
def view_studies():
    studies = Study.query.all()
    return jsonify([
        {'id': study.id, 'topic': study.topic, 'description': study.description, 'external_url': study.external_url, 'image_url': study.image_url} for study in studies]
    )


@app.route("/case-studies", methods=["GET"])
def case_studies():
    studies = Study.query.all()
    tags = Tag.query.all()
    return render_template("studies.html", title="Case Studies", studies=studies, tags=tags, form=SearchForm())


@app.route("/case-studies/search", methods=["GET", "POST"])
def search():
    results = Study.query.all()
    form = SearchForm()
    search_string = form.search.data
    if search_string:
        filtered_results = []
        for result in results:
            if search_string in result.topic.lower() or search_string in result.description.lower():
                filtered_results.append(result)
        if filtered_results:
            results = filtered_results
        else:
            flash(f"There were no matches to your search.", "warning")
    return render_template("studies.html", title="Case Studies - Results", studies=results, tags=Tag.query.all(), form=form)


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