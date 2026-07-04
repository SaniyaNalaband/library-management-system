"""
Smart Library Management System
--------------------------------
Entry point for the Flask application.
"""

from flask import Flask, render_template
from extensions import db

# Import models so SQLAlchemy knows about them before create_all() runs
from models.user import User
from models.book import Book
from models.transaction import Transaction
from models.fine import Fine


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'change-this-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()  # Creates tables if they don't already exist

    @app.route('/')
    def home():
        return render_template('index.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
