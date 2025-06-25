from datetime import date, datetime

import pytest

import library.adapters.repository as repo
from library.adapters.database_repository import SqlAlchemyRepository
from library.domain.model import User, Book, Review, Author
from library.adapters.repository import RepositoryException


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repo.add_user(user)

    repo.add_user(User('Martin', '123456789'))

    user2 = repo.get_user('Dave')

    assert user2 == user and user2 is user


def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_book_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_articles = repo.get_number_of_books()

    # Check that the query returned 177 Articles.
    assert number_of_articles == 40


def test_repository_can_add_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    before = repo.get_number_of_books()

    book = Book(1234, "test_book")
    book.release_year = 2010
    book.add_author(Author(123, "test_author"))
    book.cover_url = "as"
    book.description = "as"

    repo.add_book(book)
    getBook = repo.get_book(1234)

    assert getBook == getBook


def test_get_number_of_authors(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    assert repo.get_number_authors() == 70


def test_get_number_of_users(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert repo.get_number_of_users() == 3
