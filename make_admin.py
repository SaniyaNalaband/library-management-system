"""
Promotes an existing user to the 'admin' role by email.
Usage:

    python make_admin.py you@example.com

You must sign up normally first, then run this to grant admin access.
"""

import sys
from app import create_app
from extensions import db
from models.user import User


def make_admin(email):
    app = create_app()
    with app.app_context():
        user = User.query.filter_by(email=email.strip().lower()).first()

        if not user:
            print(f"No user found with email: {email}")
            return

        if user.role == 'admin':
            print(f"{user.email} is already an admin.")
            return

        user.role = 'admin'
        db.session.commit()
        print(f"{user.email} is now an admin.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python make_admin.py <email>")
        sys.exit(1)

    make_admin(sys.argv[1])
