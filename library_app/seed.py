from datetime import date, timedelta

from . import db
from .models import Book, Booking, Category, Rating, User


def seed_database() -> None:
    if User.query.count() > 0:
        print("Database already seeded")
        return

    fiction = Category(name="Fiction")
    science = Category(name="Science")
    history = Category(name="History")

    db.session.add_all([fiction, science, history])
    db.session.flush()

    librarian = User(name="Libby Librarian", email="librarian@example.com", role="librarian", approved=True)
    librarian.set_password("admin123")

    alice = User(name="Alice Johnson", email="alice@example.com", role="member", approved=True)
    alice.set_password("password123")
    bob = User(name="Bob Smith", email="bob@example.com", role="member", approved=True)
    bob.set_password("password123")
    carol = User(name="Carol Perez", email="carol@example.com", role="member", approved=True)
    carol.set_password("password123")

    db.session.add_all([librarian, alice, bob, carol])

    books = [
        Book(
            title="Clean Code",
            author="Robert C. Martin",
            isbn="9780132350884",
            description="Handbook of agile software craftsmanship.",
            category=science,
            copies_total=4,
            copies_available=4,
        ),
        Book(
            title="1984",
            author="George Orwell",
            isbn="9780451524935",
            description="Dystopian social science fiction novel.",
            category=fiction,
            copies_total=3,
            copies_available=3,
        ),
        Book(
            title="Sapiens",
            author="Yuval Noah Harari",
            isbn="9780062316097",
            description="Brief history of humankind.",
            category=history,
            copies_total=2,
            copies_available=2,
        ),
    ]
    db.session.add_all(books)
    db.session.flush()

    booking = Booking(
        user=alice,
        book=books[0],
        start_date=date.today(),
        end_date=date.today() + timedelta(days=7),
        approved=True,
    )
    books[0].copies_available -= 1

    db.session.add(booking)

    ratings = [
        Rating(user=alice, book=books[0], score=5, comment="Great reference!"),
        Rating(user=bob, book=books[1], score=4, comment="A classic."),
        Rating(user=carol, book=books[2], score=5, comment="Eye opening."),
    ]
    db.session.add_all(ratings)
    db.session.commit()
    print("Seed data inserted")
