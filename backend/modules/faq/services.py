from typing import Dict, List, Optional
from uuid import UUID
from core.database import db, database_manager
from modules.faq.models import FAQEntry, FAQStatus
from modules.faq.schemas import FAQEntrySchema
from core.cache import cache
import logging

logger = logging.getLogger(__name__)

class FAQService:
    """Manages FAQ entries with caching and versioning."""

    @staticmethod
    @cache.memoize(timeout=300)
    def get_faq_by_id(faq_id: UUID) -> Optional[Dict]:
        """Retrieve an FAQ by ID with caching."""
        with database_manager.session_scope() as session:
            faq = session.query(FAQEntry).get(faq_id)
            if faq:
                return FAQEntrySchema().dump(faq)
        return None

    @staticmethod
    @cache.memoize(timeout=300)
    def get_all_faqs() -> List[Dict]:
        """Retrieve all published FAQs with caching."""
        with database_manager.session_scope() as session:
            faqs = session.query(FAQEntry).filter_by(status=FAQStatus.PUBLISHED).all()
            return FAQEntrySchema(many=True).dump(faqs)

    @staticmethod
    def create_faq(data: Dict, user_id: UUID) -> Dict:
        """Create a new FAQ entry."""
        with database_manager.session_scope() as session:
            faq = FAQEntry(
                question=data['question'],
                answer=data['answer'],
                category_id=data.get('category_id'),
                document_id=data.get('document_id'),
                created_by=user_id,
                status=FAQStatus.DRAFT
            )
            session.add(faq)
            session.flush()
            FAQService._invalidate_cache(faq)
            logger.info(f"FAQ created: {faq.id}")
            return FAQEntrySchema().dump(faq)

    @staticmethod
    def update_faq(faq_id: UUID, data: Dict, user_id: UUID) -> Optional[Dict]:
        """Update an FAQ with versioning."""
        with database_manager.session_scope() as session:
            original = session.query(FAQEntry).get(faq_id)
            if not original:
                return None
            new_faq = FAQEntry(
                parent_id=original.id,
                question=data.get('question', original.question),
                answer=data.get('answer', original.answer),
                category_id=data.get('category_id', original.category_id),
                document_id=data.get('document_id', original.document_id),
                created_by=user_id,
                status=FAQStatus.DRAFT,
                version=original.version + 1
            )
            session.add(new_faq)
            original.status = FAQStatus.ARCHIVED
            session.flush()
            FAQService._invalidate_cache(original)
            FAQService._invalidate_cache(new_faq)
            logger.info(f"FAQ updated: {new_faq.id}")
            return FAQEntrySchema().dump(new_faq)

    @staticmethod
    def _invalidate_cache(faq: FAQEntry) -> None:
        """Invalidate cache for an FAQ."""
        cache.delete_memoized(FAQService.get_faq_by_id, faq.id)
        cache.delete_memoized(FAQService.get_all_faqs)
        logger.debug(f"Cache invalidated for FAQ: {faq.id}")