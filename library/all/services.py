from typing import List, Iterable

from library.adapters.repository import AbstractRepository
from library.domain.model import Book, Review, Publisher, Author, User, BooksInventory, make_review


def get_all_books(repo: AbstractRepository):
    books = repo.get_all_books()
    return books


def get_first_book(repo: AbstractRepository):
    book = repo.get_first_book()

    return book_to_dict(book)


def get_last_book(repo: AbstractRepository):
    book = repo.get_last_book()
    return book_to_dict(book)


def get_reviews(repo: AbstractRepository):
    reviews = repo.get_reviews()
    return reviews_to_dict(reviews)

##########################################

def book_to_dict(book: Book):
    book_dict = {
        'id': book.book_id,
        'title': book.title,
        'description': book.description,
        # 'publisher': book.publisher,
        'authors': book.authors,
        'release_year': book.release_year,
        'ebook': book.ebook,
        'cover_url': book.cover_url,
        # 'review': reviews_to_dict(book.r)
    }
    return book_dict

def books_to_dict(books: Iterable[Book]):
    return [book_to_dict(book) for book in books]


def review_to_dict(review: Review):
    review_dict = {
        'book': review.book,
        'review_text': review.review_text,
        'rating': review.rating,
        'timestamp': review.timestamp
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]