"""Util function tests."""
import os
from unittest import TestCase
import requests
import datetime
from models import db, User, Book, UserBook
from utils import lookup_isbn_open_library, map_response_to_book, search_user_books

os.environ['DATABASE_URL'] = "postgres:///personal_library_test"
os.environ['FLASK_ENV'] = "production"

from app import app

db.create_all()


class UtilTests(TestCase):
    """Test utility functions."""

    def setUp(self):
        UserBook.query.delete()
        Book.query.delete()
        User.query.delete()

        book = Book(
            isbn="1111111111111",
            open_library_id="abcd",
            open_library_images={
                "small": "small_url",
                "medium": "medium_url",
                "large": "large_url"
            },
            open_library_url="fake_url",
            number_of_pages=42,
            publish_date=datetime.datetime.strptime('1969-04-20', '%Y-%m-%d'),
            title="epic fake book title"
        )
        db.session.add(book)
        db.session.commit()

        user = User(username="user1@nodomain.com", password="password1")
        db.session.add(user)
        db.session.commit()

        user_book = UserBook(
            user_id=user.id,
            book_id=book.id
        )
        db.session.add(user_book)
        db.session.commit()

        self.user = user

    def test_lookup_isbn_open_library_new_isbn(self):
        """Make a call to the external API and return a response object."""

        resp = lookup_isbn_open_library("0060935464")

        self.assertIsInstance(resp, requests.models.Response)

    def test_map_response_to_book(self):
        """Maps a reqeuests response to a book object."""

        # this should really be mocked and not an actual external api call
        resp = lookup_isbn_open_library("0060935464")

        book = map_response_to_book(resp, "0060935464")

        self.assertIsInstance(book, Book)

    def test_search_user_books_by_title(self):
        """Return all books for specified user with the search string in the title."""

        books = search_user_books(self.user.id, "title", "book")

        self.assertIsInstance(books[0], Book)
        self.assertEqual(books[0].title, "epic fake book title")

    def test_search_user_books_by_isbn(self):
        """Return all books for a specified user where the search string equals the isbn."""

        books = search_user_books(self.user.id, "isbn", "1111111111111")
        self.assertIsInstance(books[0], Book)
        self.assertEqual(books[0].title, "epic fake book title")
