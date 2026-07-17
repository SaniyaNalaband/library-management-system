"""
Transaction model — represents one borrow event.
This is the bridge table between Users and Books (many-to-many via transactions).
"""

from datetime import datetime, timedelta
from extensions import db

DEFAULT_LOAN_DAYS = 14


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)

    borrow_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)  # null = still borrowed

    fine = db.relationship('Fine', backref='transaction', uselist=False, lazy=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.due_date:
            self.due_date = datetime.utcnow() + timedelta(days=DEFAULT_LOAN_DAYS)

    @property
    def is_returned(self):
        return self.return_date is not None

    @property
    def is_overdue(self):
        if self.is_returned:
            return self.return_date > self.due_date
        return datetime.utcnow() > self.due_date

    @property
    def days_overdue(self):
        reference = self.return_date or datetime.utcnow()
        if reference <= self.due_date:
            return 0
        return (reference - self.due_date).days

    def __repr__(self):
        status = 'Returned' if self.is_returned else 'Borrowed'
        return f'<Transaction user={self.user_id} book={self.book_id} [{status}]>'
