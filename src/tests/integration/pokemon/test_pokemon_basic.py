import unittest

from src.tests.base import IntegrationBaseTest


class TestPokemonBasic(IntegrationBaseTest):

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

        actual_response = response.get_json()

        expected_response = dict(
            message='An error occured while calling the PokeApi.'
        )

        self.assertDictStructure(expected_response, actual_response)


if __name__ == "__main__":
    unittest.main()