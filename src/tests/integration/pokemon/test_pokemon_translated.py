import unittest
from string import Template
from unittest import skip
from unittest.mock import patch
import mock
from mock import patch

import requests

from src.domain.translation_strategies.pokemon_translation_strategy_yoda import PokemonTranslationStrategyYoda
from src.services import ClientPokeApi
from src.tests.base import BaseTest

TRANSLATED_DESCRIPTION = Template(f'This is the translation of \'$description\'')


def mocked_translate(an_instance, description):
    return TRANSLATED_DESCRIPTION.substitute(description=description)

class TestPokemonTranslated(BaseTest):
    # The translation API may have an extremely low limit (5 per hour).
    # Therefore, we'll mock the translation API call responses.

    def test_happy_scenario(self):
        with mock.patch.object(PokemonTranslationStrategyYoda, 'translate', new=mocked_translate):
            # We can use specific resource path instead of hard-coding it here.
            path = "/v1/pokemon/translated/mewtwo"

            response = self.app.get(path)

            self.assertStatusCode(response, 200)

            actual_response = response.get_json()

            expected_response = dict(
                name= 'mewtwo',
                # Since the business requirement is that any PokeAPI.pokemon.description works,
                # we can mock this to make this work regardless of the 3rd party API changing behaviour
                description= TRANSLATED_DESCRIPTION.substitute(description=
                                                               'It was created by\na scientist after\nyears of horrific\fgene splicing and\nDNA engineering\nexperiments.'),
                habitat= 'rare',
                isLegendary= True
            )

            self.assertDictStructure(expected_response, actual_response)
            self.assertEqual(expected_response['name'], actual_response['name'])
            self.assertEqual(expected_response['description'], actual_response['description'])
            self.assertEqual(expected_response['habitat'], actual_response['habitat'])
            self.assertEqual(expected_response['isLegendary'], actual_response['isLegendary'])


if __name__ == "__main__":
    unittest.main()