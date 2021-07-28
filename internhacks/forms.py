from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from internhacks.models import User, Study, Tag


class RegistrationForm(FlaskForm):
    """ Create new account form. """
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        """ Raise error if non-unique username. """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different username.')
    
    def validate_email(self, email):
        """ Raise error if non-unique email. """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please log in.')

class LoginForm(FlaskForm):
    """ Login user form. """
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    # Cookie to remember user is logged in
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class StudyForm(FlaskForm):
    """ Create new study form. """
    topic = StringField("Topic", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    external_url = StringField("External Link", validators=[DataRequired()])
    image_url = StringField("Image URL", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_topic(self, topic):
        """ Raise error if non-unique topic. """
        topic = Study.query.filter_by(topic=topic.data).first()
        if topic:
            raise ValidationError('That topic was already created.')

class TagForm(FlaskForm):
    """ Create new tag. """
    name = StringField("Topic", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_name(self, name):
        """ Raise error if non-unique tag name. """
        name = Tag.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That tag name was already created.')

class SearchForm(FlaskForm):
    """ Search on case studies page. """
    search = StringField("", render_kw={"placeholder": "Search topic or description..."})
    submit = SubmitField("Search")


class StudyTagForm(FlaskForm):
    """ Add tag to study. """
    study = SelectField(u'Case Study', choices=[(study.id, study.topic) for study in Study.query.all()])
    tag = SelectField(u'Tag', choices=[(tag.id, tag.name) for tag in Tag.query.all()])
    submit = SubmitField("Add")