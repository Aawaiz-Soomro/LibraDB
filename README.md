# LibraDB - Library Management System

Flask + SQLite library manager with a single login/registration screen, role-aware portals, librarian approvals, and sample seed data.

## Windows + SQLite quick start

These steps assume Windows 10/11, Python 3.11+, and PowerShell.

1) **Clone and create a virtual environment**
   ```powershell
   git clone https://github.com/your-org/LibraDB.git
   cd LibraDB
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```

2) **Use SQLite (default)**
   - No extra setup needed; data lives in `library.db` in the project root.
   - To set it explicitly:
     ```powershell
     $env:DATABASE_URL = "sqlite:///library.db"
     ```

3) **Create the database schema**
   ```powershell
   flask --app app db upgrade   # applies migrations if migrations/ exists
   # or rely on create_all(): flask --app app run --debug (first run creates tables)
   ```

4) **Seed demo data (optional but recommended)**
   ```powershell
   flask --app app seed
   ```
   This creates a default librarian plus sample members, books, a booking, and ratings. The seeder is idempotent—you can rerun it safely.

5) **Run the app**
   ```powershell
   flask --app app run --debug
   ```
   Visit http://localhost:5000 — the login screen is the first stop.

## Accounts and flow

- **Librarian demo:** `librarian@example.com / admin123`
- **Member demo:** `alice@example.com / password123`
- New users register as members only from the login page; a librarian must approve their account before they can sign in.
- Member booking requests also require librarian approval before they count against available copies.

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

