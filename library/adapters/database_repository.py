from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from library.domain.model import User, Book, BooksInventory, Author, Publisher, Review
from library.adapters.repository import AbstractRepository


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def add_book(self, book: Book):
        with self._session_cm as scm:
            scm.session.add(book)
            scm.commit()

    def add_author(self, author: Author):
        with self._session_cm as scm:
            scm.session.add(author)
            scm.commit()

    def add_review(self, review: Review):
        super().add_review(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        return user

    def book_contains(self, search: str):
        return_list = []
        books = self._session_cm.session.query(Book)
        for i in books:
            name = i.title
            if search not in name:
                continue
            else:
                return_list.append(i)
        return return_list

    def get_all_authors(self):
        authors = self._session_cm.session.query(Author)
        return authors

    def get_all_books(self):
        books = self._session_cm.session.query(Book)
        return books

    #
    def get_author_by_id(self, id: int) -> Author:
        authors = self._session_cm.session.query(Author)
        return next((author for author in authors if author.unique_id == id), None)

    def get_book(self, id: int):
        book = None
        try:
            article = self._session_cm.session.query(Book).filter(Book.book_id == id).one()
            return book
        except NoResultFound:
            # Ignore any exception and return None.
            pass

    def get_book_by_id(self, id_list):
        returnList = []
        books = self._session_cm.session.query(Book)
        for i in id_list:
            returnList.append(next((book for book in books if book.unique_id == i), None))
        return returnList

    def get_reviews(self):
        review = self._session_cm.session.query(Review)
        return review

    def get_number_authors(self):
        return self._session_cm.session.query(Author).count()

    def get_number_of_users(self):
        return self._session_cm.session.query(User).count()

    def get_first_10_books(self):
        books = self._session_cm.session.query(Book)
        first10 = []

        for i in range(0, 11):
            first10.append(books[i])
        return first10

    def get_first_book(self) -> Book:
        return self._session_cm.session.query(Book)[0]

    def get_last_book(self) -> Book:
        return self._session_cm.session.query(Book)[-1]

    def get_number_of_books(self):
        return self._session_cm.session.query(Book).count()

    def get_books_by_author(self, author: Author):
        books = self._session_cm.session.query(Book)
        auth_books = []
        check = False
        for i in books:
            for auth in i.authors:
                if auth == author:
                    auth_books.append(i)
                    continue
            if check:
                check = False
                continue

    def get_release_year_of_next_book(self, book: Book):
        books = self._session_cm.session.query(Book)
        return next((book.release_year for book in books), None)

    def get_book_ids_for_author(self, author_name: str):
        pass
        # article_ids = []
        #
        # # Use native SQL to retrieve article ids, since there is no mapped class for the article_tags table. row =
        # self._session_cm.session.execute('SELECT unique_id FROM authors WHERE author_name = :author_name',
        # {'full_name': author_name}).fetchone()
        #
        # if row is None: # No tag with the name tag_name - create an empty list. article_ids = list() else: tag_id =
        # row[0] # Retrieve article ids of articles associated with the tag. article_ids =
        # self._session_cm.session.execute('SELECT book_id FROM authors WHERE author_id = :full_name ORDER BY book_id
        # ASC',{'author_id': author_id}).fetchall() article_ids = [id[0] for id in book_ids]
        #
        # return article_ids

    def get_release_year_of_previous_book(self, book: Book):
        result = None
        next_book = self._session_cm.session.query(Book).filter(Book._Book__release_year > book.release_year).order_by(
            asc(Book._Book__release_year)).first()

        if next_book is not None:
            result = next_book.release_year

        return result

    def get_books_by_release_year(self, target_year):
        matching_books = list()
        books = self._session_cm.session.query(Book)

        matching_books.append(next((book for book in books if book.release_year == target_year), None))
        return matching_books
        # matching_books = list()
        # for book in self.__books:
        #     if book.release_year == target_year:
        #         matching_books.append(book)
        # return matching_books
