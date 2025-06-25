from flask import Blueprint, request, render_template, redirect, url_for, session

import library.adapters.repository as repo
import library.utilities.services as services


# Configure Blueprint.
utilities_blueprint = Blueprint('utilities_bp', __name__)


def get_selected_books(quantity=3):
    books = services.get_random_books(quantity, repo.repo_instance)

    for book in books:
        book['hyperlink'] = url_for('news_bp.books_by_date', date=book['date'].isoformat())
    return books
