"""
Book model — tracks total vs available copies so we always know
whether a book can be borrowed right now.
"""

from extensions import db


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=True)
    total_copies = db.Column(db.Integer, nullable=False, default=1)
    available_copies = db.Column(db.Integer, nullable=False, default=1)

    transactions = db.relationship('Transaction', backref='book', lazy=True)

    @property
    def is_available(self):
        return self.available_copies > 0

    def __repr__(self):
        return f'<Book {self.title} ({self.available_copies}/{self.total_copies})>'
