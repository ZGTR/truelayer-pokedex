from unittest.mock import patch

from src.tests.integration.integration_base_test import IntegrationBaseTest


class AdminUserGroupsTest(IntegrationBaseTest):
    path = "/admin/v1/user-groups"

    data_sources = ['integration/admin/user-groups']

    def test_getAll_success(self):
        response = self.app.get(self.path)

        self.assertStatusCode(response, 200)
        actual_response = response.get_json()
        expected_response = dict(
            success=True,
            items=[
                {
                    'group_type': 'B2C',
                    'id': '1'
                },
                {
                    'group_type': 'NFX_HQ',
                    'id': '2'
                }
            ]
        )

        self.assertEqual(expected_response, actual_response)

    @patch('uuid.uuid1')
    def test_createNewUserGroup_success(self, mock_uuid):
        mock_uuid.return_value.hex = "123456789"
        request_body = dict(
            group_type='B2B'
        )
        response = self.app.post(self.path, json=request_body)

        self.assertStatusCode(response, 200)
        actual_response = response.get_json()
        expected_response = dict(
            success=True,
            item={
                'group_type': 'B2B',
                'id': '123456789'
            }
        )

        self.assertEqual(expected_response, actual_response)

    @patch('uuid.uuid1')
    def test_createExistingGroup_success(self, mock_uuid):
        mock_uuid.return_value.hex = "123456789"
        request_body = dict(
            group_type='B2C'
        )
        response = self.app.post(self.path, json=request_body)

        self.assertStatusCode(response, 400)
        actual_response = response.get_json()
        expected_response = dict(
            success=False,
            reply="A group with same type already exists."
        )

        self.assertEqual(expected_response, actual_response)
