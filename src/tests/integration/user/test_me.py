from src.enums import Country
from src.tests.integration.integration_base_test import IntegrationBaseTest


class UserMeTest(IntegrationBaseTest):
    path = "/v1/user/me"

    data_sources = ['integration/default-users']

    def test_get_success(self):
        response = self.app.get(self.path, headers=self.get_authorization_header("1"))

        self.assertStatusCode(response, 200)

        actual_response = response.get_json()
        expected_response = {
            'actions': {
                'home': {
                    'href': '/v1/user/home'
                },
                'impaired_hand_set': {
                    'href': '/v1/user/impaired-hand',
                    'params': {
                        'impaired_hand': ''
                    }
                },
                'privacy_policy': {
                    'href': '/v2/mobile-app/privacy-policy'
                },
                "utc_offset_mins":
                {
                    'href': '/v1/user/utc_offset_mins',
                    'params':
                        {
                            'utc_offset_mins': ''
                        }
                }
            },
            'success': True,
            'user': {
                'id': '1',
                'creation_date': '2019-06-28T10:55:17.561547+0000',
                'last_login': '2019-06-29T10:55:17.561547+0000',
                'email': 'user@email.com',
                'firstname': 'firstname',
                'impaired_hand': 'None',
                'lastname': 'lastname',
                'user_type': 'PatientBasic',
                'username': '1',
                'country': Country.UK.value,
                'utc_offset_mins': 0
            }
        }
        self.assertEqual(expected_response, actual_response)
