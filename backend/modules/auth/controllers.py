from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies, get_jwt
from uuid import UUID
from modules.auth.services import AuthService
from modules.auth.schemas import UserRegisterSchema, UserLoginSchema
from utils.decorators import require_roles
from utils.exceptions import APIError
from utils.validators import validate_request
from core.cache import cache
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST'])
@validate_request(UserRegisterSchema)
def register_user():
    """Register a new user."""
    try:
        data = request.get_json()
        user = AuthService.register_user(data)
        return jsonify({"status": "success", "data": user}), 201
    except APIError as e:
        logger.error(f"Registration failed: {e.message}")
        return jsonify({"status": "error", "message": e.message}), e.status_code
    except Exception as e:
        logger.exception("Unexpected error during registration")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@bp.route('/login', methods=['POST'])
@validate_request(UserLoginSchema)
def login_user():
    """Log in a user and return JWT token."""
    try:
        data = request.get_json()
        token = AuthService.login_user(data)
        response = jsonify({"status": "success", "data": {"access_token": token}})
        return response, 200
    except APIError as e:
        logger.error(f"Login failed: {e.message}")
        return jsonify({"status": "error", "message": e.message}), e.status_code
    except Exception as e:
        logger.exception("Unexpected error during login")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout_user():
    """Log out a user and revoke JWT token."""
    try:
        jti = get_jwt()["jti"]
        cache.set(f"blocklist:{jti}", "true", timeout=3600)
        response = jsonify({"status": "success", "message": "Logged out successfully"})
        unset_jwt_cookies(response)
        logger.info(f"User logged out: {get_jwt_identity()['email']}")
        return response, 200
    except Exception as e:
        logger.exception("Unexpected error during logout")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@bp.route('/me', methods=['GET'])
@jwt_required()
@require_roles('user', 'editor', 'admin')
def get_current_user():
    """Get details of the current user."""
    try:
        user_id = UUID(get_jwt_identity()['id'])
        user = AuthService.get_user_by_id(user_id)
        if not user:
            return jsonify({"status": "error", "message": "User not found"}), 404
        return jsonify({"status": "success", "data": user}), 200
    except Exception as e:
        logger.exception("Unexpected error retrieving user")
        return jsonify({"status": "error", "message": "Internal server error"}), 500