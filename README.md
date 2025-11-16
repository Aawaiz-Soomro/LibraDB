# Library Management System

A simple full-stack Library Management System built with Flask, Jinja templates, Bootstrap, and MySQL/SQLite. It demonstrates CRUD operations, booking, ratings, listings, and other common library workflows with a clean UI.

## Features

- Manage books with categories, descriptions, and copy tracking.
- Register patrons and view their bookings and ratings.
- Create and manage bookings, including marking books as returned.
- Collect 1-5 star ratings with comments for each book.
- Dashboard with quick statistics, recent additions, and top-rated books.
- Database seeding command to populate demo data.

## Tech stack

- Python 3.11+
- Flask 3 + SQLAlchemy ORM + Flask-Migrate
- MySQL (recommended) or SQLite for local demos
- Bootstrap 5 for styling

## Getting started

1. **Install dependencies**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure the database**
   - Set the `DATABASE_URL` environment variable, e.g.
     ```bash
     export DATABASE_URL="mysql://user:password@localhost:3306/library"
     ```
   - Without this variable, the app falls back to a local SQLite file (`library.db`).

3. **Initialize the database**
   ```bash
   flask --app app db init
   flask --app app db migrate -m "Initial tables"
   flask --app app db upgrade
   flask --app app seed  # optional demo data
   ```

4. **Run the development server**
   ```bash
   flask --app app run --debug
   ```

5. **Access the UI** at http://localhost:5000 to manage books, users, bookings, and ratings.

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

## Next steps

- Add authentication/authorization (Flask-Login) if you need per-user access.
- Extend the ER diagram with more entities (fines, publishers, etc.).
- Containerize with Docker for easier deployment.

Feel free to adapt the codebase to match your ER diagram or presentation requirements.
