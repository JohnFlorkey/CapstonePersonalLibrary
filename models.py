import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)


class User(db.Model):
    """Model that represents a user of the application."""

    __tablename__ = 'users'

    # properties
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    # the user will user their email address as their username
    username = db.Column(db.Text,
                         nullable=False,
                         unique=True)
    password = db.Column(db.Text,
                         nullable=False)

    # relationships
    books = db.relationship('Book',
                            secondary='users_books',
                            backref=db.backref('users'))
    tags = db.relationship('Tag',
                           secondary='users_tags',
                           backref=db.backref('users'))
    books_tags = db.relationship('UserBookTag')

    @classmethod
    def signup(cls, username, password):
        """Sign up a user with a hashed password and return an instance of the user class"""

        hashed = bcrypt.generate_password_hash(password).decode("utf8")
        user = User(
            username=username,
            password=hashed
        )
        db.session.add(user)

        return user

    @classmethod
    def authenticate(cls, username, password):
        """Attempt to authenticate the user. Return an instance of the user class on success or false on failure"""
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


class Book(db.Model):
    """Model that represents a physical book."""

    __tablename__ = 'books'

    # properties
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    isbn = db.Column(db.Text,
                     nullable=False,
                     unique=True)
    open_library_id = db.Column(db.Text,
                                nullable=False)
    open_library_images = db.Column(db.JSON)
    open_library_url = db.Column(db.Text)
    number_of_pages = db.Column(db.Integer)
    publish_date = db.Column(db.Date)
    title = db.Column(db.Text,
                      nullable=False)

    # relationships
    authors = db.relationship('Author',
                              secondary='books_authors',
                              backref=db.backref('books'))
    publishers = db.relationship('Publisher',
                                 secondary='books_publishers',
                                 backref=db.backref('books'))
    subjects = db.relationship('Subject',
                               secondary='books_subjects',
                               backref=db.backref('books'))
    subject_places = db.relationship('SubjectPlace',
                                     secondary='books_subject_places',
                                     backref=db.backref('books'))
    subject_people = db.relationship('SubjectPerson',
                                     secondary='books_subject_people',
                                     backref=db.backref('books'))
    subject_times = db.relationship('SubjectTime',
                                    secondary='books_subject_times',
                                    backref=db.backref('books'))

    def get_authors(self):
        return ', '.join([author.name for author in self.authors])

    def get_publishers(self):
        return ', '.join([publisher.name for publisher in self.publishers])

    def get_cover_image_url(self, size):
        return self.open_library_images.get(size)

    def get_user_book_tags(self, user_id):
        return db.session.query(Tag)\
            .join(UserBookTag)\
            .filter(UserBookTag.user_id == user_id, UserBookTag.book_id == self.id)\
            .all()


class Author(db.Model):
    """Model that represents the author of a book."""

    __tablename__ = 'authors'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text,
                     nullable=False,
                     unique=True)


class BookAuthor(db.Model):
    """Relates books to authors in a many to many relationship"""

    __tablename__ = 'books_authors'

    book_id = db.Column(db.Integer,
                        db.ForeignKey('books.id', ondelete="cascade"),
                        primary_key=True)
    author_id = db.Column(db.Integer,
                          db.ForeignKey('authors.id'),
                          primary_key=True)


class Publisher(db.Model):
    """Model that represents the publisher of a book."""

    __tablename__ = 'publishers'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text,
                     nullable=False,
                     unique=True)


class BookPublisher(db.Model):
    """Relates books to publishers in a many to many relationship"""

    __tablename__ = 'books_publishers'

    book_id = db.Column(db.Integer,
                        db.ForeignKey('books.id', ondelete="cascade"),
                        primary_key=True)
    publisher_id = db.Column(db.Integer,
                             db.ForeignKey('publishers.id'),
                             primary_key=True)


class Subject(db.Model):
    """Model that represents the subject of a book."""

    __tablename__ = 'subjects'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text,
                     nullable=False,
                     unique=True)


class BookSubject(db.Model):
    """Relates books to subjects in a many to many relationship"""

    __tablename__ = 'books_subjects'

    book_id = db.Column(db.Integer,
                        db.ForeignKey('books.id', ondelete="cascade"),
                        primary_key=True)
    subject_id = db.Column(db.Integer,
                           db.ForeignKey('subjects.id'),
                           primary_key=True)


class SubjectPlace(db.Model):
    """Model that represents a place that is the subject of a book."""

    __tablename__ = 'subject_places'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text,
                     nullable=False,
                     unique=True)


class BookSubjectPlace(db.Model):
    """Relates books to subject places in a many to many relationship"""

    __tablename__ = 'books_subject_places'

    book_id = db.Column(db.Integer,
                        db.ForeignKey('books.id', ondelete="cascade"),
                        primary_key=True)
    subject_place_id = db.Column(db.Integer,
                                 db.ForeignKey('subject_places.id'),
                                 primary_key=True)


class SubjectPerson(db.Model):
    """Model that represents a person that is the subject of a book."""

    __tablename__ = 'subject_people'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text,
                     nullable=False,
                     unique=True)


class BookSubjectPerson(db.Model):
    """Relates books to subject people in a many to many relationship"""

    __tablename__ = 'books_subject_people'

    book_id = db.Column(db.Integer,
                        db.ForeignKey('books.id', ondelete="cascade"),
                        primary_key=True)
    subject_person_id = db.Column(db.Integer,
                                  db.ForeignKey('subject_people.id'),
                                  primary_key=True)


class SubjectTime(db.Model):
    """Model that represents a period in time that is the subject of a book."""

    __tablename__ = 'subject_times'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text,
                     nullable=False,
                     unique=True)


class BookSubjectTime(db.Model):
    """Relates books to subject time periods in a many to many relationship"""

    __tablename__ = 'books_subject_times'

    book_id = db.Column(db.Integer,
                        db.ForeignKey('books.id', ondelete="cascade"),
                        primary_key=True)
    subject_time_id = db.Column(db.Integer,
                                db.ForeignKey('subject_times.id'),
                                primary_key=True)


class UserBook(db.Model):
    """Relates users to books in a many to many relationship"""

    __tablename__ = 'users_books'

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete="cascade"),
                        primary_key=True)
    book_id = db.Column(db.Integer,
                        db.ForeignKey('books.id'),
                        primary_key=True)
    created_date = db.Column(db.DateTime,
                             default=datetime.datetime.now())


class Tag(db.Model):
    """Model that represents a user defined tag for a book."""

    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text,
                     nullable=False,
                     unique=True)


class UserTag(db.Model):
    """Relates users to the tags in a many to many relationship"""

    __tablename__ = 'users_tags'

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete="cascade"),
                        primary_key=True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       primary_key=True)


class UserBookTag(db.Model):
    """Relates a user, a tag and a book in a many to many relationship"""

    __tablename__ = 'users_books_tags'

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete="cascade"),
                        primary_key=True)
    book_id = db.Column(db.Integer,
                        db.ForeignKey('books.id'),
                        primary_key=True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       primary_key=True)
