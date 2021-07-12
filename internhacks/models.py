from datetime import datetime
from internhacks import db, login_manager
from flask_login import UserMixin

# Loads user by user ID in /login route
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Study(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(40), unique=True, nullable=False)
    description = db.Column(db.String(160), nullable=False)
    external_url = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # tags = db.relationship('Tag', backref='study', lazy=True)

    def __repr__(self):
        return f"Study('{self.topic}', '{self.created_at}')"

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)

    def __repr__(self):
        return f"Tag('{self.name}', '{self.id}')"

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# class StudyTags(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     study_id = db.Column(db.Integer, db.ForeignKey('study.id'))
#     tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))

# class UserBookmarks(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     bookmark_id = db.Column(db.Integer, db.ForeignKey('bookmark.id'))