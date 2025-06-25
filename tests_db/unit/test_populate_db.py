from sqlalchemy import select, inspect

from library.adapters.orm import metadata

def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['authors', 'book_authors', 'books', 'reviews', 'users']


def test_database_populate_select_all_users(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[4]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['user_name'])

        assert all_users == ['thorke', 'fmercury','mjackson']

def test_database_populate_select_all_comments(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_comments_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        # query for records in table comments
        select_statement = select([metadata.tables[name_of_comments_table]])
        result = connection.execute(select_statement)

        all_comments = []
        for row in result:
            all_comments.append((row['id'], row['user_id'], row['book_id'], row['review_text'], row['timestamp']))

        assert all_comments == []

# def test_database_populate_select_all_articles(database_engine):
#
#     # Get table information
#     inspector = inspect(database_engine)
#     name_of_articles_table = inspector.get_table_names()[1]
#
#     with database_engine.connect() as connection:
#         # query for records in table articles
#         select_statement = select([metadata.tables[name_of_articles_table]])
#         result = connection.execute(select_statement)
#
#         all_articles = []
#         for row in result:
#             all_articles.append((row['id'], row['title']))
#
#         nr_articles = len(all_articles)
#         assert nr_articles == 6
#
#         assert all_articles[0] == (1, 'Coronavirus: First case of virus in New Zealand')
#

