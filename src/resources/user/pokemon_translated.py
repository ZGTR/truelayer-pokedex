from marshmallow import fields
from marshmallow.validate import OneOf
from flask_restful import Resource

from src.bootstrap.bootstrap_the_app import api
from src.core.schema import BaseSchema
from src.domain import *


class RcPokemonTranslated(Resource):
    path = "/v1/pokemon/translated/<string:pokemon_name>"

    def get(self, pokemon_name):
        # Better to have Base Resource class which handles schemas (Marshmallow) abstractly with its errors.

        resp = {
            'name': pokemon_name,
            'description': '',
            'habitat': '',
            'isLegendary': ''
        }
        return resp


api.add_resource(RcPokemonTranslated, RcPokemonTranslated.path)


