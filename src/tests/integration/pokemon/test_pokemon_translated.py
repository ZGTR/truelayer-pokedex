import unittest
from string import Template
from unittest import skip
from unittest.mock import patch
import mock
from mock import patch

import requests

from src.domain.translation_strategies.pokemon_translation_factory import PokemonTranslationFactory
from src.domain.translation_strategies.pokemon_translation_strategy_standard import PokemonTranslationStrategyStandard
from src.domain.translation_strategies.pokemon_translation_strategy_yoda import PokemonTranslationStrategyYoda
from src.services import ClientPokeApi
from src.tests.base import BaseTest
from src.tests.integration.pokemon.test_pokemon_basic import url_for

TRANSLATED_DESCRIPTION = Template(f'This is the translation of \'$description\'')

def mocked_translate_api_throwing_an_error(an_instance, description):
    raise Exception("An error in translation API.")

def mocked_translate_api(an_instance, description):
    return TRANSLATED_DESCRIPTION.substitute(description=description)

class TestPokemonTranslated(BaseTest):
    # The translation API may have an extremely low limit (5 per hour).
    # Therefore, we'll mock the translation API call responses.

    def test_happy_scenario_end_to_end(self):
        with mock.patch.object(PokemonTranslationStrategyYoda, 'translate', new=mocked_translate_api):
            response = self.app.get(url_for('rcpokemontranslated', pokemon_name='mewtwo'))

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

    def test_error_and_can_not_translate_with_a_strategy(self):
        # In this case, a standard translation should be set. We'll simply mock the
        # translate() call to throw an error to emulate this.
        with mock.patch.object(PokemonTranslationStrategyYoda, 'translate', new=mocked_translate_api_throwing_an_error):
            response = self.app.get(url_for('rcpokemontranslated', pokemon_name='mewtwo'))

            self.assertStatusCode(response, 200)

            actual_response = response.get_json()

            expected_response = dict(
                name= 'mewtwo',
                description= 'It was created by\na scientist after\nyears of horrific\fgene splicing and\nDNA engineering\nexperiments.',
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