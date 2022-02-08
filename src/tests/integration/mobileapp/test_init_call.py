from src.tests.integration.integration_base_test import IntegrationBaseTest


class InitCallTest(IntegrationBaseTest):
    path = "/v1/mobile-app/init"

    def test_init_success(self):
        response = self.app.get(self.path)
        self.assertStatusCode(response, 200)

        actual_response = response.get_json()
        expected_response = dict(
            success=True,
            android=dict(
                latest=0,
                min_allowed=0,
                repeat_push=0
            ),
            ios=dict(
                latest=0,
                min_allowed=0,
                repeat_push=0
            ),
        )
        self.assertDictStructure(expected_response, actual_response)
