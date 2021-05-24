"""User, book, tag view tests."""
import datetime
import os
from unittest import TestCase
from models import db, User, Book, Author, Publisher, Subject, SubjectPlace, SubjectPerson, SubjectTime, BookAuthor, \
    BookPublisher, BookSubject, BookSubjectPlace, BookSubjectPerson, BookSubjectTime, UserBook, Tag, UserTag, \
    UserBookTag

os.environ['DATABASE_URL'] = "postgres:///personal_library_test"
os.environ['FLASK_ENV'] = "production"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class UserBookTagViewTestCase(TestCase):
    """Test the views that involve users, books, and tags."""

    def create_user_book(self):
        user_book = UserBook(user_id=self.user.id, book_id=self.book.id)
        db.session.add(user_book)
        db.session.commit()

        return user_book

    def create_tag(self):
        tag = Tag(name='test_tag')
        db.session.add(tag)
        db.session.commit()

        self.tag = tag
        return tag

    def create_user_tag(self):
        user_tag = UserTag(user_id=self.user.id, tag_id=self.tag.id)
        db.session.add(user_tag)
        db.session.commit()

        return user_tag

    def create_user_book_tag(self):
        user_book_tag = UserBookTag(user_id=self.user.id, book_id=self.book.id, tag_id=self.tag.id)
        db.session.add(user_book_tag)
        db.session.commit()

        return user_book_tag

    def setUp(self):
        """Prepare data for tests."""

        User.query.delete()
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
        Tag.query.delete()
        UserTag.query.delete()
        UserBookTag.query.delete()

        user = User(username='test_user@nodomain.com', password='password1')
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

        self.user = user
        self.book = book

    def test_home_not_logged_in(self):
        """When there is no user logged in render the home-anon template."""

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = None

            resp = c.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Welcome to Personal Library', html)

    def test_home_logged_in(self):
        """When there is a user logged in redirect to the user's books page."""

        self.create_user_book()

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.get('/', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("epic fake book title", html)

    def test_search_isbn_not_logged_in(self):
        """If there is no user logged in flash a message and redirect to root route."""

        data = {'isbn': '1111111111111'}
        with app.test_client() as c:
            with c.session_transaction() as s:
                if s.get(CURR_USER_KEY):
                    del s[CURR_USER_KEY]

            resp = c.post('/books/search', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You are not authorized.", html)

    def test_search_isbn_in_collection(self):
        """
        If the submitted isbn is already in the logged in user's collection redirect to the user's book page.
        """

        self.create_user_book()

        data = {'isbn': self.book.isbn}

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.post('/books/search', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Remove from collection", html)

    def test_search_isbn_not_in_collection_not_in_database(self):
        """
        If the submitted isbn is not in the logged in user's collection,
        look it on the external api.
        """

        data = {'isbn': '0060935464'}

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.post('/books/search', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Add to collection", html)

    def test_search_isbn_not_in_collection_in_database(self):
        """
        If the book is in the database but not in the user's collection show the book detail page.
        """

        data = {'isbn': '1111111111111'}

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.post('/books/search', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Add to collection", html)

    def test_book_detail_logged_in(self):
        """Show the book detail with an option for the user to add the book to their collection."""

        url = f'/books/{self.book.id}'

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.get(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Add to collection", html)

    def test_book_detail_not_logged_in(self):
        """If there is no logged in user flash a message and redirect to root route."""

        url = f'/books/{self.book.id}'

        with app.test_client() as c:
            with c.session_transaction() as s:
                if s.get(CURR_USER_KEY):
                    del s[CURR_USER_KEY]

            resp = c.get(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You are not authorized.", html)

    def test_user_books_not_logged_in(self):
        """If there is no logged in user flash a message and redirect to root route."""

        url = f'/users/{self.user.id}/books'

        with app.test_client() as c:
            with c.session_transaction() as s:
                if s.get(CURR_USER_KEY):
                    del s[CURR_USER_KEY]

            resp = c.get(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You are not authorized.", html)

    def test_user_books_wrong_user(self):
        """
        If the user id in the route does not match that of the logged in user,
        flash a message and redirect to the root route.
        """

        url = '/users/0/books'

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.get(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You are not authorized.", html)

    def test_user_books(self):
        """Display the users-books.html page."""

        url = f'/users/{self.user.id}/books'

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.get(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You don't have any books in your collection yet!", html)

    def test_user_book_detail_not_logged_in(self):
        """If there is no logged in user, flash a message and redirect to the root route."""

        url = f'/users/{self.user.id}/books/{self.book.id}'

        with app.test_client() as c:
            with c.session_transaction() as s:
                if s.get(CURR_USER_KEY):
                    del s[CURR_USER_KEY]

            resp = c.get(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You are not authorized.", html)

    def test_user_book_detail_wrong_user(self):
        """
        If the user id in the route does not match that of the logged in user,
        flash a message and redirect to the root route.
        """

        url = f'/users/0/books/{self.book.id}'

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.get(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You are not authorized.", html)

    def test_user_book_detail_wrong_book(self):
        """
        If the book id in the route does not match a book in the collection of the logged in user,
        flash a message and redirect to the root route.
        """

        url = f'/users/{self.user.id}/books/0'

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.get(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Book not found!", html)

    def test_user_book_detail_get(self):
        """On a get request show the detail for the book in the user's collection."""

        self.create_user_book()

        url = f'/users/{self.user.id}/books/{self.book.id}'

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.get(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Remove from collection", html)

    def test_user_book_detail_not_in_collection_post(self):
        """On a post request add the book to the user's collection"""

        url = f'/users/{self.user.id}/books/{self.book.id}'

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.post(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Remove from collection", html)

    def test_user_book_detail_in_collection_post(self):
        """On a post request, if the book is already in the user's collection, show the book detail page."""

        self.create_user_book()

        url = f'/users/{self.user.id}/books/{self.book.id}'

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.post(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Remove from collection", html)

    def test_delete_user_book_not_logged_in(self):
        """If there is no logged in user, flash a message and redirect to the root route."""

        url = f'/users/{self.user.id}/books/{self.book.id}/delete'

        with app.test_client() as c:
            with c.session_transaction() as s:
                if s.get(CURR_USER_KEY):
                    del s[CURR_USER_KEY]

            resp = c.post(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You are not authorized.", html)

    def test_delete_user_book_wrong_user(self):
        """
        If the user id in the route does not match that of the logged in user,
        flash a message and redirect to the root route.
        """

        url = f'/users/0/books/{self.book.id}/delete'

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.post(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You are not authorized.", html)

    def test_delete_user_book_wrong_book(self):
        """
        If the book id in the route does not match a book in the collection of the logged in user,
        flash a message and redirect to the root route.
        """

        url = f'/users/{self.user.id}/books/0/delete'

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.post(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Book not found!", html)

    def test_delete_user_book(self):
        """Remove book from user's collection and redirect to user's books."""

        self.create_user_book()

        self.create_tag()

        self.create_user_tag()

        self.create_user_book_tag()

        url = f'/users/{self.user.id}/books/{self.book.id}/delete'

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.post(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You don't have any books in your collection yet!", html)

        # verify that the tags associated with the user's books have been deleted
        user_book_tags = UserBookTag.query\
            .filter(UserBookTag.user_id == self.user.id, UserBookTag.book_id == self.book.id)\
            .all()

        self.assertFalse(user_book_tags)

    def test_user_tags_not_logged_in(self):
        """If there is no logged in user, flash a message and redirect to the root route."""

        url = f'/users/{self.user.id}/tags'

        with app.test_client() as c:
            with c.session_transaction() as s:
                if s.get(CURR_USER_KEY):
                    del s[CURR_USER_KEY]

            resp = c.get(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You are not authorized.", html)

    def test_user_tags_wrong_user(self):
        """
        If the user id in the route does not match that of the logged in user,
        flash a message and redirect to the root route.
        """

        url = f'/users/0/tags'

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.get(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You are not authorized.", html)

    def test_user_tags(self):
        """Display the tags that the user has created."""

        url = f'/users/{self.user.id}/tags'

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.get(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You have not created any tags yet.", html)

    def test_add_user_tag_not_logged_in(self):
        """If there is no logged in user, flash a message and redirect to the root route."""

        url = f'/users/{self.user.id}/tag'

        with app.test_client() as c:
            with c.session_transaction() as s:
                if s.get(CURR_USER_KEY):
                    del s[CURR_USER_KEY]

            resp = c.post(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You are not authorized.", html)

    def test_add_user_tag_wrong_user(self):
        """
        If the user id in the route does not match that of the logged in user,
        flash a message and redirect to the root route.
        """

        url = f'/users/0/tag'

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.post(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You are not authorized.", html)

    # def test_add_user_tag_get(self):
    #     """Display the add tag form."""
    #
    #     url = f'/users/{self.user.id}/tag'
    #
    #     with app.test_client() as c:
    #         with c.session_transaction() as s:
    #             s[CURR_USER_KEY] = self.user.id
    #
    #         resp = c.get(url, follow_redirects=True)
    #         html = resp.get_data(as_text=True)
    #
    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn("Add a tag", html)

    def test_add_user_tag_new_tag_post(self):
        """Create a user tag and redirect to user's tags page."""

        data = {'tag': 'test_tag'}

        url = f'/users/{self.user.id}/tag'

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.post(url, data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("test_tag", html)

    def test_add_user_tag_existing_tag_post(self):
        """Add an existing tag to the user's tags and redirect to user's tags page."""

        self.create_tag()

        data = {'tag': 'test_tag'}

        url = f'/users/{self.user.id}/tag'

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.post(url, data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("test_tag", html)

    def test_delete_user_tag_not_logged_in(self):
        """If there is no logged in user, flash a message and redirect to the root route."""

        self.create_tag()
        self.create_user_tag()
        self.create_user_book()
        self.create_user_book_tag()

        url = f'/users/{self.user.id}/tag/{self.tag.id}/delete'

        with app.test_client() as c:
            with c.session_transaction() as s:
                if s.get(CURR_USER_KEY):
                    del s[CURR_USER_KEY]

            resp = c.post(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('test_tag', html)

    def test_add_book_tag_not_logged_in(self):
        """If there is no logged in user, flash a message and redirect to the root route."""

        tag = self.create_tag()

        url = f'/users/{self.user.id}/books/{self.book.id}/tag/{tag.id}'

        with app.test_client() as c:
            with c.session_transaction() as s:
                if s.get(CURR_USER_KEY):
                    del s[CURR_USER_KEY]

            resp = c.post(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You are not authorized.", html)

    def test_add_book_tag_wrong_user(self):
        """
        If the user id in the route does not match that of the logged in user,
        flash a message and redirect to the root route.
        """

        tag = self.create_tag()

        self.create_user_tag()

        url = f'/users/0/books/{self.book.id}/tag/{tag.id}'

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.post(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You are not authorized.", html)

    def test_add_book_tag_wrong_book(self):
        """
        If the book id in the route does not match a book in the collection of the logged in user,
        flash a message and redirect to the root route.
        """

        tag = self.create_tag()

        self.create_user_tag()

        url = f'/users/{self.user.id}/books/0/tag/{tag.id}'

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.post(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Book not found!", html)

    def test_add_book_tag_wrong_tag(self):
        """
        If the tag id in the route does not match a tag in the collection of the logged in user,
        flash a message and redirect to the book detail page.
        """

        self.create_user_book()

        self.create_tag()

        self.create_user_tag()

        url = f'/users/{self.user.id}/books/{self.book.id}/tag/0'

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.post(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Tag not found!", html)

    def test_add_book_tag(self):
        """Add the tag to the book and redirect to the book detail page."""

        self.create_user_book()

        tag = self.create_tag()

        self.create_user_tag()

        url = f'/users/{self.user.id}/books/{self.book.id}/tag/{tag.id}'

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.post(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<button formaction="/users/{self.user.id}/books/{self.book.id}/tag/{tag.id}/delete" formmethod="post" class="btn btn-primary btn-sm m-1" id="{tag.id}"><span class="bi bi-dash-square-fill"></span> {tag.name}</button>', html)

    def test_delete_book_tag_not_logged_in(self):
        """If there is no logged in user, flash a message and redirect to the root route."""

        self.create_user_book()

        tag = self.create_tag()

        self.create_user_tag()

        self.create_user_book_tag()

        url = f'/users/{self.user.id}/books/{self.book.id}/tag/{tag.id}/delete'

        with app.test_client() as c:
            with c.session_transaction() as s:
                if s.get(CURR_USER_KEY):
                    del s[CURR_USER_KEY]

            resp = c.post(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You are not authorized.", html)

    def test_delete_book_tag_wrong_user(self):
        """
        If the user id in the route does not match that of the logged in user,
        flash a message and redirect to the root route.
        """

        self.create_user_book()

        tag = self.create_tag()

        self.create_user_tag()

        self.create_user_book_tag()

        url = f'/users/0/books/{self.book.id}/tag/{tag.id}/delete'

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.post(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You are not authorized.", html)

    def test_delete_book_tag_wrong_book(self):
        """
        If the book id in the route does not match a book in the collection of the logged in user,
        flash a message and redirect to the root route.
        """

        self.create_user_book()

        tag = self.create_tag()

        self.create_user_tag()

        self.create_user_book_tag()

        url = f'/users/{self.user.id}/books/0/tag/{tag.id}/delete'

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.post(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Book not found!", html)

    def test_delete_book_tag_wrong_tag(self):
        """
        If the tag id in the route does not match a tag in the collection of the logged in user,
        flash a message and redirect to the book detail page.
        """

        self.create_user_book()

        tag = self.create_tag()

        self.create_user_tag()

        self.create_user_book_tag()

        url = f'/users/{self.user.id}/books/{self.book.id}/tag/0/delete'

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.post(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Tag not found!", html)

    def test_delete_book_tag(self):
        """Delete the tag from the book and redirect to the book detail page."""

        self.create_user_book()

        tag = self.create_tag()

        self.create_user_tag()

        self.create_user_book_tag()

        url = f'/users/{self.user.id}/books/{self.book.id}/tag/{tag.id}/delete'

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.post(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(f'<button formaction="/users/{self.user.id}/books/{self.book.id}/tags/{tag.id}/delete" formmethod="post" class="btn btn-primary btn-sm m-1" id="{tag.id}">{tag.name}</button>', html)

    def test_show_user_book_by_tag_not_logged_in(self):
        """If there is no logged in user, flash a message and redirect to the root route."""

        self.create_user_book()

        tag = self.create_tag()

        self.create_user_tag()

        self.create_user_book_tag()

        url = f'/users/{self.user.id}/tags/{tag.id}'

        with app.test_client() as c:
            with c.session_transaction() as s:
                if s.get(CURR_USER_KEY):
                    del s[CURR_USER_KEY]

            resp = c.get(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You are not authorized.", html)

    def test_show_user_book_by_tag_wrong_user(self):
        """
        If the book id in the route does not match a book in the collection of the logged in user,
        flash a message and redirect to the root route.
        """

        self.create_user_book()

        tag = self.create_tag()

        self.create_user_tag()

        self.create_user_book_tag()

        url = f'/users/0/tags/{tag.id}'

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.get(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You are not authorized.", html)

    def test_show_user_book_by_tag_wrong_tag(self):
        """
        If the tag in the route is not in the user's collection,
        flash a message and redirect to the root route.
        """

        self.create_user_book()

        self.create_tag()

        self.create_user_tag()

        self.create_user_book_tag()

        url = f'/users/{self.user.id}/tags/0'

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.get(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Tag not found!", html)

    def test_show_user_book_by_tag(self):
        """Show the books in the user's collection that have the submitted tag."""

        self.create_user_book()

        tag = self.create_tag()

        self.create_user_tag()

        self.create_user_book_tag()

        url = f'/users/{self.user.id}/tags/{tag.id}'

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.get(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("epic fake book title", html)

    def test_user_books_search_by_title_not_logged_in(self):
        """If there is no logged in user, flash a message and redirect to the root route."""

        self.create_user_book()

        url = f'/users/{self.user.id}/books/search'

        with app.test_client() as c:
            with c.session_transaction() as s:
                if s.get(CURR_USER_KEY):
                    del s[CURR_USER_KEY]

            resp = c.post(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You are not authorized.", html)

    def test_user_books_search_by_title_wrong_user(self):
        """
        If the book id in the route does not match a book in the collection of the logged in user,
        flash a message and redirect to the root route.
        """

        self.create_user_book()

        url = f'/users/0/books/search'

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.post(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You are not authorized.", html)

    def test_user_book_search_by_title(self):
        """Book(s) in the user's collection containing the search string should appear on the results page."""

        self.create_user_book()

        url = f'/users/{self.user.id}/books/search'

        data = {
            "search_field": "title",
            "search_string": "epic fake"
        }

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.post(url, data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("epic fake book title", html)

    def test_user_book_search_by_isbn(self):
        """If there is a book with the matching isbn, then it is displayed on the results page."""

        self.create_user_book()

        url = f'/users/{self.user.id}/books/search'

        data = {
            "search_field": "isbn",
            "search_string": "1111111111111"
        }

        with app.test_client() as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.user.id

            resp = c.post(url, data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("epic fake book title", html)
