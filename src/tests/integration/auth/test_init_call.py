import unittest

from flask import url_for
from src.tests.base import IntegrationBaseTest


class TestInitCall(IntegrationBaseTest):
    path = "/v1/app/init"

    def test_init_success(self):
        response = self.app.get(self.path)
        self.assertStatusCode(response, 200)

        actual_response = response.get_json()
        expected_response = {
            'actions':
                {
                    'pokemon_basic':
                        {
                            'href': url_for('rcpokemonbasic', pokemon_name='123'),
                        },
                    'pokemon_translated':
                        {
                            'href': url_for('rcpokemontranslated', pokemon_name='123'),
                        }
                }
        }
        self.assertDictStructure(expected_response, actual_response)

if __name__ == "__main__":
    unittest.main()