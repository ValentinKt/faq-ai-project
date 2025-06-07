from sqlalchemy import Column, String, Integer, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from core.database import db
from uuid import uuid4
import enum

class FAQStatus(enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class FAQCategory(db.Model):
    __tablename__ = "faq_categories"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))
    created_at = Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = Column(db.DateTime(timezone=True), onupdate=func.now())

class FAQEntry(db.Model):
    __tablename__ = "faq_entries"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("faq_entries.id"), nullable=True)
    question = Column(String(255), nullable=False, index=True)
    answer = Column(String(5000), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("faq_categories.id"), index=True)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), index=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(db.DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(db.DateTime(timezone=True), onupdate=func.now())
    status = Column(Enum(FAQStatus), default=FAQStatus.DRAFT, index=True)
    version = Column(Integer, default=1)