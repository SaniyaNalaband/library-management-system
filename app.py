"""
Smart Library Management System
--------------------------------
Entry point for the Flask application.
"""

from flask import Flask, render_template
from extensions import db, login_manager

# Import models so SQLAlchemy knows about them before create_all() runs
from models.user import User
from models.files.book import Book
from models.transaction import Transaction
from models.files.fine import Fine

from routes.auth import auth_bp
from routes.books import books_bp
from routes.transactions import transactions_bp


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'change-this-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(transactions_bp)

    with app.app_context():
        db.create_all()  # Creates tables if they don't already exist

    @app.route('/')
    def home():
        return render_template('index.html')

    return app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
