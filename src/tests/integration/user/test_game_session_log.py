from unittest.mock import patch

import boto3

from src.bootstrap_stages.stage02 import GeneralConstants
from src.tests.integration.integration_base_test import IntegrationBaseTest


class GameSessionLogTest(IntegrationBaseTest):
    path = "/v1/user/game-session/log"

    data_sources = ['integration/default-users', 'integration/user/game-session-log/game-sessions']

    def create_bucket(self):
        conn = boto3.resource('s3', region_name='us-east-1')
        conn.create_bucket(Bucket=GeneralConstants.NAME_S3_BUCKET_ASTARTE_GAME_LOG)

    @patch('uuid.uuid1')
    def test_log_success(self, mock_uuid):
        mock_uuid.return_value.hex = '123'
        self.create_bucket()

        request_body = dict(
            game_session_id="123456789",
            raw_data="data"
        )

        response = self.app.post(self.path, headers=self.get_authorization_header("1"), json=request_body)
        self.assertStatusCode(response, 200)

        actual_response = response.get_json()
        expected_response = dict(
            success=True,
            reply=None,
        )

        self.assertEqual(expected_response, actual_response)

    @patch('uuid.uuid1')
    def test_logBucketNotFound_error(self, mock_uuid):
        mock_uuid.return_value.hex = '123'

        request_body = dict(
            game_session_id="123456789",
            raw_data="data"
        )

        response = self.app.post(self.path, headers=self.get_authorization_header("1"), json=request_body)
        self.assertStatusCode(response, 500)

        actual_response = response.get_json()
        expected_response = dict(
            success=False,
            reply="An error happened while trying to make this operation."
        )

        self.assertEqual(expected_response, actual_response)
