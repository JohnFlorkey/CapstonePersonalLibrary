import requests
from datetime import datetime
from dateutil.parser import parse
from flask import flash
from models import Book, Author, Publisher, Subject, SubjectPlace, SubjectPerson, SubjectTime

DEFAULT_DATE = datetime(1900, 1, 1)


def lookup_isbn_open_library(isbn):
    """
    Check the database to see if the book has already been added to the database by another user.
    If it is not there, send a get request to external api looking for book data by isbn.
    """

    params = {
        'bibkeys': f'ISBN:{isbn}',
        'jscmd': 'data',
        'format': 'json'
    }
    resp = requests.get(f'https://openlibrary.org/api/books', params=params)
    if resp.status_code == 500:
        flash('Open Library API is down.')
    elif resp.status_code > 400:
        flash('The requested resource could not be found.')
    return resp


def map_response_to_book(resp, isbn):
    """Maps an external api response to a book object."""

    data = resp.json()
    data_key = data[f'ISBN:{isbn}']
    book = Book(
        isbn=isbn,
        open_library_id=data_key.get('key'),
        open_library_image_id=data_key.get('cover').get('medium') if data_key.get('cover') else None,
        open_library_url=data_key.get('url'),
        number_of_pages=data_key.get('number_of_pages'),
        publish_date=parse(data_key.get('publish_date'), default=DEFAULT_DATE),
        title=data_key.get('title')
    )
    # build list of authors, adding new authors as needed
    if data_key.get('authors'):
        for item in data_key.get('authors'):
            author = Author.query.filter_by(name=item.get('name')).first()
            if not author:
                new_author = Author(name=item.get('name'))
                book.authors.append(new_author)
            else:
                book.authors.append(author)

    # build list of publishers, creating new publishers as needed
    if data_key.get('publishers'):
        for item in data_key.get('publishers'):
            publisher = Publisher.query.filter_by(name=item.get('name')).first()
            if not publisher:
                new_publisher = Publisher(name=item.get('name'))
                book.publishers.append(new_publisher)
            else:
                book.publishers.append(publisher)

    # build list of subjects, creating new subjects as needed
    if data_key.get('subjects'):
        for item in data_key.get('subjects'):
            subject = Subject.query.filter_by(name=item.get('name')).first()
            if not subject:
                new_subject = Subject(name=item.get('name'))
                book.subjects.append(new_subject)
            else:
                book.subjects.append(subject)

    # Build list of subject places, creating new subject places as needed
    if data_key.get('subject_places'):
        for item in data_key.get('subject_places'):
            subject_place = SubjectPlace.query.filter_by(name=item.get('name')).first()
            if not subject_place:
                new_subject_place = SubjectPlace(name=item.get('name'))
                book.subject_places.append(new_subject_place)
            else:
                book.subject_places.append(subject_place)

    # build list of subject_people, creating new subject people as needed
    if data_key.get('subject_people'):
        for item in data_key.get('subject_people'):
            subject_person = SubjectPerson.query.filter_by(name=item.get('name')).first()
            if not subject_person:
                new_subject_person = SubjectPerson(name=item.get('name'))
                book.subject_people.append(new_subject_person)
            else:
                book.subject_people.append(subject_person)

    # build list of subject times, creating new subject times as needed
    if data_key.get('subject_times'):
        for item in data_key.get('subject_times'):
            subject_time = SubjectTime.query.filter_by(name=item.get('name')).first()
            if not subject_time:
                new_subject_time = SubjectTime(name=item.get('name'))
                book.subject_times.append(new_subject_time)
            else:
                book.subject_times.append(subject_time)

    return book
