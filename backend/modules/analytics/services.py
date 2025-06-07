from typing import Dict, List
from uuid import UUID
from core.database import db, database_manager
from modules.analytics.models import FAQView, FAQFeedback
from modules.analytics.schemas import FAQViewSchema, FAQFeedbackSchema
import logging

logger = logging.getLogger(__name__)

class AnalyticsService:
    """Service layer for analytics operations."""

    @staticmethod
    def log_faq_view(faq_id: UUID, user_id: UUID = None) -> Dict:
        """Log a view for a specific FAQ."""
        try:
            with database_manager.session_scope() as session:
                view = FAQView(faq_id=faq_id, user_id=user_id)
                session.add(view)
                session.flush()
                return FAQViewSchema().dump(view)
        except Exception as e:
            logger.error(f"Failed to log FAQ view: {e}")
            raise

    @staticmethod
    def log_faq_feedback(data: Dict, user_id: UUID = None) -> Dict:
        """Log feedback for a specific FAQ."""
        try:
            with database_manager.session_scope() as session:
                feedback = FAQFeedback(
                    faq_id=data['faq_id'],
                    user_id=user_id,
                    is_helpful=data['is_helpful'],
                    feedback_text=data.get('feedback_text')
                )
                session.add(feedback)
                session.flush()
                return FAQFeedbackSchema().dump(feedback)
        except Exception as e:
            logger.error(f"Failed to log FAQ feedback: {e}")
            raise

    @staticmethod
    def get_faq_views(faq_id: UUID) -> List[Dict]:
        """Retrieve all views for a specific FAQ."""
        try:
            with database_manager.session_scope() as session:
                views = session.query(FAQView).filter_by(faq_id=faq_id).all()
                return FAQViewSchema(many=True).dump(views)
        except Exception as e:
            logger.error(f"Failed to retrieve FAQ views: {e}")
            raise

    @staticmethod
    def get_faq_feedback(faq_id: UUID) -> List[Dict]:
        """Retrieve all feedback for a specific FAQ."""
        try:
            with database_manager.session_scope() as session:
                feedback = session.query(FAQFeedback).filter_by(faq_id=faq_id).all()
                return FAQFeedbackSchema(many=True).dump(feedback)
        except Exception as e:
            logger.error(f"Failed to retrieve FAQ feedback: {e}")
            raise