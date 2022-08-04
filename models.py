"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy


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
    created_at = db.Column(db.DateTime, nullable=False,
                           default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    tags = db.relationship("Tag", secondary='posts_tags', backref="posts")


class Tag(db.Model):
    """Tag."""
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)


class PostTag(db.Model):
    """PostTag."""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)
