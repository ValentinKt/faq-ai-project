from functools import wraps
from flask import abort
from flask_jwt_extended import get_jwt_identity
from modules.auth.models import User
from core.database import database_manager
import logging

logger = logging.getLogger(__name__)

def require_roles(*roles):
    """Decorator to restrict access based on user roles."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            identity = get_jwt_identity()
            if not identity:
                abort(401, description="Authentication required")
            with database_manager.session_scope() as session:
                user = session.query(User).get(identity['id'])
                if not user or not any(user.has_role(role) for role in roles):
                    logger.warning(f"Access denied for user {identity['email']} to {f.__name__}")
                    abort(403, description="Insufficient permissions")
            return f(*args, **kwargs)
        return decorated_function
    return decorator