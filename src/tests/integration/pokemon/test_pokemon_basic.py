import unittest
from unittest import skip
from unittest.mock import patch
import mock
from mock import patch

import requests
from src.services import ClientPokeApi
from src.tests.base import IntegrationBaseTest

def raising_error_grab(an_instance, pokemon_name):
    raise requests.exceptions.ConnectionError

class TestPokemonBasic(IntegrationBaseTest):
    # Since we're dealing with 3rd party API, we can test all sort of timeout issues here Like:
    # 1. def test_request_poke_api_with_a_very_short_timeout_and_fails():
    # 2. def test_request_poke_api_with_a_long_timeout_successfully():
    # 3. def test_request_poke_api_errored():
    # etc.

    def test_exits_pokemon(self):
        # We can use specific resource path instead of hard-coding it here.
        path = "/v1/pokemon/mewtwo"

        response = self.app.get(path)

        self.assertStatusCode(response, 200)

        actual_response = response.get_json()

        expected_response = dict(
            name= 'mewtwo',
            # Since the business requirement is that any description work,
            # we can mock this to make this work regarless of the 3rd party API changing behaviour
            description= 'It was created by\na scientist after\nyears of horrific\fgene splicing and\nDNA engineering\nexperiments.',
            habitat= 'rare',
            isLegendary= True
        )

        self.assertDictStructure(expected_response, actual_response)

    def test_do_not_exist_pokemon(self):
        path = "/v1/pokemon/does-not-exists"

        response = self.app.get(path)

        self.assertStatusCode(response, 500)

        self.assertDictStructure(response.get_json(), dict(
            message='An error occurred while calling pokeapi.co.'
        ))

    # We can a lot of tests mocking part of the workflow and checking the required behaviour after aligning that
    # with the POs.
    def test_problem_with_pokeapi(self):
        # We can use specific resource path instead of hard-coding it here.
        path = "/v1/pokemon/mewtwo"

        with mock.patch.object(ClientPokeApi, 'grab', new=raising_error_grab):
            response = self.app.get(path)

            self.assertStatusCode(response, 500)

            # We should be more concrete in the logic to handle different raised Exceptions.
            self.assertDictStructure(response.get_json(), dict(
                message='An error occurred while calling pokeapi.co.'
            ))


if __name__ == "__main__":
    unittest.main()