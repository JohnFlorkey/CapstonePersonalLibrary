import os
from flask import Flask, request, render_template, redirect, session, g, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, Book, User, UserBook, Tag, UserTag, UserBookTag
from forms import UserForm
from utils import lookup_isbn_open_library, map_response_to_book

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///personal_library'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

CURR_USER_KEY = 'curr_user'


@app.before_request
def add_user_to_g():
    """If there is a logged in user, add curr_user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None


def do_login(user):
    """Log the user in."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Lof the user out."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/')
def home():
    """Redirect the user to the appropriate route based on whether or not they are logged in."""

    if g.user:
        return render_template('user.html', user=g.user)
    else:
        return render_template('home-anon.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Sign up a user."""

    form = UserForm()

    import pdb
    pdb.set_trace()

    if form.validate_on_submit():
        user = User.signup(
            username=form.username.data,
            password=form.password.data
        )
        db.session.commit()

        do_login(user)

        return redirect('/')

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log the user in."""

    form = UserForm()

    if form.validate_on_submit():
        user = User.authenticate(
            username=form.username.data,
            password=form.password.data
        )
        if user:
            do_login(user)
            return redirect('/')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Log the user out."""

    do_logout()
    flash("successfully logged out.", "success")

    return redirect('/')


@app.route('/users/<int:user_id>')
def user_home(user_id):
    """Displays the user's main page."""

    if g.user.id != user_id:
        flash("You are not authorized.", "danger")
        return redirect('/')

    return render_template('user.html', user=g.user)


@app.route('/books/search', methods=['POST'])
def search_isbn():
    """
    Lookup up the isbn submitted by the user in the application database.
    If the book is in the user's collection, redirect to the user's book page.
    If the book is in the database but not in the user's collection, redirect to the book's page.
    If not found in the application database, make a call to the external api and add the response to the application
    database.
    """

    isbn = request.form.get('isbn')
    if g.user:
        user = g.user

    book = Book.query.filter_by(isbn=isbn).first()
    if book:
        if user.id in book.users:
            return redirect('/users/{user_id}/books/{book_id}')
    else:
        resp = lookup_isbn_open_library(isbn)
        book = map_response_to_book(resp, isbn)
        db.session.add(book)
        db.session.commit()
    return redirect(f'/books/{book.id}')


@app.route('/books/<int:book_id>', methods=['GET', 'POST'])
def book_detail(book_id):
    book = Book.query.get(book_id)

    return render_template('book-detail.html', book=book)


@app.route('/users/<int:user_id>/books', methods=['GET'])
def user_books(user_id):
    """Show the user's 10 most recently added books."""

    import pdb
    pdb.set_trace()

    if g.user.id != user_id:
        flash('You are not authorized!', 'danger')
        return redirect('/')

    if len(g.user.books) == 0:
        return redirect('/')

    books = db.session.query(Book).join(UserBook).filter(UserBook.user_id == user_id).all()

    return render_template('user-books.html', books=books)


@app.route('/users/<int:user_id>/books/<int:book_id>', methods=['GET', 'POST'])
def user_book_detail(user_id, book_id):
    """Add a book to the user's collection or display the book that is already in the user's collection."""

    if g.user.id != user_id:
        flash('You are not authorized!', 'danger')
        return redirect('/')

    book = Book.query.filter_by(id=book_id).first()
    if not book:
        flash('Book not found!', 'danger')
        return redirect('/')

    if request.method == 'GET':
        import pdb
        pdb.set_trace()

        in_collection = book_id in [user_book.id for user_book in g.user.books]
        # Get the tags applied to this book by this user
        book_tags = db.session.query(Tag) \
            .join(UserBookTag) \
            .filter(
            UserBookTag.user_id == user_id,
            UserBookTag.book_id == book_id
            ) \
            .all()
        all_tags = db.session.query(Tag) \
            .join(UserTag) \
            .filter(UserTag.user_id == user_id) \
            .all()
        available_tags = [tag for tag in all_tags if tag not in book_tags]

        return render_template(
            'book-detail.html',
            book=book,
            user=g.user,
            book_tags=book_tags,
            available_tags=available_tags,
            in_collection=in_collection
        )

    if request.method == 'POST':
        book_user = UserBook(
            user_id=user_id,
            book_id=book_id
        )
        db.session.add(book_user)
        db.session.commit()

        return redirect(f'/users/{user_id}/books/{book_id}')


@app.route('/users/<int:user_id>/books/<int:book_id>/delete', methods=['POST'])
def delete_user_book(user_id, book_id):
    """Remove a book from a user's collection."""

    if g.user.id != user_id:
        flash('You are not authorized!', 'danger')
        return redirect('/')

    if book_id not in [book.id for book in g.user.books]:
        flash('Book not found!', 'danger')
        return redirect('/')

    user_book = db.session.query(UserBook).filter(UserBook.user_id == user_id, UserBook.book_id == book_id).first()
    db.session.delete(user_book)
    db.session.commit()

    return redirect(f'/users/{user_id}/books')


@app.route('/users/<int:user_id>/tags', methods=['GET'])
def user_tags(user_id):
    """
    GET: Show the tags the user has defined.
    POST: Create a new user tag.
    """

    if g.user.id != user_id:
        flash('You are not authorized!', 'danger')
        return redirect('/')

    return render_template('user-tags.html', user=g.user)


@app.route('/users/<int:user_id>/tag', methods=['GET', 'POST'])
def add_user_tag(user_id):
    """
    GET: Show the add user tag form.
    POST: Create a user tag.
    """

    if g.user.id != user_id:
        flash('You are not authorized!', 'danger')
        return redirect('/')

    if request.method == 'GET':
        return render_template('add-user-tag.html', user=g.user)

    if request.method == 'POST':
        tag_name = request.form.get('tag')
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            new_tag = Tag(name=tag_name)
            db.session.add(new_tag)
            db.session.commit()

        tag = new_tag if new_tag else tag

        user_tag = UserTag(
            user_id=g.user.id,
            tag_id=tag.id
        )
        db.session.add(user_tag)
        db.session.commit()

        return redirect(f'/users/{g.user.id}/tags')


@app.route('/users/<int:user_id>/books/<int:book_id>/tags/<int:tag_id>', methods=['POST', 'DELETE'])
def add_book_tag(user_id, book_id, tag_id):
    """Add a tag to a book in a user's collection."""

    user_books = db.session.query(Book).join(UserBook).filter(UserBook.user_id == user_id).all()
    if book_id not in [book.id for book in user_books]:
        return jsonify(False)

    user_tags = db.session.query(Tag).join(UserTag).filter(UserTag.user_id == user_id).all()
    if tag_id not in [tag.id for tag in user_tags]:
        return jsonify(False)

    if request.method == 'POST':
        book_tag = UserBookTag(
            user_id=user_id,
            book_id=book_id,
            tag_id=tag_id
        )
        db.session.add(book_tag)
        db.session.commit()

    if request.method == 'DELETE':
        user_book_tag = UserBookTag.query.filter_by(user_id=user_id, book_id=book_id, tag_id=tag_id).first()
        db.session.delete(user_book_tag)
        db.session.commit()

    return jsonify(True)


@app.route('/users/<int:user_id>/tags/<int:tag_id>')
def show_user_book_by_tag(user_id, tag_id):
    """Show all the books in the user's collection with the specified tag."""

    books = db.session.query(Book)\
        .join(UserBookTag)\
        .filter(UserBookTag.user_id == user_id, UserBookTag.tag_id == tag_id)\
        .all()

    return render_template('user-books.html', books=books)
