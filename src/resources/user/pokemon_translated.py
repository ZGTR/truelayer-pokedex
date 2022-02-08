from marshmallow import fields
from marshmallow.validate import OneOf
from flask_restful import Resource

from src.bootstrap.bootstrap_the_app import api, BaseResource
from src.domain import *


class RcPokemonTranslated(BaseResource):
    # Better to create logic in TrueLayerResource class which handles schemas (Marshmallow) abstractly with its errors.
    path = "/v1/pokemon/translated/<string:pokemon_name>"

    def get(self, pokemon_name):

        # We can return this directly from pokemon.__repr__ and JSONify it.
        # But, since we want to separate between presentation API and logic API, it's better to keep them separate.
        resp = {
            'name': pokemon_name,
            'description': '',
            'habitat': '',
            'isLegendary': True
        }
        return resp


api.add_resource(RcPokemonTranslated, RcPokemonTranslated.path)


