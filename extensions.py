"""
Database instance shared across the app.
Kept in its own file to avoid circular imports between app.py and models.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
