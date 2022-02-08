from src.tests.base import IntegrationBaseTest


class InitCallTest(IntegrationBaseTest):
    path = "/v1/pokemon/"

    def test_default_response(self):
        response = self.app.get(self.path, 'mewtwo')

        self.assertStatusCode(response, 200)

        actual_response = response.get_json()

        expected_response = dict(
            name= '',
            description= '',
            habitat= '',
            isLegendary= ''
        )

        self.assertDictStructure(expected_response, actual_response)
