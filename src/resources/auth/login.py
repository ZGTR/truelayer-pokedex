from marshmallow import fields, pre_load

from src.bootstrap.bootstrap_the_app import api, config
from src.core.resource import BaseResource
from src.core.schema import BaseSchema
from src.domain import User


class SchemaSignIn(BaseSchema):
    username = fields.String(required=True, validate=BaseSchema.not_blank)
    password = fields.String(required=True, validate=BaseSchema.not_blank)

    @pre_load
    def strip_data(self, in_data, **kwargs):
        if 'username' in in_data:
            in_data['username'] = in_data['username'].lower().strip()
        if 'password' in in_data:
            in_data['password'] = in_data['password'].lower().strip()
        return in_data


class RcUserLogin(BaseResource):
    path = '/v1/user/auth/login'

    method_decorators = dict(
        post=[SchemaSignIn()]
    )

    def post(self, validated_data):
        self.logRequest()
        success, msg, current_user, access_token, refresh_token = User.user_login(validated_data.username,
                                                                                  validated_data.password)

        if not success:
            return self.respond_error(msg, 400)

        resp = {
            'token': {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'expires_in': config.JWT_ACCESS_TOKEN_EXPIRES.total_seconds()
            }
        }
        return self.respond(resp)


api.add_resource(RcUserLogin, RcUserLogin.path)
