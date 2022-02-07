from marshmallow import fields, validates_schema, ValidationError, pre_load
from marshmallow.validate import OneOf

from src.bootstrap.bootstrap_the_app import api
from src.core.resource import BaseResource
from src.core.schema import BaseSchema
from src.domain import *
from src.enums import Country


class SchemaAdminUserSignUp(BaseSchema):
    email = fields.Email(required=True, validate=BaseSchema.not_blank)
    username = fields.String(required=True, validate=BaseSchema.not_blank)
    password = fields.String(required=True, validate=BaseSchema.not_blank)
    firstname = fields.String(required=True, validate=BaseSchema.not_blank)
    lastname = fields.String(required=True, validate=BaseSchema.not_blank)
    user_group = fields.String(required=True, validate=BaseSchema.not_blank)
    country = fields.String(required=True, validate=OneOf(Country.values()))

    @pre_load
    def strip_data(self, in_data, **kwargs):
        if 'username' in in_data:
            in_data['username'] = in_data['username'].lower().strip()
        if 'email' in in_data:
            in_data['email'] = in_data['email'].lower().strip()
        return in_data

    @validates_schema
    def validate_email(self, data, **kwargs):
        if data['email'] != data['username']:
            raise ValidationError('Email is not the same as Username. For now this is not permitted.',
                                  field_name='email_username')


class RcAdminUserSignup(BaseResource):
    path = "/admin/v1/user/signup"

    # decorators = [jwt_required]

    method_decorators = dict(
        post=[SchemaAdminUserSignUp()]
    )

    def post(self, validated_data):
        self.logRequest()
        success, user, msg = User.user_signup(validated_data)

        if not success:
            return self.respond_error(msg, 400)

        return self.respond(user)


api.add_resource(RcAdminUserSignup, RcAdminUserSignup.path)
