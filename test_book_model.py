"""Book model tests."""
import datetime
import os
from unittest import TestCase
from models import db, Book, Author, Publisher, Subject, SubjectPlace, SubjectPerson, SubjectTime, BookAuthor, \
    BookPublisher, BookSubject, BookSubjectPlace, BookSubjectPerson, BookSubjectTime

os.environ['DATABASE_URL'] = "postgres:///personal_library_test"
os.environ['FLASK_ENV'] = "production"

from app import app

db.create_all()


class BookModelTestCase(TestCase):
    """Test book model."""

    def setUp(self):
        """Create sample book data."""

        Book.query.delete()
        Author.query.delete()
        Publisher.query.delete()
        Subject.query.delete()
        SubjectPlace.query.delete()
        SubjectPerson.query.delete()
        SubjectTime.query.delete()
        BookAuthor.query.delete()
        BookPublisher.query.delete()
        BookSubject.query.delete()
        BookSubjectPlace.query.delete()
        BookSubjectPerson.query.delete()
        BookSubjectTime.query.delete()

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

        author1 = Author(name="Author The First")
        author2 = Author(name="Author The Second")
        db.session.add(author1)
        db.session.add(author2)
        db.session.commit()

        book_author1 = BookAuthor(book_id=book.id, author_id=author1.id)
        book_author2 = BookAuthor(book_id=book.id, author_id=author2.id)
        db.session.add(book_author1)
        db.session.add(book_author2)
        db.session.commit()

        publisher = Publisher(name="Publishing House")
        db.session.add(publisher)
        db.session.commit()

        book_publisher1 = BookPublisher(book_id=book.id, publisher_id=publisher.id)
        db.session.add(book_publisher1)
        db.session.commit()

        subject1 = Subject(name="subject1")
        subject2 = Subject(name="subject2")
        db.session.add(subject1)
        db.session.add(subject2)
        db.session.commit()

        book_subject1 = BookSubject(book_id=book.id, subject_id=subject1.id)
        book_subject2 = BookSubject(book_id=book.id, subject_id=subject2.id)
        db.session.add(book_subject1)
        db.session.add(book_subject2)
        db.session.commit()

        subject_place1 = SubjectPlace(name="subject_place1")
        subject_place2 = SubjectPlace(name="subject_place2")
        db.session.add(subject_place1)
        db.session.add(subject_place2)
        db.session.commit()

        book_subject_place1 = BookSubjectPlace(book_id=book.id, subject_place_id=subject_place1.id)
        book_subject_place2 = BookSubjectPlace(book_id=book.id, subject_place_id=subject_place2.id)
        db.session.add(book_subject_place1)
        db.session.add(book_subject_place2)
        db.session.commit()

        subject_person1 = SubjectPerson(name="subject_person1")
        subject_person2 = SubjectPerson(name="subject_person2")
        db.session.add(subject_person1)
        db.session.add(subject_person2)
        db.session.commit()

        book_subject_person1 = BookSubjectPerson(book_id=book.id, subject_person_id=subject_person1.id)
        book_subject_person2 = BookSubjectPerson(book_id=book.id, subject_person_id=subject_person2.id)
        db.session.add(book_subject_person1)
        db.session.add(book_subject_person2)
        db.session.commit()

        subject_time1 = SubjectTime(name="subject_time1")
        subject_time2 = SubjectTime(name="subject_time2")
        db.session.add(subject_time1)
        db.session.add(subject_time2)
        db.session.commit()

        book_subject_time1 = BookSubjectTime(book_id=book.id, subject_time_id=subject_time1.id)
        book_subject_time2 = BookSubjectTime(book_id=book.id, subject_time_id=subject_time2.id)
        db.session.add(book_subject_time1)
        db.session.add(book_subject_time2)
        db.session.commit()

        self.book = book

    def tearDown(self):
        """Rollback any open transactions"""

        db.session.rollback()

    def test_book_model(self):
        """Does the basic model work?"""

        images = {
                "small": "small_url",
                "medium": "medium_url",
                "large": "large_url"
        }

        self.assertEqual(self.book.isbn, "1111111111111")
        self.assertEqual(self.book.open_library_id, "abcd")
        self.assertEqual(self.book.open_library_images, images)
        self.assertEqual(self.book.open_library_url, "fake_url")
        self.assertEqual(self.book.number_of_pages, 42)
        self.assertEqual(self.book.title, "epic fake book title")

    def test_book_authors(self):
        """Are authors created and correctly associated with the book."""

        self.assertEqual(len(self.book.authors), 2)
        self.assertIsInstance(self.book.authors[0], Author)
        self.assertIn("Author The First", [author.name for author in self.book.authors])
        self.assertIn("Author The Second", [author.name for author in self.book.authors])

    def test_book_publisher(self):
        """Are publishers create and correctly associated with the book."""

        self.assertEqual(len(self.book.publishers), 1)
        self.assertIsInstance(self.book.publishers[0], Publisher)
        self.assertIn("Publishing House", [publisher.name for publisher in self.book.publishers])

    def test_book_subjects(self):
        """Are subjects created and correctly associated with the book."""

        self.assertEqual(len(self.book.subjects), 2)
        self.assertIsInstance(self.book.subjects[0], Subject)
        self.assertIn("subject1", [subject.name for subject in self.book.subjects])
        self.assertIn("subject2", [subject.name for subject in self.book.subjects])

    def test_book_subject_places(self):
        """Are subject_places created and correctly associated with the book."""

        self.assertEqual(len(self.book.subject_places), 2)
        self.assertIsInstance(self.book.subject_places[0], SubjectPlace)
        self.assertIn("subject_place1", [subject_place.name for subject_place in self.book.subject_places])
        self.assertIn("subject_place2", [subject_place.name for subject_place in self.book.subject_places])

    def test_book_subject_people(self):
        """Are subject_people created and correctly associated with the book."""

        self.assertEqual(len(self.book.subject_people), 2)
        self.assertIsInstance(self.book.subject_people[0], SubjectPerson)
        self.assertIn("subject_person1", [subject_person.name for subject_person in self.book.subject_people])
        self.assertIn("subject_person2", [subject_person.name for subject_person in self.book.subject_people])

    def test_book_subject_time(self):
        """Are subject_times created and correctly associated with the book."""

        self.assertEqual(len(self.book.subject_times), 2)
        self.assertIsInstance(self.book.subject_times[0], SubjectTime)
        self.assertIn("subject_time1", [subject_time.name for subject_time in self.book.subject_times])
        self.assertIn("subject_time2", [subject_time.name for subject_time in self.book.subject_times])

    def test_get_authors(self):
        """Does the get_authors class method return a comma separated string of authors."""

        self.assertEqual(self.book.get_authors(), "Author The First, Author The Second")

    def test_get_publishers(self):
        """Does the get_publishers class method return a comma separated string of authors."""

        self.assertEqual(self.book.get_publishers(), "Publishing House")

    def test_get_cover_image_url(self):
        """Does the get_cover_image_url class method return a url based on the passed in key."""

        self.assertEqual(self.book.get_cover_image_url("medium"), "medium_url")
