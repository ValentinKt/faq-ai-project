from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config.settings import settings
from core.database import db, database_manager
from core.cache import cache
from modules.auth.controllers import bp as auth_bp
from modules.faq.controllers import bp as faq_bp
from modules.documents.controllers import bp as documents_bp
from modules.ai.controllers import bp as ai_bp
from modules.analytics.controllers import bp as analytics_bp
from modules.auth.services import AuthService
import logging

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = settings.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['JWT_SECRET_KEY'] = settings.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = settings.JWT_ACCESS_TOKEN_EXPIRES
app.config['MAX_CONTENT_LENGTH'] = settings.MAX_CONTENT_LENGTH
app.config['CACHE_REDIS_URL'] = settings.REDIS_URL

# Logging
logging.basicConfig(level=logging.INFO if not settings.DEBUG else logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize extensions
database_manager.init_app(app)
cache.init_app(app)
jwt = JWTManager(app)
CORS(app, supports_credentials=True)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(faq_bp)
app.register_blueprint(documents_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(analytics_bp)

@jwt.token_in_blocklist_loader
def check_if_token_revoked(_, jwt_payload):
    """Check if a JWT token is in the blocklist"""
    jti = jwt_payload["jti"]
    return cache.get(f"blocklist:{jti}") is not None


# Replace the @app.before_first_request with:
# Add this near your other CLI commands
@app.cli.command("init-db")
def initialize_db():
    """Initialize the database."""
    db.create_all()
    AuthService.seed_initial_roles()
    logger.info("Application initialized")

def create_app():
    """Create the Flask app instance."""
    # With this:
    with app.app_context():
        # This code will run when the application starts
        def initialize_app():
            """Initialize roles and database"""
            db.create_all()
            AuthService.seed_initial_roles()
            logger.info("Application initialized")
        
        # Call the function immediately
        initialize_app()
    return app
# Replace the @app.before_first_request with:



if __name__ == '__main__':
    app.run(debug=settings.DEBUG, host='127.0.0.1', port=8000)