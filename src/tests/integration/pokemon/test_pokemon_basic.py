import unittest
from unittest import skip
from unittest.mock import patch
import mock
from mock import patch
from flask import url_for
import requests
from src.services import ClientPokeApi
from src.tests.base import BaseTest

def raising_error_grab(an_instance, pokemon_name):
    raise requests.exceptions.ConnectionError


class TestPokemonBasic(BaseTest):
    # The PokeAPI may have a limiter and then we should either use a test account with a larger limit
    # Or mock the API call responses same as we did in PokemonTranslated test.

    # Since we're dealing with 3rd party API, we can test all sort of timeout issues here Like:
    # 1. def test_request_poke_api_with_a_very_short_timeout_and_fails():
    # 2. def test_request_poke_api_with_a_long_timeout_successfully():
    # 3. def test_request_poke_api_errored():
    # etc.


    def test_happy_scenario_end_to_end(self):
        response = self.app.get(url_for('rcpokemonbasic', pokemon_name='mewtwo'))

        self.assertStatusCode(response, 200)

        actual_response = response.get_json()

        expected_response = dict(
            v=1,
            name= 'mewtwo',
            # Since the business requirement is that any description work,
            # we can mock this to make this work regarless of the 3rd party API changing behaviour
            description= 'It was created by\na scientist after\nyears of horrific\fgene splicing and\nDNA engineering\nexperiments.',
            habitat= 'rare',
            isLegendary= True
        )

        self.assertDictStructure(expected_response, actual_response)
        self.assertEqual(expected_response['name'], actual_response['name'])
        self.assertEqual(expected_response['description'], actual_response['description'])
        self.assertEqual(expected_response['habitat'], actual_response['habitat'])
        self.assertEqual(expected_response['isLegendary'], actual_response['isLegendary'])

    def test_do_not_exist_pokemon(self):
        response = self.app.get(url_for('rcpokemonbasic', pokemon_name='does-not-exists'))
        self.assertStatusCode(response, 500)
        self.assertDictStructure(response.get_json(), dict(
            message='An error occurred while calling pokeapi.co.'
        ))

    # We can add a lot of tests mocking part of the workflow and checking the required behaviour after aligning that
    # with the POs.
    def test_problem_with_pokeapi(self):
        with mock.patch.object(ClientPokeApi, 'grab', new=raising_error_grab):
            response = self.app.get(url_for('rcpokemonbasic', pokemon_name='mewtwo'))
            self.assertStatusCode(response, 500)
            # We should be more concrete in the logic to handle different raised Exceptions.
            self.assertDictStructure(response.get_json(), dict(
                message='An error occurred while calling pokeapi.co.'
            ))


if __name__ == "__main__":
    unittest.main()