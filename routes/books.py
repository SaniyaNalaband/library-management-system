"""
Book catalog routes: list all books, search/filter by title, author, or category.
"""

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from models.files.book import Book
from models.files.transaction import Transaction

books_bp = Blueprint('books', __name__)


@books_bp.route('/books')
@login_required
def list_books():
    query = request.args.get('q', '').strip()

    if query:
        like_pattern = f'%{query}%'
        books = Book.query.filter(
            (Book.title.ilike(like_pattern)) |
            (Book.author.ilike(like_pattern)) |
            (Book.category.ilike(like_pattern))
        ).all()
    else:
        books = Book.query.all()

    # Map book_id -> transaction_id for books the current user currently has borrowed
    active_txns = Transaction.query.filter_by(
        user_id=current_user.id, return_date=None
    ).all()
    borrowed_map = {t.book_id: t.id for t in active_txns}

    return render_template('books.html', books=books, query=query, borrowed_map=borrowed_map)
