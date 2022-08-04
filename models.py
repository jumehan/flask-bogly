"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from sqlalchemy.sql import func


db = SQLAlchemy()

# Default url for testing
DEFAULT_IMAGE_URL = 'https://www.fwpgroup.co.uk/wp-content/uploads/2020/03/male-profile-icon-white-on-the-blue-background-vector-3451989-421x500.jpg'


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    image_url = db.Column(db.Text(), nullable=False, default=DEFAULT_IMAGE_URL)

    posts = db.relationship("Post", backref="user")


class Post(db.Model):
    """Post"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created_at = db.Column(DateTime(timezone=True),
                           server_default=func.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
