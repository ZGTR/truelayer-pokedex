from flask import url_for
from flask_restful import Resource

from src.bootstrap.bootstrap_the_app import api, BaseResource


class RcAppInit(BaseResource):
    path = "/v1/app/init"

    def get(self):
        resp = {
            'actions':
                {
                    'pokemon_basic':
                        {
                            'href': url_for('rcpokemonbasic', pokemon_name=''),
                        },
                    'pokemon_translated':
                        {
                            'href': url_for('rcpokemontranslated', pokemon_name=''),
                        }
                }
        }
        return resp


api.add_resource(RcAppInit, RcAppInit.path)
