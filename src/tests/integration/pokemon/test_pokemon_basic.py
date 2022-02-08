import unittest

from src.tests.base import IntegrationBaseTest


class TestPokemonBasic(IntegrationBaseTest):


    def test_default_response(self):
        path = "/v1/pokemon/mewtwo"

        response = self.app.get(path)

        self.assertStatusCode(response, 200)

        actual_response = response.get_json()
        expected_response = dict(
            name= 'mewtwo',
            description= '',
            habitat= '',
            isLegendary= ''
        )

        self.assertDictStructure(expected_response, actual_response)

if __name__ == "__main__":
    unittest.main()