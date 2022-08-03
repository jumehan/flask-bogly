"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)


# GET /
# Redirect to list of users. (We’ll fix this in a later step).
@app.get('/')
def redirect_to_users():
    """Redirect to list of users. """
    return redirect('/users')

# GET /users
# Show all users.


@app.get('/users')
def show_all_users():
    """Show all users."""

    # Make these links to view the detail page for the user.
    users = User.query.all()

    # Have a link here to the add-user form.
    return render_template('index.html', users=users)


# GET /users/new
@app.get('/users/new')
def show_add_form():
    """Show an add form for users"""
    return render_template('new_user.html')

# POST /users/new
# Process the add form, adding a new user and going back to /users


@app.post('/users/new')
def process_new_user():

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

#  validate inputs before submit
    user = User(first_name=first_name,
                last_name=last_name, image_url=image_url)

    db.session.add(user)
    db.session.commit()

    return redirect('users')

# GET /users/[user-id]
# Show information about the given user.

# Have a button to get to their edit page, and to delete the user.

# GET /users/[user-id]/edit
# Show the edit page for a user.

# Have a cancel button that returns to the detail page for a user, and a save button that updates the user.

# POST /users/[user-id]/edit
# Process the edit form, returning the user to the /users page.
# POST /users/[user-id]/delete
# Delete the user.
