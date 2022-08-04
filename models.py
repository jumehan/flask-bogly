"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Default url for testing
DEFAULT_IMAGE_URL = 'https://rithm-students-assets.s3.amazonaws.com/r27/exercises/flask-blogly/handout/_images/detail.png'


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
