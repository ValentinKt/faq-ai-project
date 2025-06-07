from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from core.database import db
from uuid import uuid4

class FAQAnalytics(db.Model):
    __tablename__ = "faq_analytics"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    faq_id = Column(UUID(as_uuid=True), ForeignKey("faq_entries.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    action = Column(String(50), nullable=False)  # e.g., 'view', 'feedback'
    is_helpful = Column(Boolean)
    feedback_text = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class FAQView(db.Model):
    __tablename__ = "faq_views"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    faq_id = Column(UUID(as_uuid=True), ForeignKey("faq_entries.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    viewed_at = Column(DateTime, default=func.now())

class FAQFeedback(db.Model):
    __tablename__ = "faq_feedback"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    faq_id = Column(UUID(as_uuid=True), ForeignKey("faq_entries.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    is_helpful = Column(Boolean, nullable=False)
    feedback_text = Column(String(1000), nullable=True)
    created_at = Column(DateTime, default=func.now())