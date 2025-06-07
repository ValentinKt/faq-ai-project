from sqlalchemy import Column, String, DateTime, ForeignKey, Table, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import db
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
import enum

class UserRoleEnum(enum.Enum):
    USER = "user"
    EDITOR = "editor"
    ADMIN = "admin"

# INITIAL_ROLES = [
#     {"name": UserRoleEnum.USER, "description": "Standard user with read-only access"},
#     {"name": UserRoleEnum.EDITOR, "description": "Can create and update FAQ entries"},
#     {"name": UserRoleEnum.ADMIN, "description": "Full administrative access"}
# ]   

user_roles = Table(
    'user_roles',
    db.Model.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True),
    Column('role_id', UUID(as_uuid=True), ForeignKey('roles.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    roles = relationship(UserRoleEnum, secondary=user_roles, back_populates="users")

    def set_password(self, password: str) -> None:
        """Set the user's password with hashing."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify the user's password."""
        return check_password_hash(self.password_hash, password)

    def has_role(self, role_name: str) -> bool:
        """Check if the user has a specific role."""
        return any(role.name == role_name for role in self.roles)

class Role(db.Model):
    __tablename__ = "roles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(Enum(UserRoleEnum), unique=True, nullable=False)
    description = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    users = relationship("User", secondary=user_roles, back_populates="roles")


INITIAL_ROLES = [
    {"name": UserRoleEnum.USER, "description": "Standard user with read-only access"},
    {"name": UserRoleEnum.EDITOR, "description": "Can create and update FAQ entries"},
    {"name": UserRoleEnum.ADMIN, "description": "Full administrative access"}
]