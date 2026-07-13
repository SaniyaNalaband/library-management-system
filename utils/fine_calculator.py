"""
Fine calculation logic.
Rule: ₹5 per day overdue, calculated from due_date to return_date (or today, if still unreturned).
This is intentionally kept separate from the model so the "business rule" can be
explained and changed independently — a common interview talking point.
"""

from datetime import datetime
from extensions import db
from models.fine import Fine

FINE_PER_DAY = 5.0


def calculate_fine(transaction):
    """
    Given a Transaction object, calculate overdue fine (in rupees).
    Returns 0 if not overdue.
    """
    reference_date = transaction.return_date or datetime.utcnow()

    if reference_date <= transaction.due_date:
        return 0.0

    days_overdue = (reference_date - transaction.due_date).days
    return round(days_overdue * FINE_PER_DAY, 2)


def apply_fine_if_overdue(transaction):
    """
    Called when a book is returned. If overdue, creates a Fine record
    linked to the transaction. Returns the Fine object or None.
    """
    fine_amount = calculate_fine(transaction)

    if fine_amount > 0:
        fine = Fine(transaction_id=transaction.id, amount=fine_amount)
        db.session.add(fine)
        db.session.commit()
        return fine

    return None
