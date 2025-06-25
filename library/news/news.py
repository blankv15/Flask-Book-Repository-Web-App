from flask import Blueprint, request, render_template, redirect, url_for, session

import library.adapters.repository as repo
import library.utilities.utilities as utilities
import library.news.services as services

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from library.Auth.auth import login_required


# Configure Blueprint.
news_blueprint = Blueprint('news_bp', __name__)


@news_blueprint.route('/browse_books', methods=['GET'])
def browse_books():
    # Read query parameters.
    target_date = request.args.get('release_year')
    book_to_show_reviews = request.args.get('view_reviews_for')

    # Fetch the first and last books in the series.
    first_book = services.get_first_book(repo.repo_instance) #is a dict
    last_book = services.get_last_book(repo.repo_instance) #is a dict

    if target_date is None:
        # No date query parameter, so return books from release_year 1 of the series.
        target_date = first_book['release_year']
    else:
        # Convert target_date from string to date.
        target_date = int(target_date)

    if book_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent book id.
        book_to_show_reviews = -1
    else:
        # Convert book_to_show_reviews from string to int.
        book_to_show_reviews = int(book_to_show_reviews)

    # Fetch book(s) for the target date. This call also returns the previous and next dates for books immediately
    # before and after the target date.
    books, previous_release_year, next_release_year = services.get_books_by_release_year(target_date, repo.repo_instance)
    reviews = services.get_reviews(repo.repo_instance)

    first_book_url = None
    last_book_url = None
    next_book_url = None
    prev_book_url = None

    if len(books) > 0:
        # There's at least one book for the target date.
        if previous_release_year is not None:
            # There are books on a previous date, so generate URLs for the 'previous' and 'first' navigation buttons.
            prev_book_url = url_for('news_bp.browse_books', date=int(previous_release_year))
            first_book_url = url_for('news_bp.browse_books', date=int(first_book['release_year']))

        # There are books on a subsequent date, so generate URLs for the 'next' and 'last' navigation buttons.
        if next_release_year is not None:
            next_book_url = url_for('news_bp.browse_books', date=int(next_release_year))
            last_book_url = url_for('news_bp.browse_books', date=int(last_book['release_year']))

        # Construct urls for viewing book reviews and adding reviews.
        for book in books:
            book['view_review_url'] = url_for('news_bp.browse_books', date=target_date, view_reviews_for=book['id'])
            book['add_review_url'] = url_for('news_bp.review_on_book', book=book['id'])

        # Generate the webpage to display the books.
        return render_template(
            'news/book.html',
            title='Books',
            release_year=target_date,
            books=books,
            first_book_url=first_book_url,
            last_book_url=last_book_url,
            prev_book_url=prev_book_url,
            next_book_url=next_book_url,
            show_reviews_for_book=book_to_show_reviews,
            reviews=reviews
        )

    # No books to show, so return the homepage.
    return redirect(url_for('home.home'))










'''
#####AUTHOR#####
news_blueprint.route('/books_by_author', methods=['GET'])
def books_by_author():
    # Read query parameters.
    target_auth = request.args.get('author')
    book_to_show_reviews = request.args.get('view_reviews_for')

    # Fetch the first and last books in the series.
    first_book = services.get_first_book(repo.repo_instance)  # is a dict
    last_book = services.get_last_book(repo.repo_instance)  # is a dict

    if target_auth is None:
        # No date query parameter, so return books from release_year 1 of the series.
        target_auth = first_book['author']
    else:
        # Convert target_date from string to date.
        target_auth = int(target_auth)

    if book_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent book id.
        book_to_show_reviews = -1
    else:
        # Convert book_to_show_reviews from string to int.
        book_to_show_reviews = int(book_to_show_reviews)

    # Fetch book(s) for the target date. This call also returns the previous and next dates for books immediately
    # before and after the target date.
    books, previous_release_year, next_release_year = services.get_books_by_release_year(target_auth,
                                                                                         repo.repo_instance)
    reviews = services.get_reviews(repo.repo_instance)

    first_book_url = None
    last_book_url = None
    next_book_url = None
    prev_book_url = None

    if len(books) > 0:
        # There's at least one book for the target date.
        if previous_release_year is not None:
            # There are books on a previous date, so generate URLs for the 'previous' and 'first' navigation buttons.
            prev_book_url = url_for('news_bp.books_by_author', date=int(previous_release_year))
            first_book_url = url_for('news_bp.books_by_author', date=int(first_book['author']))

        # There are books on a subsequent date, so generate URLs for the 'next' and 'last' navigation buttons.
        if next_release_year is not None:
            next_book_url = url_for('news_bp.books_by_author', date=int(next_release_year))
            last_book_url = url_for('news_bp.books_by_author', date=int(last_book['author']))

        # Construct urls for viewing book reviews and adding reviews.
        for book in books:
            book['view_review_url'] = url_for('news_bp.books_by_author', date=target_auth, view_reviews_for=book['id'])
            book['add_review_url'] = url_for('news_bp.review_on_book', book=book['id'])

        # Generate the webpage to display the books.
        return render_template(
            'news/author.html',
            title='Books',
            author=target_auth,
            books=books,
            selected_books=utilities.get_selected_books(len(books) * 2),
            first_book_url=first_book_url,
            last_book_url=last_book_url,
            prev_book_url=prev_book_url,
            next_book_url=next_book_url,
            show_reviews_for_book=book_to_show_reviews,
            reviews=reviews
        )

    # No books to show, so return the homepage.
    return redirect(url_for('home.home'))


'''
'''
    books_per_page = 3

    # Read query parameters.
    author_name = request.args.get('author')
    cursor = request.args.get('cursor')
    book_to_show_reviews = request.args.get('view_reviews_for')

    if book_to_show_reviews is None:
        # No view-comments query parameter, so set to a non-existent article id.
        book_to_show_reviews = -1
    else:
        # Convert article_to_show_comments from string to int.
        book_to_show_reviews = int(book_to_show_reviews)

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    # Retrieve article ids for articles that are tagged with tag_name.
    book_ids = services.get_book_ids_for_author(author_name, repo.repo_instance)

    # Retrieve the batch of articles to display on the Web page.
    books = services.get_books_by_id(book_ids[cursor:cursor + books_per_page], repo.repo_instance)

    first_article_url = None
    last_article_url = None
    next_article_url = None
    prev_article_url = None

    if cursor > 0:
        # There are preceding articles, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_article_url = url_for('news_bp.articles_by_tag', tag=tag_name, cursor=cursor - articles_per_page)
        first_article_url = url_for('news_bp.articles_by_tag', tag=tag_name)

    if cursor + articles_per_page < len(article_ids):
        # There are further articles, so generate URLs for the 'next' and 'last' navigation buttons.
        next_article_url = url_for('news_bp.articles_by_tag', tag=tag_name, cursor=cursor + articles_per_page)

        last_cursor = articles_per_page * int(len(article_ids) / articles_per_page)
        if len(article_ids) % articles_per_page == 0:
            last_cursor -= articles_per_page
        last_article_url = url_for('news_bp.articles_by_tag', tag=tag_name, cursor=last_cursor)

    # Construct urls for viewing article comments and adding comments.
    for article in articles:
        article['view_comment_url'] = url_for('news_bp.articles_by_tag', tag=tag_name, cursor=cursor, view_comments_for=article['id'])
        article['add_comment_url'] = url_for('news_bp.comment_on_article', article=article['id'])

    # Generate the webpage to display the articles.
    return render_template(
        'news/articles.html',
        title='Articles',
        articles_title='Articles tagged by ' + tag_name,
        articles=articles,
        selected_articles=utilities.get_selected_articles(len(articles) * 2),
        tag_urls=utilities.get_tags_and_urls(),
        first_article_url=first_article_url,
        last_article_url=last_article_url,
        prev_article_url=prev_article_url,
        next_article_url=next_article_url,
        show_comments_for_article=article_to_show_comments
    )
'''


######## REVIEWS ########
@news_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def review_on_book():
    # Obtain the user name of the currently logged in user.
    user_name = session['user_name']

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an book id, when subsequently called with a HTTP POST request, the book id remains in the
    # form.
    form = CommentForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the comment text has passed data validation.
        # Extract the book id, representing the commented book, from the form.
        book_id = int(form.book_id.data)

        # Use the service layer to store the new comment.
        services.add_review(form.review.data, user_name, book_id, int(form.rating.data), repo.repo_instance)

        # Retrieve the book in dict form.
        book = services.get_book(book_id, repo.repo_instance)

        # Cause the web browser to display the page of all books that have the same date as the commented book,
        # and display all comments, including the new comment.
        return redirect(url_for('news_bp.review_on_book', release_year=book['release_year'], view_reviews_for=book_id))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the book id, representing the book to comment, from a query parameter of the GET request.
        book_id = int(request.args.get('book'))

        # Store the book id in the form.
        form.book_id.data = book_id
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the book id of the book being commented from the form.
        book_id = int(form.book_id.data)

    # For a GET or an unsuccessful POST, retrieve the book to comment in dict form, and return a Web page that allows
    # the user to enter a comment. The generated Web page includes a form object.
    book = services.get_book(book_id, repo.repo_instance)
    review_dict = services.get_reviews(repo.repo_instance)

    return render_template(
        'news/review_on_book.html',
        title='Edit book',
        book=book,
        form=form,
        user=user_name,
        reviews=review_dict,
        handler_url=url_for('news_bp.review_on_book'),
        selected_books=utilities.get_selected_books(),
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class CommentForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])

    rating = TextAreaField('Rating', [
        DataRequired(),
        Length(min=1, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])

    book_id = HiddenField("Book id")
    submit = SubmitField('Submit')