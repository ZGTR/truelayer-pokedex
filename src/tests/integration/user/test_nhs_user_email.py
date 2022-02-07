from src.models import NhsUserEmailsModel
from src.tests.integration.integration_base_test import IntegrationBaseTest


class NhsUserEmailTest(IntegrationBaseTest):
    path = "/v1/user/nhs-user-email"

    data_sources = ['integration/default-users']

    def test_addEmail_sent(self):
        email = "user@gmail.com"
        request_body = dict(
            email=email
        )

        response = self.app.post(self.path, headers=self.get_authorization_header("1"), json=request_body)
        self.assertStatusCode(response, 200)

        actual_response = response.get_json()
        expected_response = dict(
            success=True,
            reply="Email sent."
        )

        self.assertEqual(expected_response, actual_response)

        self.assertFalse(NhsUserEmailsModel.get(hash_key=email).user_requested_again)

    def test_addEmailThenRequestAgain_success(self):
        email = "user@gmail.com"
        request_body = dict(
            email=email
        )

        response = self.app.post(self.path, headers=self.get_authorization_header("1"), json=request_body)
        self.assertStatusCode(response, 200)

        actual_response = response.get_json()
        expected_response = dict(
            success=True,
            reply="Email sent."
        )

        self.assertEqual(expected_response, actual_response)

        self.assertFalse(NhsUserEmailsModel.get(hash_key=email).user_requested_again)

        response = self.app.post(self.path, headers=self.get_authorization_header("1"), json=request_body)
        self.assertStatusCode(response, 200)

        actual_response = response.get_json()
        expected_response = dict(
            success=True,
            reply="Email requested again."
        )

        self.assertEqual(expected_response, actual_response)
        self.assertTrue(NhsUserEmailsModel.get(hash_key=email).user_requested_again)
