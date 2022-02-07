from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity, create_access_token
from marshmallow import fields

from src.bootstrap.bootstrap_the_app import api
from src.bootstrap_stages.stage01 import config
from src.core.resource import BaseResource
from src.core.schema import BaseSchema
from src.models.api_client import ApiClientModel


class SchemaTokenRefresh(BaseSchema):
    client_id = fields.String(required=True, validate=BaseSchema.not_blank)
    client_secret = fields.String(required=True, validate=BaseSchema.not_blank)


class RcTokenRefresh(BaseResource):
    path = '/v1/user/auth/token/refresh'

    method_decorators = dict(
        post=[SchemaTokenRefresh()]
    )

    @jwt_refresh_token_required
    def post(self, validated_data):
        self.logRequest()
        client_id = validated_data.client_id
        client_secret = validated_data.client_secret

        ddb_client = ApiClientModel.get_by_client_data(client_id, client_secret)

        if not ddb_client:
            return self.respond_error('You are not an authorized client.', 403)

        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return self.respond(dict(
            access_token=access_token,
            expires_in=config.JWT_ACCESS_TOKEN_EXPIRES.total_seconds()
        ))


api.add_resource(RcTokenRefresh, RcTokenRefresh.path)
