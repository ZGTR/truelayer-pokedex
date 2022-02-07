from src.models.user import UserModel
from src.tests.integration.integration_base_test import IntegrationBaseTest
from flask_jwt_extended import current_user

class RCUserUtcOffsetMinsTest(IntegrationBaseTest):
    path = "/v1/user/utc_offset_mins"
    data_sources = ['integration/default-users']

    def test_utc_offset_mins_update_success(self):

        response = self.app.post(
            self.path,
            headers=self.get_authorization_header("1"),
            json=dict(utc_offset_mins="60")
        )

        actual_response = response.get_json()
        print(actual_response)
        expected_response = dict(
            success=True,
            reply="Updated user utc_offset_mins"
        )

        # expected data
        expected_user_utc_offset_mins = UserModel.get(hash_key=current_user.id, attributes_to_get=['utc_offset_mins']).utc_offset_mins

        self.assertStatusCode(response, 200)
        self.assertEqual(expected_response, actual_response)
        self.assertEqual(60, expected_user_utc_offset_mins)
