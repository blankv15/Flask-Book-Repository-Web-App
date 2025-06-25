from flask import Blueprint, render_template

import library.adapters.repository as repo
import library.utilities.utilities as utilities

import library.home.services as services

home_blueprint = Blueprint('home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    top_books = services.get_first_10_books(repo.repo_instance)


    return render_template('home/home.html')
