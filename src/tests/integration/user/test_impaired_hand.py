from src.tests.integration.integration_base_test import IntegrationBaseTest


class UserImpairedHandTest(IntegrationBaseTest):
    path = "/v1/user/impaired-hand"

    data_sources = ['integration/default-users']

    def test_setImpairedHand_doneSuccessfully(self):
        request_body = dict(impaired_hand="Right")
        response = self.app.post(self.path, json=request_body, headers=self.get_authorization_header("1"))

        self.assertStatusCode(response, 200)

        actual_response = response.get_json()
        expected_response = dict(
            success=True,
            impaired_hand="Right"
        )

        self.assertEqual(expected_response, actual_response)
