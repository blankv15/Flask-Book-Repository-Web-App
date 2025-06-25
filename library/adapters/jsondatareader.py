import json
from typing import List

from library.domain.model import Publisher, Author, Book


class BooksJSONReader:

    def __init__(self, books_file_name: str, authors_file_name: str):
        self.__books_file_name = books_file_name
        self.__authors_file_name = authors_file_name
        self.__dataset_of_books = []

    @property
    def dataset_of_books(self) -> List[Book]:
        return self.__dataset_of_books

    def read_books_file(self) -> list:
        books_json = []
        with open(self.__books_file_name, encoding='UTF-8') as books_jsonfile:
            for line in books_jsonfile:
                book_entry = json.loads(line)
                books_json.append(book_entry)
        return books_json

    def read_authors_file(self) -> dict:
        # authors_json = []
        # with open(self.__authors_file_name, encoding='UTF-8') as authors_jsonfile:
        #     for line in authors_jsonfile:
        #         author_entry = json.loads(line)
        #         authors_json.append(author_entry)
        # return authors_json

        all_authors = {}
        with open(self.__authors_file_name) as authors:
            for author in authors:
                current = json.loads(author)
                all_authors[current["author_id"]] = [current["name"], current["average_rating"],
                                                     current["text_reviews_count"], current["ratings_count"]]
        return all_authors

    def read_json_files(self):
        authors_json = self.read_authors_file()
        books_json = self.read_books_file()
        publishers = {}

        for book_json in books_json:
            book_instance = Book(int(book_json['book_id']), book_json['title'])

            if book_json["publisher"] not in publishers:
                publishers[book_json["publisher"]] = Publisher(book_json["publisher"])
                book_instance.publisher = publishers[book_json["publisher"]]
            else:
                book_instance.publisher = publishers[book_json["publisher"]]
            # if Publisher(book_json['publisher']) not in publishers:
            #     publishers.append(book_json['publisher'])
            #     book_instance.
            if book_json['publication_year'] != "":
                book_instance.release_year = int(book_json['publication_year'])
            if book_json['is_ebook'].lower() == 'false':
                book_instance.ebook = False
            else:
                if book_json['is_ebook'].lower() == 'true':
                    book_instance.ebook = True
            book_instance.description = book_json['description']
            if book_json['num_pages'] != "":
                book_instance.num_pages = int(book_json['num_pages'])
            if book_instance.cover_url != "":
                book_instance.cover_url = book_json["image_url"]

            for i in book_json["authors"]:
                name = authors_json[i["author_id"]][0]
                book_instance.add_author(Author(int(i["author_id"]), name))

            self.__dataset_of_books.append(book_instance)
