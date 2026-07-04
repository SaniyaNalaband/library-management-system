# 📚 Smart Library Management System

A full-stack library management system with role-based access, automated fine
calculation, and an admin analytics dashboard — built to go beyond basic CRUD.

## Status
🚧 In development — scaffold complete, features being built incrementally.

## Features (planned)
- [ ] User authentication (Student & Admin roles) with hashed passwords
- [ ] Book catalog with search & filter
- [ ] Borrow / Return workflow
- [ ] Automatic fine calculation for overdue books
- [ ] Admin dashboard: most borrowed books, overdue list, category trends
- [ ] Database triggers for real-time availability updates

## Tech Stack
| Layer      | Technology            |
|------------|------------------------|
| Backend    | Python (Flask)         |
| Database   | SQLite / MySQL         |
| Frontend   | HTML, CSS, Jinja2      |
| Charts     | Chart.js               |

## Project Structure
```
library-management-system/
├── app.py                 # App entry point
├── models/                # Database models
├── routes/                # Route handlers (blueprints)
├── utils/                 # Helper functions (e.g., fine calculation)
├── templates/              # HTML templates
├── static/
│   ├── css/
│   ├── js/
│   └── img/
├── requirements.txt
└── README.md
```

## Setup & Installation
```bash
git clone <your-repo-url>
cd library-management-system
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Then visit `http://127.0.0.1:5000` in your browser.

## Database Schema (ER Overview)
- **Users** — id, name, email, password_hash, role
- **Books** — id, title, author, category, total_copies, available_copies
- **Transactions** — id, user_id (FK), book_id (FK), borrow_date, due_date, return_date
- **Fines** — id, transaction_id (FK), amount, paid_status

## Author
Saniya — BCA Graduate
