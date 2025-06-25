from datetime import date, datetime
from typing import List

import pytest
from library.domain.model import Book, Review, Publisher, Author, User, BooksInventory, make_review
from library.adapters.repository import RepositoryException




def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_book_count(in_memory_repo):
    number_of_articles = in_memory_repo.get_number_of_books()

    # Check that the query returned 6 Articles.
    assert number_of_articles == 20


def test_repository_can_add_book(in_memory_repo):
    book = Book(22, "Harry Potter")
    in_memory_repo.add_book(book)

    assert in_memory_repo.get_book_by_id(22) == book


def test_repository_can_retrieve_book(in_memory_repo):
    in_memory_repo.add_book(Book(12345,"abcd"))
    test = in_memory_repo.get_book_by_id(12345)

    # Check that the Article has the expected title.
    assert test.title == 'abcd'


def test_repository_does_not_retrieve_a_non_existent_book(in_memory_repo):
    book = in_memory_repo.get_book_by_id(69)
    assert book is None


def test_get_book_by_search(in_memory_repo):
    contains_list = in_memory_repo.book_contains('Switchblade')
    assert contains_list[0].title == "The Switchblade Mamma"


def test_add_author_and_get_by_id(in_memory_repo):
    before = in_memory_repo.get_number_authors()
    in_memory_repo.add_author(Author(69, "Test Name"))
    after = in_memory_repo.get_number_authors()

    assert before == after

