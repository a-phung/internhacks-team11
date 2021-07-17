from datetime import datetime
from internhacks import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    """ Given user's id, retrieves user from database. """
    return User.query.get(int(user_id))

# Association table between User and Study.
UserBookmarks = db.Table('bookmarks',
    db.Column('study_id', db.Integer, db.ForeignKey('study.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

# Association table between Study and Tags.
StudyTags = db.Table('tags',
    db.Column('study_id', db.Integer, db.ForeignKey('study.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class User(db.Model, UserMixin):
    """ Represents a user or admin user with login information. """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    bookmarks = db.relationship('Study', secondary=UserBookmarks, backref=db.backref('bookmarked'), lazy=True)

    def __repr__(self):
        """ Prints string of User. """
        return f"User('{self.id}', '{self.username}')"

class Study(db.Model):
    """ Represents a case study submitted by admin user. """
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(40), unique=True, nullable=False)
    description = db.Column(db.String(160), nullable=False)
    external_url = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tags = db.relationship('Tag', secondary=StudyTags, backref=db.backref('studies'), lazy=True)

    def __repr__(self):
        """ Prints string of Study. """
        return f"Study('{self.id}', '{self.topic}')"

class Tag(db.Model):
    """ Represents a Tag that is attached to a Study. """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)

    def __repr__(self):
        """ Prints string of Tag. """
        return f"Tag('{self.id}', '{self.name}')"
