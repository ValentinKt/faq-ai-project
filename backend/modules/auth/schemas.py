from marshmallow import Schema, fields, validate, post_load
from modules.auth.models import UserRoleEnum

class UserSchema(Schema):
    id = fields.UUID(dump_only=True)
    email = fields.Email(required=True)
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=80))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=80))
    roles = fields.List(fields.Str(), dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class UserRegisterSchema(UserSchema):
    password = fields.Str(required=True, validate=validate.Length(min=8))

    @post_load
    def set_default_role(self, data, **kwargs):
        """Set default user role if none provided."""
        if 'roles' not in data:
            data['roles'] = [UserRoleEnum.USER.value]
        return data

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)