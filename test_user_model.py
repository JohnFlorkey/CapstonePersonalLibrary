"""User model tests."""

import os
from unittest import TestCase
import sqlalchemy.exc
from models import db, User

os.environ['DATABASE_URL'] = "postgresql:///personal_library_test"
os.environ['FLASK_ENV'] = "production"

from app import app

db.create_all()


class UserModelTestCase(TestCase):
    """Test user model."""

    def setUp(self):
        """Create sample user data."""

        User.query.delete()

        user = User(username="user1@nodomain.com", password="password1")
        db.session.add(user)
        db.session.commit()

        self.user = user

    def tearDown(self):
        """Rollback any open transactions"""

        db.session.rollback()

    def test_user_model(self):
        """Does basic model work?"""

        self.assertEqual(self.user.username, "user1@nodomain.com")
        self.assertEqual(self.user.password, "password1")

    def test_signup(self):
        """Is a new user created by the signup class method."""

        user = User.signup(username="user2@nodomain.com", password="password2")
        db.session.commit()

        self.assertEqual(user.username, "user2@nodomain.com")
        self.assertTrue(user.password)
        self.assertNotEqual(user.password, "password2")

    def test_signup_duplicate_user(self):
        """An attempt to signup a duplicate username results in an integrity error."""

        User.signup(username="user1@nodomain.com", password="nonsense")

        self.assertRaises(sqlalchemy.exc.IntegrityError, db.session.commit)

    def test_user_authenticate(self):
        """Does a valid authentication attempt return the user object."""

        new_user = User.signup(
            username="user2@nodomain.com",
            password="password2"
        )
        user = User.authenticate(
            username="user2@nodomain.com",
            password="password2"
        )

        self.assertIsInstance(user, User)
        self.assertEqual(user, new_user)

    def test_user_authenticate_invalid(self):
        """Does an invalid authentication attempt return false."""

        User.signup(
            username="user2@nodomain.com",
            password="password2"
        )
        invalid_username_result = User.authenticate(
            username="frank",
            password="password2"
        )
        invalid_password_result = User.authenticate(
            username="user2@nodomain.com",
            password="notthepassword"
        )

        self.assertFalse(invalid_username_result)
        self.assertFalse(invalid_password_result)
