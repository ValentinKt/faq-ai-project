from marshmallow import Schema, fields

class FAQViewSchema(Schema):
    id = fields.UUID(dump_only=True)
    faq_id = fields.UUID(required=True)
    user_id = fields.UUID(allow_none=True)
    viewed_at = fields.DateTime(dump_only=True)

class FAQFeedbackSchema(Schema):
    id = fields.UUID(dump_only=True)
    faq_id = fields.UUID(required=True)
    user_id = fields.UUID(allow_none=True)
    is_helpful = fields.Boolean(required=True)
    feedback_text = fields.Str(allow_none=True, validate=lambda s: len(s) <= 1000 if s else True)
    created_at = fields.DateTime(dump_only=True)