# 📚 Smart Library Management System

A full-stack library management system with role-based access, automated fine
calculation, and an admin panel for catalog management — built to go beyond
basic CRUD.

## Status
✅ All core features complete and working: auth, catalog, borrow/return,
fines, admin panel, and analytics dashboard.

## Features
- [x] User authentication (Student & Admin roles) with hashed passwords
- [x] Book catalog with search & filter (by title, author, or category)
- [x] Borrow / Return workflow with real-time copy availability
- [x] Automatic fine calculation for overdue books (₹5/day)
- [x] Admin panel: add, edit, and delete books (role-protected)
- [x] Admin analytics dashboard: most borrowed books, overdue list, category breakdown

## Tech Stack
| Layer      | Technology                          |
|------------|--------------------------------------|
| Backend    | Python (Flask, Flask-Login)          |
| Database   | SQLite (via SQLAlchemy ORM)          |
| Frontend   | HTML, CSS, Jinja2                    |
| Auth       | Werkzeug password hashing            |

## Project Structure
```
library-management-system/
├── app.py                     # App entry point, blueprint registration
├── extensions.py              # Shared db + login manager instances
├── seed_books.py              # Populates the catalog with sample books
├── make_admin.py              # Promotes a signed-up user to admin
├── models/
│   ├── user.py                # User model (auth, roles)
│   ├── book.py                # Book model
│   ├── transaction.py         # Borrow/return records
│   └── fine.py                # Fine records
├── routes/
│   ├── auth.py                # Signup, login, logout
│   ├── books.py                # Catalog listing + search
│   ├── transactions.py        # Borrow / return endpoints
│   └── admin.py                # Admin book management (CRUD) + analytics dashboard
├── utils/
│   ├── fine_calculator.py     # Overdue fine business logic
│   └── decorators.py          # admin_required access control
├── templates/                  # Jinja2 templates (base, auth, books, admin)
├── static/
│   ├── css/style.css
│   └── img/
├── requirements.txt
└── README.md
```

## Setup & Installation
```bash
git clone https://github.com/SaniyaNalaband/library-management-system.git
cd library-management-system
python -m venv venv
venv\Scripts\activate         # Windows
# source venv/bin/activate    # Mac/Linux

pip install -r requirements.txt
python app.py
```
Then visit `http://127.0.0.1:5000` in your browser.

## Getting Started (demo walkthrough)
1. **Sign up** for a student account through the UI.
2. **Seed the catalog** with sample books:
   ```bash
   python seed_books.py
   ```
3. **Promote yourself to admin** (optional, for catalog management):
   ```bash
   python make_admin.py your-email@example.com
   ```
   Log out and back in to see the **Admin** link appear in the nav.
4. Browse the catalog, borrow a book, and return it to see the fine logic
   in action (mark a transaction overdue in the database to test it, or
   wait past the 14-day due date).

## Database Schema (ER Overview)
- **Users** — id, name, email, password_hash, role, created_at
- **Books** — id, title, author, category, isbn, total_copies, available_copies
- **Transactions** — id, user_id (FK), book_id (FK), borrow_date, due_date, return_date
- **Fines** — id, transaction_id (FK), amount, paid, created_at

**Relationships:** One user → many transactions. One book → many transactions.
One transaction → one fine (created automatically on late return).

## Key Design Decisions
- **Fine calculation is isolated** in `utils/fine_calculator.py` rather than
  baked into the model, so the business rule (₹5/day) can be explained,
  tested, and changed independently.
- **Role-based access control** via a custom `admin_required` decorator,
  rather than checking `current_user.role` inline in every route.
- **Passwords are never stored in plain text** — hashed with Werkzeug's
  `generate_password_hash` / `check_password_hash`.

## Contributing
This started as a personal portfolio project, but feel free to fork it,
open issues, or submit a pull request if you'd like to improve something —
whether that's a bug fix, a new feature, or better documentation.

## Author
Saniya — BCA Graduate

## License
MIT