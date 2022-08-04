"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

# BELOW ARE THE USER ROUTES

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


@app.post('/users/new')
def process_new_user():
    """Process the add form, adding a new user and going back to /users"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None

#  validate inputs before submit
    user = User(first_name=first_name,
                last_name=last_name, image_url=image_url)

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

# GET /users/[user-id]
# Show information about the given user.


@app.get('/users/<int:user_id>')
def show_user_detail(user_id):
    """Show information about the given user."""
    # Have a button to get to their edit page, and to delete the user.

    user = User.query.get_or_404(user_id)

    return render_template('user_detail.html', user=user)


# GET /users/[user-id]/edit
# Show the edit page for a user.
# Have a cancel button that returns to the detail page for a user, and a save button that updates the user.
@app.get('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Show the edit page for a user."""

    user = User.query.get_or_404(user_id)

    return render_template('edit_user.html', user=user)


# POST /users/[user-id]/edit
# Process the edit form, returning the user to the /users page.
@app.post('/users/<int:user_id>/edit')
def process_edit_form(user_id):
    """Process the edit form, returning the user to the /users page."""

    user = User.query.get_or_404(user_id)

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    #  validate inputs before submit
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()

    return redirect('/users')


@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Delete the user"""

    user = User.query.get_or_404(user_id)

    # user.query.delete() incorrect
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


# BELOW ARE THE POST ROUTES

# GET /users/[user-id]/posts/new
# Show form to add a post for that user.
@app.get('/users/<int:user_id>/posts/new')
def new_post(user_id):
    """Render create a new post form"""

    user = User.query.get_or_404(user_id)

    return render_template('/new_post.html', user=user)

# POST /users/[user-id]/posts/new
# Handle add form; add post and redirect to the user detail page.
@app.post('/users/<int:user_id>/posts/new')
def add_new_post(user_id):
    """Lets user add a new post including post title and content"""

    title = request.form["title"]
    content = request.form["content"]

    post = Post(title=title, content=content, user_id=user_id)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

# GET /posts/[post-id]
# Show a post.
@app.get('/posts/<int:post_id>')
def show_post(post_id):
    """Render show details for a post."""

    post = Post.query.get(post_id)

    return render_template('/post_detail.html', post=post)

# GET /posts/[post-id]/edit
# Show form to edit a post, and to cancel (back to user page).
@app.get('/posts/<int:post_id>/edit')
def show_edit_post(post_id):
    """Render edit form to edit a post."""

    post = Post.query.get(post_id)

    return render_template('/edit_post.html', post=post)

# POST /posts/[post-id]/edit
# Handle editing of a post. Redirect back to the post view.
@app.post('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Render edit form to edit a post."""

    post = Post.query.get(post_id)

    title = request.form["title"]
    content = request.form["content"]

    post.title = title
    post.content = content

    db.session.commit()

    return redirect(f"/posts/{post_id}")

# POST /posts/[post-id]/delete
# Delete the post.
@app.post('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Delete a post."""

    post = Post.query.get(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")
