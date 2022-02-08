from marshmallow import fields
from marshmallow.validate import OneOf

from src.bootstrap.bootstrap_the_app import api
from src.core.resource import BaseResource
from src.core.schema import BaseSchema
from src.domain import *


class RcPokemonTranslated(BaseResource):
    path = "/v1/pokemon/translated/{pokemon_name}"

    def get(self):
        resp = {
            'name': '',
            'description': '',
            'habitat': '',
            'isLegendary': '',
        }

        return self.respond(resp)


api.add_resource(RcPokemonTranslated, RcPokemonTranslated.path)
