"""
Database instance shared across the app.
Kept in its own file to avoid circular imports between app.py and models.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # redirects here if @login_required fails
login_manager.login_message = 'Please log in to access this page.'
