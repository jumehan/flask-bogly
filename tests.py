
from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, User, Post

# Let's configure our app to use a different database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test_first",
            last_name="test_last",
            image_url=None,
        )

        second_user = User(
            first_name="test_two",
            last_name="test_last_two",
            image_url=None,
        )

        db.session.add_all([test_user, second_user])
        db.session.commit()

        self.user_id = test_user.id
        self.user_id_two = second_user.id

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        """Display user list, renders index.html correctly"""
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)

    def test_user_details(self):
        """Display user detail with edit and delete button"""
        with self.client as c:
            resp = c.get(f'/users/{self.user_id}')
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_first", html)
            self.assertIn("Delete", html)
            self.assertIn("Edit", html)
            self.assertNotIn("test_first_two", html)

    def test_add_new_user(self):
        """Adds new user to the database"""
        with self.client as c:
            resp = c.post('/users/new',
                          data={'first_name': 'Joe',
                                'last_name': 'Rabbit', 'image_url': ''},
                          follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Rabbit", html)

    def test_delete_user(self):
        """Deletes user from database"""
        with self.client as c:
            resp = c.post(f'/users/{self.user_id}/delete',
                          follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            # breakpoint()
            html = resp.get_data(as_text=True)
            self.assertNotIn("test_first", html)
            self.assertIn("test_two", html)


class PostViewTestCase(TestCase):
    """Test viewing, adding, editing, and deleting posts"""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test_first",
            last_name="test_last",
            image_url=None,
        )

        db.session.add_all([test_user])
        db.session.commit()

        self.user_id = test_user.id

        post_one = Post(
            title="post one",
            content="content of post one",
            created_at = None,
            user_id=self.user_id
        )

        db.session.add(post_one)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.

        self.post_one_id = post_one.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_add_new_post(self):
        """"adds posts to the database"""
        with self.client as c:

            resp = c.post(f'/users/{self.user_id}/posts/new',
                          data={'title': 'Rabbits are cool',
                                'content': 'Rabbits are cool content',
                                'user_id': self.user_id},
                          follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Rabbit", html)

    def test_view_post(self):
        """"allows viewing a post from the database"""
        with self.client as c:

            resp = c.get(f'/posts/{self.post_one_id}')
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("content of post one", html)
            self.assertIn('post one', html)
            self.assertIn("test_first", html)

    def test_delete_post(self):
        """deletes post"""
        with self.client as c:
            resp = c.post(
                f'/posts/{self.post_one_id}/delete', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertNotIn('post one', html)

    def test_edit_post(self):
        """edits post"""
        with self.client as c:
            resp = c.post(
                f'/posts/{self.post_one_id}/edit',
                data={"title": "NewPostTitle", 'content': 'Rabbits are cool content'}, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertNotIn('post one', html)
            self.assertIn('NewPostTitle', html)