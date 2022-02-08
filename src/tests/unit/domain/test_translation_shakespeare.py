import unittest
from unittest import skip
from unittest.mock import patch
import mock
from mock import patch

import requests
from src.services import ClientPokeApi
from src.tests.base import BaseTest


class TestTranslationApiShakespeare(BaseTest):

    def test_happy_scenario(self):
        # # We can use specific resource path instead of hard-coding it here.
        # path = "/v1/pokemon/translated/mewtwo"
        #
        # response = self.app.get(path)
        #
        # self.assertStatusCode(response, 200)
        #
        # actual_response = response.get_json()
        #
        # expected_response = dict(
        #     name= 'mewtwo',
        #     # Since the business requirement is that any description work,
        #     # we can mock this to make this work regarless of the 3rd party API changing behaviour
        #     description= 'It was created by\na scientist after\nyears of horrific\fgene splicing and\nDNA engineering\nexperiments.',
        #     habitat= 'rare',
        #     isLegendary= True
        # )
        #
        # self.assertDictStructure(expected_response, actual_response)


if __name__ == "__main__":
    unittest.main()