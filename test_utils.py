"""Util function tests."""
import os
from unittest import TestCase
import requests
from models import db, User, Book, Tag, UserBook, UserTag, UserBookTag
from utils import lookup_isbn_open_library, map_response_to_book

os.environ['DATABASE_URL'] = "postgresql:///personal_library_test"
os.environ['FLASK_ENV'] = "production"

from app import app

db.create_all()


class UtilTests(TestCase):
    """Test utility functions."""

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