from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, url_for

from . import db
from .models import Book, Booking, Category, Rating, User

bp = Blueprint("library", __name__)


def get_form_value(field_name: str, cast=str, default=None):
    value = request.form.get(field_name)
    if value is None or value == "":
        return default
    return cast(value)


@bp.route("/")
def index():
    book_count = Book.query.count()
    user_count = User.query.count()
    booking_count = Booking.query.count()
    rating_count = Rating.query.count()

    recent_books = Book.query.order_by(Book.created_at.desc()).limit(5)
    top_rated = Book.query.all()
    top_rated.sort(key=lambda b: b.average_rating(), reverse=True)

    return render_template(
        "index.html",
        book_count=book_count,
        user_count=user_count,
        booking_count=booking_count,
        rating_count=rating_count,
        recent_books=recent_books,
        top_rated=top_rated[:5],
    )


@bp.route("/books")
def books():
    category_id = request.args.get("category", type=int)
    categories = Category.query.all()

    if category_id:
        book_list = Book.query.filter_by(category_id=category_id).all()
    else:
        book_list = Book.query.all()

    return render_template(
        "books/list.html",
        books=book_list,
        categories=categories,
        selected_category=category_id,
    )


@bp.route("/books/create", methods=["GET", "POST"])
def create_book():
    categories = Category.query.all()

    if request.method == "POST":
        book = Book(
            title=get_form_value("title"),
            author=get_form_value("author"),
            isbn=get_form_value("isbn"),
            description=get_form_value("description"),
            category_id=get_form_value("category_id", int),
            copies_total=get_form_value("copies_total", int, 1),
            copies_available=get_form_value("copies_available", int, 1),
        )
        db.session.add(book)
        db.session.commit()
        flash("Book created successfully", "success")
        return redirect(url_for("library.books"))

    return render_template("books/form.html", categories=categories)


@bp.route("/books/<int:book_id>/edit", methods=["GET", "POST"])
def edit_book(book_id: int):
    book = Book.query.get_or_404(book_id)
    categories = Category.query.all()

    if request.method == "POST":
        book.title = get_form_value("title")
        book.author = get_form_value("author")
        book.isbn = get_form_value("isbn")
        book.description = get_form_value("description")
        book.category_id = get_form_value("category_id", int)
        book.copies_total = get_form_value("copies_total", int)
        book.copies_available = get_form_value("copies_available", int)
        db.session.commit()
        flash("Book updated successfully", "success")
        return redirect(url_for("library.books"))

    return render_template("books/form.html", book=book, categories=categories)


@bp.route("/books/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id: int):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash("Book deleted", "info")
    return redirect(url_for("library.books"))


@bp.route("/users")
def users():
    return render_template("users/list.html", users=User.query.all())


@bp.route("/users/create", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        user = User(name=get_form_value("name"), email=get_form_value("email"))
        db.session.add(user)
        db.session.commit()
        flash("User created", "success")
        return redirect(url_for("library.users"))

    return render_template("users/form.html")


@bp.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id: int):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted", "info")
    return redirect(url_for("library.users"))


@bp.route("/bookings")
def bookings():
    bookings_list = Booking.query.order_by(Booking.start_date.desc()).all()
    return render_template("bookings/list.html", bookings=bookings_list)


@bp.route("/bookings/create", methods=["GET", "POST"])
def create_booking():
    users = User.query.all()
    books = Book.query.all()

    if request.method == "POST":
        book_id = get_form_value("book_id", int)
        book = Book.query.get_or_404(book_id)
        if book.copies_available < 1:
            flash("No copies available", "warning")
            return redirect(url_for("library.create_booking"))

        booking = Booking(
            user_id=get_form_value("user_id", int),
            book_id=book_id,
            start_date=get_form_value("start_date", lambda v: date.fromisoformat(v)),
            end_date=get_form_value("end_date", lambda v: date.fromisoformat(v)),
        )
        book.copies_available -= 1
        db.session.add(booking)
        db.session.commit()
        flash("Booking created", "success")
        return redirect(url_for("library.bookings"))

    return render_template("bookings/form.html", users=users, books=books)


@bp.route("/bookings/<int:booking_id>/return", methods=["POST"])
def return_booking(booking_id: int):
    booking = Booking.query.get_or_404(booking_id)
    if not booking.returned:
        booking.returned = True
        booking.book.copies_available += 1
        db.session.commit()
        flash("Book returned", "success")
    return redirect(url_for("library.bookings"))


@bp.route("/ratings")
def ratings():
    rating_list = Rating.query.order_by(Rating.created_at.desc()).all()
    return render_template("ratings/list.html", ratings=rating_list)


@bp.route("/ratings/create", methods=["GET", "POST"])
def create_rating():
    users = User.query.all()
    books = Book.query.all()
    if request.method == "POST":
        rating = Rating(
            user_id=get_form_value("user_id", int),
            book_id=get_form_value("book_id", int),
            score=get_form_value("score", int),
            comment=get_form_value("comment"),
        )
        db.session.add(rating)
        db.session.commit()
        flash("Rating submitted", "success")
        return redirect(url_for("library.ratings"))

    return render_template("ratings/form.html", users=users, books=books)
