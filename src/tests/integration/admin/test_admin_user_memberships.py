from src.tests.integration.integration_base_test import IntegrationBaseTest


class AdminUsersMembershipsTest(IntegrationBaseTest):
    path = "/admin/v1/users-memberships"

    data_sources = ['integration/admin/users-memberships']

    def test_getAll_success(self):
        response = self.app.get(self.path)

        self.assertStatusCode(response, 200)
        actual_response = response.get_json()
        expected_response = dict(
            success=True,
            items=[
                {
                    'creation_date': '2019-06-28T10:55:17.561547+0000',
                    'expiry_date': '2019-06-28T10:55:17.561547+0000',
                    'id': '1',
                    'membership_type': 'Basic',
                    'user_id': '123'
                }
            ]
        )

        self.assertEqual(expected_response, actual_response)
