"""
Seed script — populates the catalog with a diverse set of well-known books.
Run this once after setting up the database:

    python seed_books.py

Safe to re-run: it skips any book whose title already exists.
"""

from app import create_app
from extensions import db
from models.book import Book

BOOKS = [
    # (title, author, category, total_copies)
    ("Pride and Prejudice", "Jane Austen", "Classic Fiction", 3),
    ("1984", "George Orwell", "Dystopian Fiction", 4),
    ("To Kill a Mockingbird", "Harper Lee", "Classic Fiction", 3),
    ("The Great Gatsby", "F. Scott Fitzgerald", "Classic Fiction", 3),
    ("Crime and Punishment", "Fyodor Dostoevsky", "Classic Fiction", 2),
    ("The Hobbit", "J.R.R. Tolkien", "Fantasy", 4),
    ("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "Fantasy", 5),
    ("A Game of Thrones", "George R.R. Martin", "Fantasy", 3),
    ("Dune", "Frank Herbert", "Science Fiction", 3),
    ("The Martian", "Andy Weir", "Science Fiction", 2),
    ("Sapiens", "Yuval Noah Harari", "Non-Fiction", 3),
    ("Atomic Habits", "James Clear", "Self-Help", 4),
    ("Thinking, Fast and Slow", "Daniel Kahneman", "Psychology", 2),
    ("Clean Code", "Robert C. Martin", "Programming", 3),
    ("Introduction to Algorithms", "Thomas H. Cormen", "Computer Science", 2),
    ("Design Patterns", "Erich Gamma", "Computer Science", 2),
    ("A Brief History of Time", "Stephen Hawking", "Science", 3),
    ("The Silent Patient", "Alex Michaelides", "Mystery/Thriller", 3),
    ("Gone Girl", "Gillian Flynn", "Mystery/Thriller", 2),
    ("The Alchemist", "Paulo Coelho", "Fiction", 4),
    ("Wuthering Heights", "Emily Bronte", "Classic Fiction", 2),
    ("Meditations", "Marcus Aurelius", "Philosophy", 2),
    ("Educated", "Tara Westover", "Memoir", 3),
    ("The Diary of a Young Girl", "Anne Frank", "Memoir", 2),
    ("World History: Patterns of Interaction", "Roger B. Beck", "History", 2),
]


def seed():
    app = create_app()
    with app.app_context():
        added = 0
        skipped = 0

        for title, author, category, total_copies in BOOKS:
            if Book.query.filter_by(title=title).first():
                skipped += 1
                continue

            book = Book(
                title=title,
                author=author,
                category=category,
                total_copies=total_copies,
                available_copies=total_copies,
            )
            db.session.add(book)
            added += 1

        db.session.commit()
        print(f"Seed complete: {added} books added, {skipped} already existed and were skipped.")


if __name__ == "__main__":
    seed()