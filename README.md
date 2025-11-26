# LibraDB - Library Management System

A full-stack Library Management System built with Flask, SQLAlchemy, Jinja templates, and Bootstrap. The app provides librarian and member portals with authentication, approvals, bookings, and ratings.

## Windows + SQLite quick start

The following steps assume Windows 10/11 with Python 3.11+ installed and Git Bash/PowerShell available.

1. **Clone and set up a virtual environment**
   ```powershell
   git clone https://github.com/your-org/LibraDB.git
   cd LibraDB
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Use SQLite (default)**
   - No extra configuration is required. If `DATABASE_URL` is not set, the app stores data in `library.db` in the project root.
   - To explicitly set it, run:
     ```powershell
     $env:DATABASE_URL = "sqlite:///library.db"
     ```

3. **Initialize the database**
   ```powershell
   flask --app app db init
   flask --app app db migrate -m "Bootstrap tables"
   flask --app app db upgrade
   flask --app app seed   # optional demo data (creates a librarian and sample members)
   ```

   > Tip: The app also calls `db.create_all()` on startup. If you skip the migration
   > commands on SQLite, simply running `flask --app app run --debug` will create the
   > tables automatically and insert a default librarian account if none exists.

4. **Run the development server**
   ```powershell
   flask --app app run --debug
   ```

5. **Sign in** at http://localhost:5000
   - Librarian demo: `librarian@example.com / admin123`
   - Member demo: `alice@example.com / password123`
   - New member registrations are created from the login page and require librarian approval before sign-in.

## Core features

- Single login/registration screen with role-aware routing to librarian or member portals.
- Librarian approvals for new member registrations and member booking requests.
- Manage books with categories, descriptions, and copy tracking.
- Create and manage bookings, including approvals and returns.
- Collect 1-5 star ratings with comments for each book.
- Dashboards for both roles with quick actions and summaries.

## Project structure

```
├── app.py                # Flask entry point
├── library_app
│   ├── __init__.py       # App factory and extensions
│   ├── config.py         # Settings (secret key, DB URI)
│   ├── models.py         # SQLAlchemy models
│   ├── routes.py         # Views / controllers
│   ├── seed.py           # Demo data helper
│   ├── templates         # Jinja templates for UI
│   └── static            # CSS assets
├── requirements.txt
└── README.md
```

