from typing import List, Iterable

from library.adapters.repository import AbstractRepository
from library.domain.model import Book, Review, Publisher, Author, User, BooksInventory, make_review


class NonExistentBookException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_review(review_text: str, user_name, book_id: int, rating: int, repo: AbstractRepository):
    # Check that the book exists.
    book = repo.get_book(book_id)
    if book is None:
        raise NonExistentBookException

    user = repo.get_user(user_name)

    #if user is None:
    #    raise UnknownUserException

    review = make_review(review_text, user, book, rating)

    # Update the repository.
    repo.add_review(review)


'''def get_reviews(book_id, repo: AbstractRepository):
    review_list = []
    all_reviews = repo.get_reviews()
    for review in all_reviews:
        if review.book_id == book_id:
            review_list.append(review)
    return review_list'''


def get_book(book_id: int, repo: AbstractRepository):
    book = repo.get_book(book_id)

    if book is None:
        raise NonExistentBookException

    return book_to_dict(book)


def get_first_book(repo: AbstractRepository):
    book = repo.get_first_book()

    return book_to_dict(book)


def get_last_book(repo: AbstractRepository):
    book = repo.get_last_book()
    return book_to_dict(book)


# same function as get comments by date
def get_books_by_release_year(release_year, repo: AbstractRepository):
    # generic browsing, later make methods browsing by author, release_year and publisher
    # Returns books for the target release_year (empty if no matches), the release_year of the previous book (might be null),
    # the release_year of the next book (might be null)

    books = repo.get_books_by_release_year(release_year)

    books_dto = list()
    prev_release_year = next_release_year = None

    if len(books) > 0:
        prev_release_year = repo.get_release_year_of_previous_book(books[0])
        next_release_year = repo.get_release_year_of_next_book(books[0])

        # Convert Books to dictionary form.
        books_dto = books_to_dict(books)
    return books_dto, prev_release_year, next_release_year


def get_books_by_id(id_list, repo: AbstractRepository):
    books = repo.get_books_by_id(id_list)

    # Convert Books to dictionary form.
    books_as_dict = books_to_dict(books)

    return books_as_dict


def get_reviews_for_book(book_id, repo: AbstractRepository):
    book = repo.get_book(book_id)

    if book is None:
        raise NonExistentBookException

    return reviews_to_dict(book.reviews)


def get_reviews(repo: AbstractRepository):
    reviews = repo.get_reviews()
    return reviews_to_dict(reviews)


def get_book_ids_for_author(author_name, repo: AbstractRepository):
    book_ids = repo.get_book_ids_for_author(author_name)

    return book_ids


def get_all_books(repo: AbstractRepository):
    books = repo.get_all_books()

    return books

# ============================================
# Functions to convert model entities to dicts
# ============================================


def book_to_dict(book: Book):
    book_dict = {
        'id': book.book_id,
        'title': book.title,
        'description': book.description,
        # 'publisher': book.publisher,
        'authors': book.authors,
        'release_year': book.release_year,
        'ebook': book.ebook,
        'cover_url': book.cover_url
        # 'reviews': tags_to_dict(book.reviews)
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


# ============================================
# Functions to convert dicts to model entities
# ============================================
def dict_to_book(dict):
    book = Book(dict.book_id, dict.title)
    return book


def dict_to_review(dict):
    book = dict.book
    return book
