from flask import Blueprint, render_template, redirect, url_for, session, request

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
import library.search.services as services
import library.adapters.repository as repo

# Configure Blueprint.
search_blueprint = Blueprint('search_bp', __name__)


@search_blueprint.route("/search", methods=['GET', 'POST'])
def search():
    form = SearchForm()
    inputData = []
    results = "No search results found"
    search_items = []
    if request.method == 'POST':
        inputData = form.title_search.data

        if len(inputData) != 0:

            results = str(len(inputData)) + " Books found"

            search_items = services.get_book_by_search(repo.repo_instance, inputData)

    return render_template(

        'search/search.html',
        title='search',
        returnlength= len(search_items),
        searchInput=inputData,
        results=results,
        search_item=search_items,
        form=form,
    )


class SearchForm(FlaskForm):
    title_search = StringField('Title of book', [DataRequired(message="Enter in name of title")])
    submit = SubmitField('Search')
