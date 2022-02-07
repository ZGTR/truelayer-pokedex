from src.tests.integration.integration_base_test import IntegrationBaseTest


class AdminUsersTest(IntegrationBaseTest):
    path = "/admin/v1/users"

    data_sources = ['integration/admin/users']

    def test_getAllowedUsers_found(self):
        response = self.app.get(self.path)

        self.assertStatusCode(response, 200)
        actual_response = response.get_json()
        expected_response = dict(
            success=True,
            items=[
                {
                    'firstname': 'firstname',
                    'id': '123456789',
                    'lastname': 'lastname',
                    'user_type': 'PatientBasic',
                    'impaired_hand': 'None',
                    'username': 'user',
                    'country': 'uk',
                    'utc_offset_mins': 0
                }
            ]
        )

        self.assertEqual(expected_response, actual_response)

    def test_getUserById_found(self):
        user_id = "123456789"
        response = self.app.get(self.path + '/' + user_id)

        self.assertStatusCode(response, 200)
        actual_response = response.get_json()
        expected_response = dict(
            success=True,
            creation_date='2019-06-28T10:55:17.561547+0000',
            email='user@email.com',
            firstname='firstname',
            impaired_hand='None',
            id='123456789',
            lastname='lastname',
            user_type="PatientBasic",
            username="user",
            country='uk',
            utc_offset_mins=0
        )

        self.assertEqual(expected_response, actual_response)
