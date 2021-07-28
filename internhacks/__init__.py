from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Starts Flask app
app = Flask(__name__)
# Protects against cookies - store your key in your ENV file
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY') 
# Our database is found at site.db for local - for production, we will change this
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
# Creates database
db = SQLAlchemy(app)
# Generates and checks password hashes 
bcrypt = Bcrypt(app)
# Handles all of our login/logout functionality
login_manager = LoginManager(app)
# User is redirected to /login if not logged in
login_manager.login_view = 'login' 
login_manager.login_message_category = 'info'
# Import routes - DO NOT MOVE THE BELOW LINE
from internhacks import routes 