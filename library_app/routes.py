from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from . import db
from .models import Book, Booking, Category, Rating, User

bp = Blueprint("library", __name__)


def current_role() -> str | None:
    return session.get("role")


def current_member() -> User | None:
    user_id = session.get("user_id")
    if not user_id:
        return None
    return User.query.get(user_id)


def require_role(role: str):
    if current_role() != role:
        flash("Please log in to access that portal.", "warning")
        return redirect(url_for("library.login", next=request.path))
    return None


@bp.app_context_processor
def inject_globals():
    return {"active_role": current_role(), "active_member": current_member()}


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


@bp.route("/login", methods=["GET", "POST"])
def login():
    users = User.query.order_by(User.name).all()

    if request.method == "POST":
        role = request.form.get("role")

        if role == "admin":
            session.clear()
            session["role"] = "admin"
            flash("Logged in as Librarian.", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("library.admin_portal"))

        if role == "member":
            name = get_form_value("name")
            email = get_form_value("email")
            if not name or not email:
                flash("Please provide your name and email to continue.", "warning")
                return redirect(url_for("library.login"))

            member = User.query.filter_by(email=email).first()
            if not member:
                member = User(name=name, email=email)
                db.session.add(member)
                db.session.commit()

            session.clear()
            session["role"] = "member"
            session["user_id"] = member.id
            flash("Signed in to the Member portal.", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("library.member_portal"))

        flash("Select a portal to continue.", "warning")

    return render_template("auth/login.html", users=users)


@bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("library.index"))


@bp.route("/admin")
def admin_portal():
    redirect_response = require_role("admin")
    if redirect_response:
        return redirect_response

    book_count = Book.query.count()
    user_count = User.query.count()
    booking_count = Booking.query.count()
    rating_count = Rating.query.count()

    recent_books = Book.query.order_by(Book.created_at.desc()).limit(5)
    active_bookings = Booking.query.filter_by(returned=False).order_by(Booking.start_date.desc()).limit(5)

    return render_template(
        "admin/dashboard.html",
        book_count=book_count,
        user_count=user_count,
        booking_count=booking_count,
        rating_count=rating_count,
        recent_books=recent_books,
        active_bookings=active_bookings,
    )


@bp.route("/member")
def member_portal():
    redirect_response = require_role("member")
    if redirect_response:
        return redirect_response

    member = current_member()
    open_bookings = Booking.query.filter_by(user_id=member.id, returned=False).order_by(Booking.start_date.desc()).limit(5)
    recent_ratings = Rating.query.filter_by(user_id=member.id).order_by(Rating.created_at.desc()).limit(3)
    suggested_books = Book.query.order_by(Book.created_at.desc()).limit(4)

    return render_template(
        "member/dashboard.html",
        member=member,
        open_bookings=open_bookings,
        recent_ratings=recent_ratings,
        suggested_books=suggested_books,
    )


@bp.route("/portfolio")
def portfolio():
    hero = {
        "name": "Avery Quinn",
        "roles": ["CS Student", "Creative Coder", "Full-Stack Dev"],
        "tagline": "Design-forward developer crafting ultra-fast experiences.",
        "bio": (
            "I'm a computer science student obsessed with building polished, human-centered interfaces "
            "and performant systems. Here's a snapshot of the playground where I experiment with "
            "motion, micro-interactions, and emerging tech."
        ),
        "cta_primary": {"label": "Download Résumé", "url": "#"},
        "cta_secondary": {"label": "Let's Talk", "url": "#contact"},
    }

    stats = [
        {"label": "Projects", "value": "24", "detail": "concept-to-launch"},
        {"label": "Hackathons", "value": "12", "detail": "global podium finishes"},
        {"label": "Coffee", "value": "∞", "detail": "fueling late-night builds"},
    ]

    projects = [
        {
            "title": "NeuroEdge Studio",
            "subtitle": "Realtime AI dashboard for the creative industry",
            "description": "Designed a cinematic data canvas with GPU-accelerated visuals, sub-100ms interactions, and adaptive layouts.",
            "tags": ["WebGL", "FastAPI", "WebSockets", "UX"],
            "image": "https://images.unsplash.com/photo-1483478550801-ceba5fe50e8e?auto=format&fit=crop&w=1200&q=80",
            "link": "#",
        },
        {
            "title": "Pulseboard",
            "subtitle": "Low-latency ops board for campus mobility",
            "description": "Built an offline-first PWA with predictive routing, gradient theming, and tactile micro-interactions.",
            "tags": ["TypeScript", "PWA", "GraphQL", "Design Systems"],
            "image": "https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=1200&q=80",
            "link": "#",
        },
        {
            "title": "Aurora Compiler",
            "subtitle": "DSL + compiler toolkit for shader artists",
            "description": "Created a playful syntax, VS Code extension, and visual debugger that transforms creative coding workflows.",
            "tags": ["Rust", "Compilers", "VS Code", "DX"],
            "image": "https://images.unsplash.com/photo-1520607162513-77705c0f0d4a?auto=format&fit=crop&w=1200&q=80",
            "link": "#",
        },
    ]

    experiences = [
        {
            "role": "Product Engineering Intern",
            "company": "Nova Labs",
            "timeframe": "2023 — Present",
            "summary": "Prototyped motion-heavy dashboards and shipped production-ready React + Flask surfaces.",
            "highlights": [
                "Cut render times by 38% via memoized data flows",
                "Partnered with design to build a living design system",
            ],
        },
        {
            "role": "Research Fellow",
            "company": "Human-Computer Interaction Lab",
            "timeframe": "2022 — 2023",
            "summary": "Explored tangible interfaces and spatial computing for inclusive education.",
            "highlights": [
                "Co-authored paper on adaptive haptics",
                "Built AR storytelling toolkit adopted by 4 classrooms",
            ],
        },
        {
            "role": "Freelance Creative Technologist",
            "company": "Self-Initiated",
            "timeframe": "Ongoing",
            "summary": "Partner with early-stage founders to transform sketches into launch-ready experiences.",
            "highlights": [
                "End-to-end delivery of 7 branded microsites",
                "Integrated analytics + A/B testing for rapid learning",
            ],
        },
    ]

    skill_groups = [
        {"title": "Core Stack", "stack": ["Python", "TypeScript", "Rust", "Go", "SQL", "GraphQL"]},
        {"title": "Frameworks", "stack": ["React", "Next.js", "Flask", "FastAPI", "Tailwind", "Framer Motion"]},
        {"title": "Tooling", "stack": ["Figma", "Notion", "Blender", "Docker", "AWS", "Vite"]},
    ]

    spotlights = [
        {
            "title": "Current focus",
            "description": "Building ambient computing prototypes that blur the line between physical and digital worlds.",
        },
        {
            "title": "Recent win",
            "description": "Led a team of 4 to sweep a 48-hour hackathon with an adaptive transit assistant.",
        },
        {
            "title": "What's next",
            "description": "Exploring generative UI systems + compiler-assisted design workflows.",
        },
    ]

    contact = {
        "email": "hello@avery.codes",
        "location": "Remote • Earth",
        "availability": "Open for internships, freelance collaborations, and research labs",
    }

    return render_template(
        "portfolio.html",
        hero=hero,
        stats=stats,
        projects=projects,
        experiences=experiences,
        skill_groups=skill_groups,
        spotlights=spotlights,
        contact=contact,
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


@bp.route("/member/books")
def member_books():
    redirect_response = require_role("member")
    if redirect_response:
        return redirect_response

    category_id = request.args.get("category", type=int)
    categories = Category.query.all()

    if category_id:
        book_list = Book.query.filter_by(category_id=category_id).all()
    else:
        book_list = Book.query.all()

    return render_template(
        "member/books.html",
        books=book_list,
        categories=categories,
        selected_category=category_id,
    )


@bp.route("/member/bookings")
def member_bookings():
    redirect_response = require_role("member")
    if redirect_response:
        return redirect_response

    member = current_member()
    bookings_list = (
        Booking.query.filter_by(user_id=member.id)
        .order_by(Booking.start_date.desc())
        .all()
    )
    return render_template("member/bookings.html", bookings=bookings_list, member=member)


@bp.route("/member/bookings/new", methods=["GET", "POST"])
def member_create_booking():
    redirect_response = require_role("member")
    if redirect_response:
        return redirect_response

    member = current_member()
    books = Book.query.all()

    if request.method == "POST":
        book_id = get_form_value("book_id", int)
        book = Book.query.get_or_404(book_id)
        if book.copies_available < 1:
            flash("No copies available", "warning")
            return redirect(url_for("library.member_create_booking"))

        booking = Booking(
            user_id=member.id,
            book_id=book_id,
            start_date=get_form_value("start_date", lambda v: date.fromisoformat(v)),
            end_date=get_form_value("end_date", lambda v: date.fromisoformat(v)),
        )
        book.copies_available -= 1
        db.session.add(booking)
        db.session.commit()
        flash("Booking created", "success")
        return redirect(url_for("library.member_bookings"))

    return render_template("member/booking_form.html", books=books, member=member)


@bp.route("/member/bookings/<int:booking_id>/return", methods=["POST"])
def member_return_booking(booking_id: int):
    redirect_response = require_role("member")
    if redirect_response:
        return redirect_response

    member = current_member()
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != member.id:
        flash("That booking does not belong to you.", "danger")
        return redirect(url_for("library.member_bookings"))

    if not booking.returned:
        booking.returned = True
        booking.book.copies_available += 1
        db.session.commit()
        flash("Book marked as returned", "success")

    return redirect(url_for("library.member_bookings"))


@bp.route("/member/ratings")
def member_ratings():
    redirect_response = require_role("member")
    if redirect_response:
        return redirect_response

    member = current_member()
    rating_list = (
        Rating.query.filter_by(user_id=member.id)
        .order_by(Rating.created_at.desc())
        .all()
    )
    return render_template("member/ratings.html", ratings=rating_list, member=member)


@bp.route("/member/ratings/new", methods=["GET", "POST"])
def member_create_rating():
    redirect_response = require_role("member")
    if redirect_response:
        return redirect_response

    member = current_member()
    books = Book.query.all()

    if request.method == "POST":
        rating = Rating(
            user_id=member.id,
            book_id=get_form_value("book_id", int),
            score=get_form_value("score", int),
            comment=get_form_value("comment"),
        )
        db.session.add(rating)
        db.session.commit()
        flash("Thanks for rating!", "success")
        return redirect(url_for("library.member_ratings"))

    return render_template("member/rating_form.html", books=books, member=member)
