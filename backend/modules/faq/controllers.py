from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from uuid import UUID
from modules.faq.services import FAQService
from modules.faq.schemas import FAQEntrySchema
from utils.decorators import require_roles
from utils.validators import validate_request
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('faq', __name__, url_prefix='/api/faq')

@bp.route('/', methods=['POST'])
@jwt_required()
@require_roles('admin', 'editor')
@validate_request(FAQEntrySchema)
def create_faq():
    """Create a new FAQ entry."""
    try:
        data = request.get_json()
        user_id = UUID(get_jwt_identity()['id'])
        faq = FAQService.create_faq(data, user_id)
        return jsonify({"status": "success", "data": faq}), 201
    except Exception as e:
        logger.exception("Error creating FAQ")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@bp.route('/<uuid:faq_id>', methods=['PUT'])
@jwt_required()
@require_roles('admin', 'editor')
@validate_request(FAQEntrySchema)
def update_faq(faq_id: UUID):
    """Update an existing FAQ entry."""
    try:
        data = request.get_json()
        user_id = UUID(get_jwt_identity()['id'])
        faq = FAQService.update_faq(faq_id, data, user_id)
        if not faq:
            return jsonify({"status": "error", "message": "FAQ not found"}), 404
        return jsonify({"status": "success", "data": faq}), 200
    except Exception as e:
        logger.exception("Error updating FAQ")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@bp.route('/<uuid:faq_id>', methods=['GET'])
def get_faq(faq_id: UUID):
    """Retrieve a specific FAQ entry."""
    try:
        faq = FAQService.get_faq_by_id(faq_id)
        if not faq:
            return jsonify({"status": "error", "message": "FAQ not found"}), 404
        return jsonify({"status": "success", "data": faq}), 200
    except Exception as e:
        logger.exception("Error retrieving FAQ")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@bp.route('/', methods=['GET'])
def get_all_faqs():
    """Retrieve all published FAQs."""
    try:
        faqs = FAQService.get_all_faqs()
        return jsonify({"status": "success", "data": faqs}), 200
    except Exception as e:
        logger.exception("Error retrieving FAQs")
        return jsonify({"status": "error", "message": "Internal server error"}), 500