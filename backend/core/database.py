from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

db = SQLAlchemy()
migrate = Migrate()

class DatabaseManager:
    """Manages database connections and sessions."""

    @staticmethod
    def init_app(app) -> None:
        """Initialize the database with the Flask app."""
        db.init_app(app)
        migrate.init_app(app, db)
        logger.info("Database initialized with Flask app")

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope for database operations."""
        session = db.session
        try:
            yield session
            session.commit()
            logger.debug("Database transaction committed")
        except Exception as e:
            session.rollback()
            logger.error(f"Database transaction failed: {str(e)}")
            raise
        finally:
            session.close()

database_manager = DatabaseManager()