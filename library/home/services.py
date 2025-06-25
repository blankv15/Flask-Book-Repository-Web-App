from typing import List, Iterable


from library.adapters.repository import AbstractRepository
from library.domain.model import Book, Review, Publisher, Author, User, BooksInventory, make_review


class NonExistentBookException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def get_first_10_books(repo: AbstractRepository):
    tenBooks = []
    for i in repo.get_first_10_books():
        tenBooks.append(book_to_dict(tenBooks))


def book_to_dict(book: Book):
    book_dict = {
        'title': Book.title,
        'description': Book.description,
        # 'publisher': Book.publisher,
        'authors': Book.authors,
        'release_year': Book.release_year,
        'ebook': Book.ebook,
        'isbn': Book.book_id
        # 'reviews': tags_to_dict(book.reviews)
    }
    return book_dict
