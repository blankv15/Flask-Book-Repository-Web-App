import csv
from pathlib import Path

from werkzeug.security import generate_password_hash

from library import MemoryRepository
from library.adapters.jsondatareader import BooksJSONReader
from library.adapters.memory_repository import load_books
from library.adapters.repository import AbstractRepository
from library.domain.model import User, Book


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


def load_books(data_path: Path, repo: AbstractRepository):
    allBooks = BooksJSONReader(data_path / "comic_books_excerpt.json", data_path / "book_authors_excerpt.json")
    allBooks.read_json_files()

    for i in allBooks.dataset_of_books:
        repo.add_book(i)


def load_authors(data_path: Path, repo: AbstractRepository):
    allBooks = BooksJSONReader(data_path / "comic_books_excerpt.json", data_path / "book_authors_excerpt.json")
    allBooks.read_json_files()
    for i in allBooks.dataset_of_books:
        for b in i.authors:

            repo.add_book(b)

def load_users(data_path: Path, repo: AbstractRepository):
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


def populate(data_path: Path, repo: AbstractRepository):
    load_books(data_path, repo)

    load_users(data_path, repo)
    load_authors(data_path, repo)


'''def load_reviews(data_path: Path, repo: MemoryRepository, users):
    comments_filename = str(Path(data_path) / "comments.csv")
    for data_row in read_csv_file(comments_filename):
        comment = make_comment(
            comment_text=data_row[3],
            user=users[data_row[1]],
            article=repo.get_article(int(data_row[2])),
            timestamp=datetime.fromisoformat(data_row[4])
        )
        repo.add_comment(comment)'''
