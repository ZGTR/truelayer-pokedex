import boto3

from src.tests.integration.integration_base_test import IntegrationBaseTest


class ForgotActivationCodeTest(IntegrationBaseTest):
    path = "/v1/user/request/activation-code"

    data_sources = ['integration/user/forgot-activation-users']

    def verify_email_address(self):
        sender = "developers@neurofenix.com"
        conn = boto3.client('ses', region_name='us-east-1')
        conn.verify_email_identity(EmailAddress=sender)

    def test_forgotCode_success(self):
        self.verify_email_address()

        request_body = dict(
            email="user@email.com"
        )

        response = self.app.post(self.path, json=request_body)
        self.assertStatusCode(response, 200)

        actual_response = response.get_json()
        expected_response = dict(
            success=True,
            reply=None,
        )

        self.assertEqual(expected_response, actual_response)

    def test_invalidEmail_400(self):
        request_body = dict(
            email="not-an-email"
        )

        response = self.app.post(self.path, json=request_body)
        self.assertStatusCode(response, 400)

        actual_response = response.get_json()
        expected_response = dict(
            success=False,
            reply="Missing: email: ['Not a valid email address.']"
        )

        self.assertEqual(expected_response, actual_response)
