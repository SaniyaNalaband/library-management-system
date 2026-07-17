"""
Admin routes: manage the book catalog (add / edit / delete) and view
the analytics dashboard.
All routes here require an authenticated user with role == 'admin'.
"""

from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from sqlalchemy import func

from extensions import db
from models.book import Book
from models.user import User
from models.transaction import Transaction
from models.fine import Fine
from utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_books = Book.query.count()
    total_users = User.query.filter_by(role='student').count()
    active_borrows = Transaction.query.filter_by(return_date=None).count()

    unpaid_fines_total = (
        db.session.query(func.coalesce(func.sum(Fine.amount), 0))
        .filter(Fine.paid.is_(False))
        .scalar()
    )

    # Most borrowed books: join Transaction -> Book, group by book, count, top 5
    most_borrowed = (
        db.session.query(Book.title, func.count(Transaction.id).label('borrow_count'))
        .join(Transaction, Transaction.book_id == Book.id)
        .group_by(Book.id)
        .order_by(func.count(Transaction.id).desc())
        .limit(5)
        .all()
    )

    # Currently overdue: active borrow whose due date has passed
    overdue = (
        db.session.query(Transaction, Book.title, User.name, User.email)
        .join(Book, Transaction.book_id == Book.id)
        .join(User, Transaction.user_id == User.id)
        .filter(Transaction.return_date.is_(None))
        .filter(Transaction.due_date < datetime.utcnow())
        .order_by(Transaction.due_date.asc())
        .all()
    )

    # Category distribution: group books by category, count
    category_counts = (
        db.session.query(Book.category, func.count(Book.id))
        .group_by(Book.category)
        .order_by(func.count(Book.id).desc())
        .all()
    )

    return render_template(
        'admin_dashboard.html',
        total_books=total_books,
        total_users=total_users,
        active_borrows=active_borrows,
        unpaid_fines_total=unpaid_fines_total,
        most_borrowed=most_borrowed,
        overdue=overdue,
        category_counts=category_counts,
        now=datetime.utcnow(),
    )


@admin_bp.route('/books')
@login_required
@admin_required
def manage_books():
    books = Book.query.order_by(Book.title).all()
    return render_template('admin_books.html', books=books)


@admin_bp.route('/books/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_book():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        category = request.form.get('category', '').strip()
        isbn = request.form.get('isbn', '').strip() or None
        total_copies = request.form.get('total_copies', '1').strip()

        if not title or not author or not category:
            flash('Title, author, and category are required.', 'error')
            return redirect(url_for('admin.add_book'))

        try:
            total_copies = max(1, int(total_copies))
        except ValueError:
            total_copies = 1

        book = Book(
            title=title,
            author=author,
            category=category,
            isbn=isbn,
            total_copies=total_copies,
            available_copies=total_copies,
        )
        db.session.add(book)
        db.session.commit()

        flash(f'"{title}" was added to the catalog.', 'success')
        return redirect(url_for('admin.manage_books'))

    return render_template('admin_book_form.html', book=None)


@admin_bp.route('/books/<int:book_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        category = request.form.get('category', '').strip()
        isbn = request.form.get('isbn', '').strip() or None
        total_copies = request.form.get('total_copies', '1').strip()

        if not title or not author or not category:
            flash('Title, author, and category are required.', 'error')
            return redirect(url_for('admin.edit_book', book_id=book.id))

        try:
            new_total = max(1, int(total_copies))
        except ValueError:
            new_total = book.total_copies

        # Keep available_copies consistent when total_copies changes
        borrowed_count = book.total_copies - book.available_copies
        book.title = title
        book.author = author
        book.category = category
        book.isbn = isbn
        book.total_copies = new_total
        book.available_copies = max(0, new_total - borrowed_count)

        db.session.commit()
        flash(f'"{title}" was updated.', 'success')
        return redirect(url_for('admin.manage_books'))

    return render_template('admin_book_form.html', book=book)


@admin_bp.route('/books/<int:book_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)

    active_borrows = [t for t in book.transactions if t.return_date is None]
    if active_borrows:
        flash(f'Cannot delete "{book.title}" — it currently has active borrows.', 'error')
        return redirect(url_for('admin.manage_books'))

    title = book.title
    db.session.delete(book)
    db.session.commit()
    flash(f'"{title}" was removed from the catalog.', 'success')
    return redirect(url_for('admin.manage_books'))
