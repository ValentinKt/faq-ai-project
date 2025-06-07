from functools import wraps
from flask import request
from utils.exceptions import APIError
import logging

logger = logging.getLogger(__name__)

def validate_request(schema):
    """Decorator to validate request data against a schema."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json() or {}
            try:
                result = schema().load(data)
            except Exception as e:
                logger.error(f"Validation errors: {str(e)}")
                raise APIError(f"Validation errors: {str(e)}", 400)
            request.validated_data = result
            return f(*args, **kwargs)
        return decorated_function
    return decorator
