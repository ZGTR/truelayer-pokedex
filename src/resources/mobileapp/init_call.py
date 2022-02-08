from flask import url_for

from src.bootstrap.bootstrap_the_app import api
from src.core.resource import BaseResource


class RcMobileAppInitV1(BaseResource):
    path = "/v1/app/init"

    def get(self):
        print('----- in resource')
        resp = {
            'actions':
                {
                    'pokemon_basic_description':
                        {
                            'href': url_for('rcpokemonbasic'),
                        },
                    'pokemon_translated_description':
                        {
                            'href': url_for('rcpokemontranslated'),
                        },

                }
        }
        return self.respond(resp)


api.add_resource(RcMobileAppInitV1, RcMobileAppInitV1.path)
