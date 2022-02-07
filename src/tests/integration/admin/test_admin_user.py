from src.tests.integration.integration_base_test import IntegrationBaseTest


class AdminUserTest(IntegrationBaseTest):
    path = "/admin/v1/user/remove"

    data_sources = ['integration/admin/user']

    def test_deleteUser_foundAndDeleted(self):
        user_id = "123456789"
        request_body = dict(user_id=user_id)
        response = self.app.post(self.path, json=request_body)

        self.assertStatusCode(response, 200)

        response = self.app.post(self.path, json=request_body)
        self.assertStatusCode(response, 400)

        actual_response = response.get_json()
        expected_response = dict(
            reply="We don't have a user with the provided id",
            success=False
        )

        self.assertEqual(expected_response, actual_response)
