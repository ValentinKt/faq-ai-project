from typing import Dict, Optional
from uuid import UUID
from flask_jwt_extended import create_access_token
from core.database import db, database_manager
from modules.auth.models import User, Role, UserRoleEnum
from modules.auth.schemas import UserSchema
from utils.exceptions import APIError
import logging

INITIAL_ROLES = [
    {"name": UserRoleEnum.ADMIN, "description": "Administrator"},
    {"name": UserRoleEnum.EDITOR, "description": "Editor"},
    {"name": UserRoleEnum.USER, "description": "Standard user"}
]
logger = logging.getLogger(__name__)

class AuthService:
    """Handles authentication and user management."""

    @staticmethod
    def register_user(data: Dict) -> Dict:
        """Register a new user with default role."""
        with database_manager.session_scope() as session:
            if session.query(User).filter_by(email=data['email']).first():
                raise APIError("User with this email already exists", 409)

            user = User(
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name']
            )
            user.set_password(data['password'])

            user_role = session.query(Role).filter_by(name=UserRoleEnum.USER).first()
            if not user_role:
                user_role = Role(name=UserRoleEnum.USER, description="Standard user")
                session.add(user_role)
            user.roles.append(user_role)

            session.add(user)
            session.flush()
            logger.info(f"User registered: {user.email}")
            return UserSchema().dump(user)

    @staticmethod
    def login_user(data: Dict) -> str:
        """Authenticate user and return JWT token."""
        with database_manager.session_scope() as session:
            user = session.query(User).filter_by(email=data['email']).first()
            if not user or not user.check_password(data['password']):
                raise APIError("Invalid credentials", 401)

            identity = {
                "id": str(user.id),
                "email": user.email,
                "roles": [role.name.value for role in user.roles]
            }
            token = create_access_token(identity=identity)
            logger.info(f"User logged in: {user.email}")
            return token

    @staticmethod
    def get_user_by_id(user_id: UUID) -> Optional[Dict]:
        """Retrieve user details by ID."""
        with database_manager.session_scope() as session:
            user = session.query(User).get(user_id)
            if user:
                return UserSchema().dump(user)
            return None

    @staticmethod
    def seed_initial_roles() -> None:
        """Seed initial roles if they don't exist."""
        with database_manager.session_scope() as session:
            for role_data in INITIAL_ROLES:
                if not session.query(Role).filter_by(name=role_data['name']).first():
                    role = Role(name=role_data['name'], description=role_data['description'])
                    session.add(role)
            logger.info("Initial roles seeded")