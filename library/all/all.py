from flask import Blueprint, render_template, redirect, url_for, session, request

import library.all.services as services
import library.utilities.utilities as utilities

import library.adapters.repository as repo

# Configure Blueprint.
all_blueprint = Blueprint('all_bp', __name__)


@all_blueprint.route("/browse_all_books", methods=['GET'])
def browse_all_books():
    # Read query parameters.
    target_id = request.args.get('id')
    book_to_show_reviews = request.args.get('view_reviews_for')

    # Fetch the first and last books in the series.
    first_book = services.get_first_book(repo.repo_instance)  # is a dict
    last_book = services.get_last_book(repo.repo_instance)  # is a dict

    if book_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent book id.
        book_to_show_reviews = -1
    else:
        # Convert book_to_show_reviews from string to int.
        book_to_show_reviews = int(book_to_show_reviews)


    # Fetch book(s) for the target date. This call also returns the previous and next dates for books immediately
    # before and after the target date.
    books = services.get_all_books(repo.repo_instance)
    reviews = services.get_reviews(repo.repo_instance)

        # Construct urls for viewing book reviews and adding reviews.
    '''for book in books:
        book['view_review_url'] = url_for('all_bp.browse_all_books', id=target_id, view_reviews_for=book['id'])            book['add_review_url'] = url_for('news_bp.review_on_book', book=book['id'])
    '''

        # Generate the webpage to display the books.
    return render_template(
        'all/all_books.html',
        title='Books',
        books=books,
        show_reviews_for_book=book_to_show_reviews,
        reviews=reviews,
        handler_url=url_for('all_bp.browse_all_books')
    )

    # No books to show, so return the homepage.
    return redirect(url_for('home.home'))