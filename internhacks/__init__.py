from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)  # Instantiates Flask App
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')  # Protects against cookies
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app) 
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from internhacks import routes