from flask import url_for
from src.tests.base import IntegrationBaseTest


class InitCallTest(IntegrationBaseTest):
    path = "/v1/app/init"

    def test_init_success(self):
        response = self.app.get(self.path)
        self.assertStatusCode(response, 200)

        actual_response = response.get_json()
        expected_response = {
            'success': True,
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
        self.assertDictStructure(expected_response, actual_response)
