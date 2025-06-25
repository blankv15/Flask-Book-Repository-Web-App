from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey, Boolean
)
from sqlalchemy.orm import mapper, relationship, synonym

# global variable giving access to the MetaData (schema) information of the database
from library.domain import model
from library.domain.model import Publisher

metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=False, nullable=False),
    Column('password', String(255), nullable=False)
)
# publisher_table = Table(
#     'publisher', metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('name', String(255), nullable=False)
# )

authors_table = Table(
    'authors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('unique_id', Integer, nullable=False),
    Column('full_name', String(255), nullable=False)
)

reviews_table = Table(
    # review book, review text, rating time
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('book_id', ForeignKey('books.id')),
    Column('rating', Integer, nullable=False),

    Column('review_text', String(1024), nullable=False),
    Column('timestamp', DateTime, nullable=False)
)
books_table = Table(
    # book book id, book title, coverUrl des pub author year ebook, pages
    'books', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book_id', Integer, nullable=False),
    # Column('publisher', ForeignKey('publisher.id')),

    Column('title', String(255), nullable=False),
    Column('cover_url', String(255), nullable=False),

    Column('description', String(255), nullable=False),
    Column('release_year', Integer, nullable=False),
    Column('authors', ForeignKey('authors.unique_id')),

    Column('num_pages', Integer, nullable=True),
    Column('ebook', Boolean, unique=False, default=False)

)
books_author_table = Table(
    'book_authors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book_id', ForeignKey('books.id')),
    Column('author_id', ForeignKey('authors.id'))
)
# books_published_table = Table(
#     'book_publisher', metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('book_id', ForeignKey('books.id')),
#     Column('publisher_id', ForeignKey('publisher.id'))
# )


def map_model_to_tables():
    mapper(model.User, users_table, properties={
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        '_User__Reviews': relationship(model.Review, backref='_Review__user')

    })
    mapper(model.Review, reviews_table, properties={
        '_Review__review_text': reviews_table.c.review_text,
        '_Review__timestamp': reviews_table.c.timestamp
    })
    # mapper(model.Publisher, publisher_table, properties={
    #     '_Publisher__name': publisher_table.c.name,
    #     '_Publisher__book_published': relationship(
    #         model.Book,
    #         secondary=books_published_table,
    #         back_populates="_Book__publisher"
    #     )
    # })

    mapper(model.Book, books_table, properties={

        '_Book__title': books_table.c.title,
        '_Book__book_id': books_table.c.book_id,

        '_Book__cover_url': books_table.c.cover_url,
        '_Book__description': books_table.c.description,
        '_Book__release_year': books_table.c.release_year,
        '_Book__authors': relationship(model.Author, secondary=books_author_table,
                                       back_populates='_Author__book_authored'),
        # '_Book__publisher': relationship(model.Publisher, secondary=books_published_table,
        #                                  back_populates='_Publisher__book_published'),
        '_Book__num_pages': books_table.c.num_pages,

        '_Book__ebook': books_table.c.ebook
    })
    mapper(model.Author, authors_table, properties={
        '_Author__unique_id': authors_table.c.unique_id,
        '_Author__full_name': authors_table.c.full_name,

        '_Author__book_authored': relationship(
            model.Book,
            secondary=books_author_table,
            back_populates="_Book__authors"
        )

    })
