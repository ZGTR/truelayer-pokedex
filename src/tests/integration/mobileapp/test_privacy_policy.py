from src.tests.integration.integration_base_test import IntegrationBaseTest


class PrivacyPolicyTest(IntegrationBaseTest):
    path = "/v2/mobile-app/privacy-policy"

    data_sources = ['integration/mobileapp/users']

    def test_privacyPolicy_success(self):
        response = self.app.get(self.path, headers=self.get_authorization_header('user'))
        self.assertStatusCode(response, 200)

        actual_response = response.get_json()

        expected_response = dict(
            v=1,
            text='',
            success=True,
        )
        self.assertDictStructure(expected_response, actual_response)
