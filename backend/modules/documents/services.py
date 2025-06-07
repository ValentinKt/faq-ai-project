import os
import logging
from uuid import UUID
from typing import Dict
from werkzeug.datastructures import FileStorage
from flask import current_app
from core.database import db, database_manager
from modules.documents.models import Document
from modules.documents.schemas import DocumentSchema
from config.settings import settings
from threading import Thread
from modules.ai.services import AIService

logger = logging.getLogger(__name__)

class DocumentService:
    """Service for document upload and processing"""

    @staticmethod
    def upload_document(file: FileStorage, user_id: UUID) -> Dict:
        try:
            if not file or not file.filename:
                raise APIError("No file provided", 400)
            filename = os.path.basename(file.filename)
            if not filename or '..' in filename or filename.startswith('.'):
                raise APIError("Invalid filename", 400)
            filepath = os.path.join(settings.UPLOAD_FOLDER, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            file.save(filepath)
            with database_manager.session_scope() as session:
                document = Document(
                    filename=filename,
                    filepath=filepath,
                    file_type=file.content_type,
                    uploaded_by=user_id
                )
                session.add(document)
                session.flush()
                Thread(
                    target=DocumentService.process_document,
                    args=(document.id,),
                    daemon=True
                ).start()
                return DocumentSchema().dump(document)
        except APIError:
            raise
        except Exception as e:
            logger.error(f"Document upload failed: {str(e)}")
            raise APIError("Document upload failed", 500)

    @staticmethod
    def process_document(document_id: UUID):
        try:
            with database_manager.session_scope() as session:
                document = session.query(Document).get(document_id)
                if not document:
                    logger.error(f"Document not found: {document_id}")
                    return
                text = f"Content extracted from {document.filename}"
                AIService().store_document_embedding(document.id, text)
                document.status = "processed"
                document.processed_at = func.now()
                logger.info(f"Processed document: {document_id}")
        except Exception as e:
            logger.error(f"Document processing failed: {str(e)}")
            with database_manager.session_scope() as session:
                document = session.query(Document).get(document_id)
                if document:
                    document.status = "failed"

    @staticmethod
    def get_all_documents() -> list:
        try:
            with database_manager.session_scope() as session:
                documents = session.query(Document).all()
                return DocumentSchema(many=True).dump(documents)
        except Exception as e:
            logger.error(f"Failed to retrieve documents: {str(e)}")
            raise APIError("Failed to retrieve documents", 500)