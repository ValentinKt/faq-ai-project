from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from modules.ai.services import AIService
from utils.decorators import require_roles
from uuid import UUID
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('ai', __name__, url_prefix='/api/ai')

@bp.route('/generate-faq', methods=['POST'])
@jwt_required()
@require_roles('admin', 'editor')
def generate_faq():
    """Generate an FAQ using AI."""
    try:
        data = request.get_json()
        query = data.get('query')
        document_ids = [UUID(did) for did in data.get('document_ids', [])]
        if not query:
            return jsonify({"status": "error", "message": "Query is required"}), 400
        result = AIService().generate_faq(query, document_ids)
        return jsonify({"status": "success", "data": result}), 200
    except Exception as e:
        logger.exception("Error generating FAQ with AI")
        return jsonify({"status": "error", "message": "Internal server error"}), 500