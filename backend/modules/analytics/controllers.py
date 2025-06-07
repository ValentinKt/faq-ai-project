from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from uuid import UUID
from typing import Dict, Any
from modules.analytics.services import AnalyticsService
from modules.analytics.schemas import FAQFeedbackSchema
from utils.decorators import require_roles
from utils.exceptions import APIError
from utils.validators import validate_request
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

@bp.route('/faq/<uuid:faq_id>/view', methods=['POST'])
@jwt_required()
def log_faq_view(faq_id: UUID) -> Dict[str, Any]:
    """Log a view for a specific FAQ."""
    try:
        user_id = UUID(get_jwt_identity()['id'])
        view = AnalyticsService.log_faq_view(faq_id, user_id)
        return jsonify({
            "status": "success",
            "data": view,
            "message": "FAQ view logged successfully"
        }), 201
    except Exception as e:
        logger.error(f"FAQ view logging failed: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@bp.route('/faq/<uuid:faq_id>/feedback', methods=['POST'])
@jwt_required()
@validate_request(FAQFeedbackSchema)
def log_faq_feedback(faq_id: UUID) -> Dict[str, Any]:
    """Log feedback for a specific FAQ."""
    try:
        data = request.get_json()
        data['faq_id'] = str(faq_id)
        user_id = UUID(get_jwt_identity()['id'])
        feedback = AnalyticsService.log_faq_feedback(data, user_id)
        return jsonify({
            "status": "success",
            "data": feedback,
            "message": "FAQ feedback logged successfully"
        }), 201
    except APIError as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), e.status_code
    except Exception as e:
        logger.error(f"FAQ feedback logging failed: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@bp.route('/faq/<uuid:faq_id>/views', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_faq_views(faq_id: UUID) -> Dict[str, Any]:
    """Retrieve all views for a specific FAQ."""
    try:
        views = AnalyticsService.get_faq_views(faq_id)
        return jsonify({
            "status": "success",
            "data": views,
            "message": "FAQ views retrieved successfully"
        }), 200
    except Exception as e:
        logger.error(f"FAQ views retrieval failed: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@bp.route('/faq/<uuid:faq_id>/feedback', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_faq_feedback(faq_id: UUID) -> Dict[str, Any]:
    """Retrieve all feedback for a specific FAQ."""
    try:
        feedback = AnalyticsService.get_faq_feedback(faq_id)
        return jsonify({
            "status": "success",
            "data": feedback,
            "message": "FAQ feedback retrieved successfully"
        }), 200
    except Exception as e:
        logger.error(f"FAQ feedback retrieval failed: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500