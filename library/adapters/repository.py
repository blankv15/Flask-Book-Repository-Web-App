import abc
from typing import List
from datetime import date
from library.adapters.jsondatareader import BooksJSONReader
from library.domain.model import Publisher, Author, Book, Review, User, BooksInventory

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_book(self, book: Book):
        raise NotImplementedError

    @abc.abstractmethod
    def book_contains(self, search: str):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        """ Returns the User named user_name from the repository.

        If there is no User with the given user_name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_author(self, author: Author):
        """ Adds an Article to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_author_by_id(self, id: int) -> Author:
        """ Returns a list of Articles that were published on target_date.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_by_author(self, author: Author):
        """ Returns the number of Articles in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_books(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_books(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_authors(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_authors(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_book(self) -> Book:
        """ Returns the first Article, ordered by date, from the repository.

        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_book(self) -> Book:
        """ Returns the last Article, ordered by date, from the repository.

        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_10_books(self):
        """ Returns the last Article, ordered by date, from the repository.

        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_release_year_of_previous_book(self, book: Book):
        """ Returns the date of an Article that immediately precedes article.

        If article is the first Article in the repository, this method returns None because there are no Articles
        on a previous date.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_release_year_of_next_book(self, book: Book):
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_by_release_year(self, target_year):
        raise NotImplementedError

    @abc.abstractmethod
    def get_book_by_id(self, id_list):
        raise NotImplementedError

    @abc.abstractmethod
    def get_book(self, id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Comment not correctly attached to a User')
        if review.book is None or review not in review.book.reviews:
            raise RepositoryException('Comment not correctly attached to an Article')

    @abc.abstractmethod
    def get_reviews(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_book_ids_for_author(self, author_name: str):
        """ Returns a list of ids representing Articles that are tagged by tag_name.

        If there are Articles that are tagged by tag_name, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_books(self):
        """ Returns a list of ids representing Articles that are tagged by tag_name.

        If there are Articles that are tagged by tag_name, this method returns an empty list.
        """
        raise NotImplementedError
