from marshmallow import fields
from marshmallow.validate import OneOf

from src.bootstrap.bootstrap_the_app import api
from src.core.resource import BaseResource
from src.core.schema import BaseSchema
from src.domain import *
from src.enums import ImpairedHand


class SchemaImpairedHand(BaseSchema):
    impaired_hand = fields.String(required=True, validate=OneOf(ImpairedHand.values()))


class RcImpairedHand(BaseResource):
    path = "/v1/user/impaired-hand"
    decorators = [jwt_required]
    method_decorators = dict(
        post=[SchemaImpairedHand()]
    )

    def post(self, validated_data):
        self.logRequest()
        success, msg = UserModel.set_impaired_hand(validated_data.impaired_hand)

        if success:
            return self.respond(dict(
                impaired_hand=validated_data.impaired_hand
            ))

        return self.respond_error(msg, 400)


api.add_resource(RcImpairedHand, RcImpairedHand.path)
