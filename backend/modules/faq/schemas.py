from marshmallow import Schema, fields, validate

class FAQEntrySchema(Schema):
    id = fields.UUID(dump_only=True)
    parent_id = fields.UUID(allow_none=True)
    question = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    answer = fields.Str(required=True, validate=validate.Length(min=1, max=5000))
    category_id = fields.UUID(allow_none=True)
    document_id = fields.UUID(allow_none=True)
    created_by = fields.UUID(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    status = fields.Str(dump_only=True)
    version = fields.Int(dump_only=True)