from marshmallow import fields
from marshmallow.validate import OneOf

from src.bootstrap.bootstrap_the_app import api
from src.core.resource import BaseResource
from src.core.schema import BaseSchema
from src.domain import *


class SchemaPokemonBasic(BaseSchema):
    name = fields.String(required=True)
    # impaired_hand = fields.String(required=True, validate=OneOf(ImpairedHand.values()))


class RcPokemonBasic(BaseResource):
    path = "/v1/pokemon/"
    # decorators = [jwt_required]
    method_decorators = dict(
        post=[SchemaPokemonBasic()]
    )

    def post(self, validated_data):

        if success:
            return self.respond(dict(
                impaired_hand=validated_data.impaired_hand
            ))

        return self.respond_error(msg, 400)


api.add_resource(RcPokemonBasic, RcPokemonBasic.path)
