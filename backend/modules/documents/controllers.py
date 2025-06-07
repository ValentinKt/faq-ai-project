from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from uuid import UUID
from modules.documents.services import DocumentService
from utils.decorators import require_roles
from utils.exceptions import APIError
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('documents', __name__, url_prefix='/api/documents')

@bp.route('/', methods=['POST'])
@jwt_required()
@require_roles('admin', 'editor')
def upload_document():
    """Upload a document"""
    try:
        if 'file' not in request.files:
            raise APIError("No file provided", 400)
        
        file = request.files['file']
        user_id = UUID(get_jwt_identity()['id'])
        document = DocumentService.upload_document(file, user_id)
        
        return jsonify({
            "status": "success",
            "data": document,
            "message": "Document uploaded successfully"
        }), 201
    except APIError as e:
        logger.error(f"Document upload error: {str(e)}")
        return jsonify({"status": "error", "message": e.message}), e.status_code
    except Exception as e:
        logger.exception("Document upload failed")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@bp.route('/', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_documents():
    """Get all documents"""
    try:
        documents = DocumentService.get_all_documents()
        return jsonify({
            "status": "success",
            "data": documents,
            "message": "Documents retrieved successfully"
        }), 200
    except Exception as e:
        logger.exception("Failed to retrieve documents")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@bp.route('/', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_all_documents():
    """Retrieve all documents."""
    try:
        documents = DocumentService.get_all_documents()
        return jsonify({"status": "success", "data": documents}), 200
    except Exception as e:
        logger.exception("Error retrieving documents")
        return jsonify({"status": "error", "message": "Internal server error"}), 500