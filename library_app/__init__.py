from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

# Initialize extensions

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config: dict | None = None) -> Flask:
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    from . import routes  # noqa: WPS433

    app.register_blueprint(routes.bp)

    @app.cli.command("seed")
    def seed_data() -> None:
        """Seed the database with sample data."""
        from .seed import seed_database

        seed_database()

    return app
