import csv
from abc import ABC
from pathlib import Path
from datetime import date, datetime
from typing import List

from werkzeug.security import generate_password_hash

from library.adapters.jsondatareader import BooksJSONReader
from library.adapters.repository import AbstractRepository, RepositoryException
from library.adapters.jsondatareader import BooksJSONReader
from library.domain.model import User, Author, Publisher, Book, BooksInventory, Review, make_review
from bisect import bisect, bisect_left, insort_left


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__books = list()
        self.__authors = list()
        self.__publisher = list()
        self.__users = list()
        self.__reviews = list()
        self.__books_index = dict()

    def add_user(self, user: User):
        self.__users.append(user)

    def add_book(self, book: Book):
        insort_left(self.__books, book)
        self.__books_index[book.book_id] = book

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)

    def book_contains(self, search: str):
        return_list = []
        for i in self.__books:
            title = i.title
            if search in title:
                return_list.append(i)
        return return_list



    def add_author(self, author: Author):
        if type(Author) == Author and author not in self.__authors:
            self.__authors.append(author)

    def get_all_books(self):
        return self.__books

    def get_all_authors(self):
        return self.__authors

    def get_all_authors(self):
        return self.__authors

    def get_author_by_id(self, id: int) -> Author:
        return next((author for author in self.__authors if author.unique_id == id), None)

    def get_books_by_release_year(self, target_year):

        matching_books = list()
        for book in self.__books:
            if book.release_year == target_year:
                matching_books.append(book)
        return matching_books

    def book_index(self, book: Book):
        index = bisect_left(self.__books, book)
        if index != len(self.__books) and self.__books[index].release_year == book.release_year:
            return index
        raise ValueError

    def get_release_year_of_previous_book(self, book: Book):
        previous_year = None

        try:
            index = self.book_index(book)
            for stored_book in reversed(self.__books[0:index]):
                if stored_book.release_year < book.release_year:
                    previous_year = stored_book.release_year
                    break
        except ValueError:
            # No earlier books, so return None.
            pass

        return previous_year

    def get_release_year_of_next_book(self, book: Book):
        next_year = None
        try:
            index = self.book_index(book)
            for stored_book in self.__books[index + 1:len(self.__books)]:
                if stored_book.release_year > book.release_year:
                    next_year = stored_book.release_year
                    break
        except ValueError:
            # No subsequent articles, so return None.
            pass
        return next_year

    def get_book_by_id(self, id_list):
        for i in self.__books:
            if i.book_id == id_list:
                return i

    def get_books_by_author(self, author: Author):

        matching_books = list()
        for book in self.__books:
            for i in book.authors:
                if author.unique_id == i.unique_id:
                    matching_books.append(book)
        return matching_books

    def get_book(self, id: int):
        book = None

        try:
            book = self.__books_index[id]
        except KeyError:
            pass  # Ignore exception and return None.

        return book

    def get_number_of_books(self):
        return len(self.__books)

    def get_number_authors(self):
        return len(self.__authors)

    def get_first_book(self) -> Book:
        book = None

        if len(self.__books) > 0:
            book = self.__books[0]
        return book

    def get_last_book(self) -> Book:
        book = None

        if len(self.__books) > 0:
            book = self.__books[-1]
        return book

    def get_first_10_books(self):
        return self.__books[0:9]

    def add_review(self, review: Review):
        # call parent class first, add_comment relies on implementation of code common to all derived classes
        super().add_review(review)
        self.__reviews.append(review)

    def get_reviews(self):
        return self.__reviews

    def get_book_ids_for_author(self, author_name: str):
        # Linear search, to find the first occurrence of a Tag with the name tag_name.
        author = next((author for author in self.__authors if author.author_name == author_name), None)

        # Retrieve the ids of articles associated with the Tag.
        if author is not None:
            book_ids = [book.id for book in author.tagged_articles]
        else:
            # No Tag with name tag_name, so return an empty list.
            book_ids = list()

        return book_ids

    def get_all_books(self):
        return self.__books


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_books(data_path: Path, repo: MemoryRepository):
    allBooks = BooksJSONReader(data_path / "comic_books_excerpt.json", data_path / "book_authors_excerpt.json")
    allBooks.read_json_files()

    for i in allBooks.dataset_of_books:
        repo.add_book(i)


def load_authors(data_path: Path, repo: MemoryRepository):
    allBooks = BooksJSONReader(data_path / "comic_books_excerpt.json", data_path / "book_authors_excerpt.json")
    allBooks.read_json_files()


def load_users(data_path: Path, repo: MemoryRepository):
    users = dict()

    users_filename = str(Path(data_path) / "users.csv")
    for data_row in read_csv_file(users_filename):
        user = User(
            user_name=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users


def populate(data_path: Path, repo: MemoryRepository):
    load_books(data_path, repo)

    load_authors(data_path, repo)

    load_users(data_path, repo)


def load_reviews(data_path: Path, repo: MemoryRepository, users):
    comments_filename = str(Path(data_path) / "comments.csv")
    for data_row in read_csv_file(comments_filename):
        comment = Review(
            comment_text=data_row[3],
            user=users[data_row[1]],
            article=repo.get_article(int(data_row[2])),
            timestamp=datetime.fromisoformat(data_row[4])
        )
        repo.add_review(comment)
