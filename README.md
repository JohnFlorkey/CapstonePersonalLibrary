# Personal Library
Hosted on heroku at: https://personal-library-jf.herokuapp.com
## Purpose
This site is intended to help those with large book collections that would find it useful to search their collection 
based on tags that they have created and added to their books.

## Features
* Create user account
* Lookup books by ISBN and add them to the user's collection
* Create tags and apply them to books in the user's collection
* Search the user's collection by partial title or by matching ISBN
* Search the user's collection for all books with a specified tag
* Remove a tag from all books in the user's collection and from the user's collection of tags

## Typical Workflow
1) Create user account
2) Enter an ISBN of a book in your physical book collection in the ISBN text box on the navigation bar and click the 
   "Lookup" button
3) The site will lookup that ISBN using the Open Library API and return book details.
4) Add the book to your collection by clicking the "Add to collection" button.
5) Click "Browse Tags" on the navigation bar and create some tags that categorize this book in a way that is meaningful 
   to you. For example if you need to find books where the characters are animals that behave like humans, you could 
   create an "Anthropomorphic Animals" tag
6) Click "Browse Collection" on the navigation bar. 
7) Click a book cover image
8) Review the book details.
9) Add or remove tags you have previously defined to this book.
10) Click "Browse Collection" on the navigation bar. 
11) Notice the tags that have been applied to the book are visible.
12) Click a tag to see all books in your collection that have the same tag applied.
13) A book search by tag can also be performed on the "Browse Tags" page by clicking a tag.

## Third Party API
The site uses the OpenLibrary API.  
Sample API call: https://openlibrary.org/api/books?bibkeys=ISBN:9780980200447&jscmd=data&format=json

## Tech Stack
Details can be found in [requirements.txt](requirements.txt), but the basics are python, flask, sqlalchemy, bcrypt,
WTForms  
Database: PostrgeSQL