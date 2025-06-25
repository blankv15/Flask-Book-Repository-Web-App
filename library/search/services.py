from typing import List, Iterable

from library.adapters.repository import AbstractRepository
from library.domain.model import Book, Review, Publisher, Author, User, BooksInventory, make_review


def get_book_by_search(repo: AbstractRepository, search: str):
    searched_books = repo.book_contains(search)
    print(searched_books)
    return searched_books
