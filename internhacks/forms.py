from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from internhacks.models import User, Study, Tag


class RegistrationForm(FlaskForm):  # Python classes representative of forms automatically converted to HTML
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different username.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please log in.')

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")  # Cookie to remember that user is logged in
    submit = SubmitField("Login")

class StudyForm(FlaskForm):
    topic = StringField("Topic", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    external_url = StringField("External Link", validators=[DataRequired()])
    image_url = StringField("Image URL", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_topic(self, topic):
        topic = Study.query.filter_by(topic=topic.data).first()
        if topic:
            raise ValidationError('That topic was already created.')

class TagForm(FlaskForm):
    name = StringField("Topic", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_name(self, name):
        name = Tag.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That tag name was already created.')

class SearchForm(FlaskForm):
    search = StringField("")
    submit = SubmitField("Search")