"""
Fine model — one-to-one with Transaction.
Created automatically when a book is returned late (see utils/fine_calculator.py).
"""

from datetime import datetime
from extensions import db


class Fine(db.Model):
    __tablename__ = 'fines'

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=False, unique=True)
    amount = db.Column(db.Float, nullable=False, default=0.0)
    paid = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        status = 'Paid' if self.paid else 'Unpaid'
        return f'<Fine ₹{self.amount} [{status}]>'
