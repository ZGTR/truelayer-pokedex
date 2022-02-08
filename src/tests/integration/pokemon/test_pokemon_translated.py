import unittest
from unittest import skip
from unittest.mock import patch
import mock
from mock import patch

import requests
from src.services import ClientPokeApi
from src.tests.base import BaseTest


class TestPokemonTranslated(BaseTest):
    # Same as with tests for PokemonBasicApi:
    # Since we're dealing with 3rd party API, we can test all sort of timeout issues here Like:
    # 1. def test_request_poke_api_with_a_very_short_timeout_and_fails():
    # 2. def test_request_poke_api_with_a_long_timeout_successfully():
    # 3. def test_request_poke_api_errored():
    # etc.

    def test_happy_scenario(self):
        # We can use specific resource path instead of hard-coding it here.
        path = "/v1/pokemon/translated/mewtwo"

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


if __name__ == "__main__":
    unittest.main()