"""
Borrow / Return routes — the core workflow of the library system.
Borrowing decrements available_copies; returning increments it and
triggers fine calculation if overdue.
"""

from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime

from extensions import db
from models.book import Book
from models.transaction import Transaction
from utils.fine_calculator import apply_fine_if_overdue

transactions_bp = Blueprint('transactions', __name__)


@transactions_bp.route('/borrow/<int:book_id>', methods=['POST'])
@login_required
def borrow(book_id):
    book = Book.query.get_or_404(book_id)

    if book.available_copies <= 0:
        flash(f'"{book.title}" is currently unavailable.', 'error')
        return redirect(url_for('books.list_books'))

    # Prevent borrowing the same book twice without returning it
    existing = Transaction.query.filter_by(
        user_id=current_user.id, book_id=book.id, return_date=None
    ).first()
    if existing:
        flash(f'You already have "{book.title}" borrowed.', 'error')
        return redirect(url_for('books.list_books'))

    txn = Transaction(user_id=current_user.id, book_id=book.id)
    book.available_copies -= 1

    db.session.add(txn)
    db.session.commit()

    flash(f'You borrowed "{book.title}". Due back in 14 days.', 'success')
    return redirect(url_for('books.list_books'))


@transactions_bp.route('/return/<int:transaction_id>', methods=['POST'])
@login_required
def return_book(transaction_id):
    txn = Transaction.query.get_or_404(transaction_id)

    if txn.user_id != current_user.id:
        flash('You cannot return a book that is not yours.', 'error')
        return redirect(url_for('books.list_books'))

    if txn.is_returned:
        flash('This book has already been returned.', 'error')
        return redirect(url_for('books.list_books'))

    txn.return_date = datetime.utcnow()
    txn.book.available_copies += 1
    db.session.commit()

    fine = apply_fine_if_overdue(txn)
    if fine:
        flash(f'Returned late. A fine of ₹{fine.amount} has been added.', 'error')
    else:
        flash('Book returned on time. Thank you!', 'success')

    return redirect(url_for('books.list_books'))
