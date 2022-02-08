from src.bootstrap.bootstrap_the_app import api
from src.core.resource import BaseResource
from src.core.schema import BaseSchema
from src.domain import *


class RcPokemonBasic(BaseResource):
    path = "/v1/pokemon/{pokemon_name}"

    def get(self):
        resp = {
            'name': '',
            'description': '',
            'habitat': '',
            'isLegendary': ''
        }
        return self.respond(resp)


api.add_resource(RcPokemonBasic, RcPokemonBasic.path)
