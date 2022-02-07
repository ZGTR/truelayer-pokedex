from unittest.mock import patch

from src.models import CalibrationModel
from src.tests.integration.integration_base_test import IntegrationBaseTest


class CalibrationTest(IntegrationBaseTest):
    path = "/v1/user/calibration"

    data_sources = ['integration/default-users']

    @patch('uuid.uuid1')
    def test_allCalibrations_success(self, mock_uuid):
        id = '123'
        mock_uuid.return_value.hex = id
 
        request_body = dict(
            nfx_device_name="device",
            raw_data="raw data"
        )

        response = self.app.post(self.path, headers=self.get_authorization_header("1"), json=request_body)
        self.assertStatusCode(response, 200)

        actual_response = response.get_json()
        expected_response = dict(
            success=True,
            game_session=dict(
                href='/v1/user/game-session',
                params=dict(
                    calibration_id=id,
                    start_date=None,
                    end_date=None,
                    play_time_in_sec=None,
                    reps_grsp=None,
                    reps_h=None,
                    reps_v=None,
                    game_type=None,
                    game_score=None,
                    game_score_tag=None,
                    game_status=None,
                    gameplay_raw_data=None,
                    game_start_raw_data=None,
                    game_end_raw_data=None,
                )
            )
        )

        self.assertEqual(expected_response, actual_response)

        calibration = CalibrationModel.get(hash_key=id)
        self.assertIsNotNone(calibration)
        self.assertEqual(calibration.user_id, "1")
