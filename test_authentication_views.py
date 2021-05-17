"""Authentication view tests."""

import os
from unittest import TestCase
from flask import g

from models import db, User

os.environ['DATABASE_URL'] = "postgresql:///personal_library_test"
os.environ['FLASK_ENV'] = "production"

from app import app, CURR_USER_KEY, do_login, do_logout

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class AuthenticationViewTestCase(TestCase):
    """Tests for authentication views."""

    def setUp(self):
        User.query.delete()

        # provide a test user to login for tests requiring a logged in user
        user = User(username='test_user@nodomain.com', password='password1')
        db.session.add(user)
        db.session.commit()

        self.user = user

    def test_do_login(self):
        """Adds the passed in user's user id to the session."""

        user = User(id=99, username='user1@nodomain.com', password='password1')

        with app.test_request_context('/') as c:
            do_login(user)

            self.assertEqual(c.session[CURR_USER_KEY], user.id)

    def test_do_logout(self):
        """Remove the user id from the session."""

        with app.test_request_context('/') as c:
            c.session[CURR_USER_KEY] = 99
            do_logout()

            self.assertNotIn(CURR_USER_KEY, c.session.keys())

    def test_signup_get(self):
        """A get request should display the signup form when there is not a user logged in."""

        with app.test_client() as c:
            resp = c.get('/signup')
            html = resp.get_data(as_text=True)

            self.assertIn("Sign me up!", html)

    def test_signup_post(self):
        """A post request should create a new user, log that user in and redirect to the root route."""

        data = {
            'username': 'new_user@nodomain.com',
            'password': 'new_password'
        }

        with app.test_client() as c:
            resp = c.post('/signup', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You don't have any books in your collection yet!", html)
            self.assertTrue(g.user)

    def test_signup_post_duplicate(self):
        """A post request for a username that has already been taken should redirect back to the signup form."""

        data = {
            'username': 'test_user@nodomain.com',
            'password': 'adifferentpassword'
        }

        with app.test_client() as c:
            resp = c.post('/signup', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Username already taken", html)

    def test_signup_already_logged_in(self):
        """
        A get request to the signup route when there is a user logged in
        should return a message and redirect to the user's books page.
        """
        # import pdb
        # pdb.set_trace()

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id
            resp = c.get('/signup', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Please logout before creating a new account", html)
