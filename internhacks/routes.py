from flask import render_template, url_for, flash, redirect, request, jsonify, g
from internhacks.forms import RegistrationForm, LoginForm, StudyForm, TagForm, SearchForm, StudyTagForm
from internhacks.models import User, Study, Tag
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
    """ Render Home page. """
    studies = Study.query.limit(2).all()
    return render_template("home.html", studies=studies)


@app.route("/recommended-practices")
def practices():
    """ Render Practices page. """
    return render_template("practices.html", title="Recommended Practices")


@app.route("/admin")
@admin_required
def admin():
    """ Render Admin page if user has admin access. """
    return render_template("admin/index.html", title="Admin")


@app.route("/study/new", methods=["GET", "POST"])
@admin_required
def new_study():
    """ GET add new case study form or POST new case study to database. """
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

@app.route("/bookmarks/new", methods=["GET", "POST"])
@login_required
def new_bookmark():
    """ GET add new bookmark for user or POST new bookmark to user. """
    # Retrieve study ID
    study_id = request.args.get('study')
    # Retrieve study object
    study = Study.query.get(study_id)
    # Does relationship already exist?
    if study in current_user.bookmarks:
        current_user.bookmarks.remove(study)
        db.session.commit()
        flash(f"This study has been un-bookmarked.", "success")
    else:
        # Add study to bookmarks
        current_user.bookmarks.append(study)
        # Save database
        db.session.commit()
        flash(f"This study was added!", "success")
    return render_template("studies.html", title="Case Studies", studies=Study.query.all(), tags=Tag.query.all(), form=SearchForm())

@app.route("/tag/new", methods=["GET", "POST"])
@admin_required
def new_tag():
    """ GET add new tag form or POST new tag to database. """
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


@app.route("/study/tag/new", methods=["GET", "POST"])
@admin_required
def new_study_tag():
    """ GET add tag to study form or POST new tag to study. """
    form = StudyTagForm()
    if form.validate_on_submit():
        # Retrieve study and tag instance
        study = Study.query.get(form.study.data)
        tag = Tag.query.get(form.tag.data)
        # Does relationship already exist?
        if tag in study.tags:
            flash(f"This tag is already added to this study.", "warning")
        else:
            # Add tag to study
            study.tags.append(tag)
            # Save database
            db.session.commit()
            flash(f"This tag was added!", "success")
    return render_template("/admin/add_study_tag.html", title="Add Tag to Case Study", form=form)


@app.route("/tag/all", methods=["GET"])
def view_tags():
    """ GET json of all tags. """
    tags = Tag.query.all()
    return jsonify([
        {'id': tag.id, 'name': tag.name} for tag in tags]
    )

@app.route("/study/all", methods=["GET"])
def view_studies():
    """ GET json of all studies. """
    studies = Study.query.all()
    return jsonify([
        {'id': study.id, 'topic': study.topic, 'description': study.description, 'external_url': study.external_url, 'image_url': study.image_url} for study in studies]
    )


@app.route("/case-studies", methods=["GET", "POST"])
def case_studies():
    """ GET list of case studies or POST case studies based on filters. """
    # Get tag if passed in
    tag_name = request.args.get('tag')
    # Get all studies and tags
    studies = Study.query.all()
    tags = Tag.query.all()
    form = SearchForm()
    # If there is a search query or tag filter
    if form.search.data or tag_name:
        # Create empty list to hold filtered results
        filtered_results = []
        # Iterte over every study
        for study in studies:
            if tag_name and not form.search.data:
                for tag in study.tags:
                    if tag_name == tag.name:
                        filtered_results.append(study)
            elif form.search.data in study.topic.lower() or form.search.data in study.description.lower():
                if tag_name:
                    for tag in study.tags:
                        if tag_name == tag.name:
                            filtered_results.append(study)
                else:
                    filtered_results.append(study)
        if filtered_results:
            studies = filtered_results
        else:
            flash(f"There were no matches to your search.", "warning")
    return render_template("studies.html", title="Case Studies", studies=studies, tags=tags, form=SearchForm())


@app.route("/upload")
@login_required
def upload():
    """ Render Upload page. """
    return render_template("upload.html", title="Upload File")


@app.route("/account")
@login_required
def account():
    """ Render Account page. """
    return render_template("account.html", title="Account")


@app.route("/register", methods=["GET", "POST"])
def register():
    """ Render User Registration form. """
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
    """ Render User Login form. """
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
    """ Logs out user. """
    logout_user()
    return redirect(url_for("home"))