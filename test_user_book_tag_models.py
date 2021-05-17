"""User, Book, Tag model tests."""
import datetime
import os
from unittest import TestCase
from models import db, User, Book, Tag, UserBook, UserTag, UserBookTag

os.environ['DATABASE_URL'] = "postgresql:///personal_library_test"
os.environ['FLASK_ENV'] = "production"

from app import app

db.create_all()


class UserBookTagModelTestCase(TestCase):
    """Test user, book, tag model interactions."""

    def setUp(self):
        """Create sample user data."""

        User.query.delete()
        Book.query.delete()
        Tag.query.delete()
        UserBook.query.delete()
        UserTag.query.delete()

        user = User(username="user1@nodomain.com", password="password1")
        db.session.add(user)
        db.session.commit()

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

        user_book = UserBook(
            user_id=user.id,
            book_id=book.id
        )
        db.session.add(user_book)
        db.session.commit()

        tag1 = Tag(name="tag1")
        tag2 = Tag(name="tag2")
        db.session.add(tag1)
        db.session.add(tag2)
        db.session.commit()

        user_tag1 = UserTag(
            user_id=user.id,
            tag_id=tag1.id
        )
        user_tag2 = UserTag(
            user_id=user.id,
            tag_id=tag2.id
        )
        db.session.add(user_tag1)
        db.session.add(user_tag2)
        db.session.commit()

        user_book_tag_1 = UserBookTag(
            user_id=user.id,
            book_id=book.id,
            tag_id=tag1.id
        )
        user_book_tag_2 = UserBookTag(
            user_id=user.id,
            book_id=book.id,
            tag_id=tag2.id
        )
        db.session.add(user_book_tag_1)
        db.session.add(user_book_tag_2)
        db.session.commit()

        self.user = user
        self.book = book

    def test_user_tags(self):
        """Are tags created and correctly associated to the user."""

        self.assertEqual(len(self.user.tags), 2)
        self.assertIsInstance(self.user.tags[0], Tag)
        self.assertIn("tag1", [tag.name for tag in self.user.tags])
        self.assertIn("tag2", [tag.name for tag in self.user.tags])

    def test_user_books(self):
        """Are books correctly associated to the user."""

        self.assertEqual(len(self.user.books), 1)
        self.assertIsInstance(self.user.books[0], Book)
        self.assertIn("epic fake book title", [book.title for book in self.user.books])

    def test_get_user_book_tags(self):
        """Are the correct tags returned for the specified user and book."""

        self.assertEqual(len(self.book.get_user_book_tags(self.user.id)), 2)
        self.assertIsInstance(self.book.get_user_book_tags(self.user.id)[0], Tag)
        self.assertIn("tag1", [tag.name for tag in self.book.get_user_book_tags(self.user.id)])
        self.assertIn("tag2", [tag.name for tag in self.book.get_user_book_tags(self.user.id)])