from app import db
from models import Book, Author, BookAuthor
import datetime

db.drop_all()
db.create_all()

# create sample books
# book1 = Book(
#     isbn='fake_isbn_1',
#     open_library_id='fake_OL_id_1',
#     open_library_images=None,
#     open_library_url='fake_OL_url_1',
#     number_of_pages=42,
#     publish_date=datetime.datetime.now(),
#     title='Epic book title, the first'
# )
# book2 = Book(
#     isbn='fake_isbn_2',
#     open_library_id='fake_OL_id_2',
#     open_library_images=None,
#     open_library_url='fake_OL_url_2',
#     number_of_pages=43,
#     publish_date=datetime.datetime.now(),
#     title='Epic book title, the second'
# )
# db.session.add_all([book1, book2])
# db.session.commit()
#
# # create some sample authors
# author1 = Author(name='Piers Anthony')
# author2 = Author(name='Neil Gaiman')
#
# db.session.add_all([author1, author2])
# db.session.commit()
#
# # assign author(s) to book(s)
# book_author1 = BookAuthor(book_id=book1.id, author_id=author1.id)
# book_author2 = BookAuthor(book_id=book1.id, author_id=author2.id)
# book_author3 = BookAuthor(book_id=book2.id, author_id=author1.id)
#
# db.session.add_all([book_author1, book_author2, book_author3])
# db.session.commit()
