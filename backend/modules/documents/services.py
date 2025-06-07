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
        """Upload and process a document"""
        try:
            # Save file to uploads directory
            filename = file.filename
            filepath = os.path.join(settings.UPLOAD_FOLDER, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            file.save(filepath)
            
            # Create document record
            with database_manager.session_scope() as session:
                document = Document(
                    filename=filename,
                    filepath=filepath,
                    file_type=file.content_type,
                    uploaded_by=user_id
                )
                session.add(document)
                session.flush()
                
                # Start background processing
                Thread(
                    target=DocumentService.process_document, 
                    args=(document.id,)
                ).start()
                
                return DocumentSchema().dump(document)
        except Exception as e:
            logger.error(f"Document upload failed: {str(e)}")
            raise

    @staticmethod
    def process_document(document_id: UUID):
        """Process document content in background"""
        try:
            with database_manager.session_scope() as session:
                document = session.query(Document).get(document_id)
                if not document:
                    logger.error(f"Document not found: {document_id}")
                    return
                
                # Simulate text extraction (real implementation would use PyMuPDF)
                text = f"Content extracted from {document.filename}"
                
                # Store embedding in vector database
                AIService().store_document_embedding(document.id, text)
                
                # Update document status
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
        """Retrieve all documents"""
        with database_manager.session_scope() as session:
            documents = session.query(Document).all()
            return DocumentSchema(many=True).dump(documents)