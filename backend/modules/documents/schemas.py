from marshmallow import Schema, fields, validate

class DocumentSchema(Schema):
    id = fields.UUID(dump_only=True)
    filename = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    filepath = fields.Str(dump_only=True)
    file_type = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    uploaded_by = fields.UUID(dump_only=True)
    uploaded_at = fields.DateTime(dump_only=True)
    processed_at = fields.DateTime(allow_none=True, dump_only=True)
    status = fields.Str(dump_only=True)