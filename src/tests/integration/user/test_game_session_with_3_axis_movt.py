from unittest.mock import patch

from freezegun import freeze_time

from src.models import DayStreakModel, UserModel
from src.tests.integration.integration_base_test import IntegrationBaseTest


class GameSessionTest(IntegrationBaseTest):
    path = "/v1/user/game-session"
    utc_offset_mins_path = "/v1/user/utc_offset_mins"

    data_sources = ['integration/default-users']

    @patch('uuid.uuid1')
    @freeze_time("2019-06-28T10:55:17.561547")
    def test_createGameSessionNewDay_success(self, mock_uuid):
        uuid_val = '123'
        mock_uuid.return_value.hex = uuid_val

        request_body = dict(
            start_date="2019-06-28T10:55:17.561547",
            end_date="2019-06-28T10:55:17.561547",
            calibration_id="1",
            game_score="1",
            game_score_tag="1",
            game_start_raw_data="data",
            game_end_raw_data="data",
            game_status="Finish",
            game_type="PacMan",
            gameplay_raw_data="1",
            play_time_in_sec="123",
            reps_grsp="1",
            reps_h="20",
            reps_v="25",
            reps_z="10",
            label_h="TiltRight",
            label_v="Flexion",
            label_z="ShoulderFlexion"
        )

        response = self.app.post(self.path, headers=self.get_authorization_header("1"), json=request_body)
        self.assertStatusCode(response, 200)

        actual_response = response.get_json()
        expected_response = dict(
            success=True,
            game_session_log=dict(
                href='/v1/user/game-session/log',
                params=dict(
                    game_session_id=mock_uuid().hex,
                    raw_data=None,
                )
            )
        )

        self.assertEqual(expected_response, actual_response)
        user = UserModel.get("1")

        actual_streak_model = DayStreakModel.get(user.id).as_dict()
        expected_day_streak = dict(
            user_id=user.id,
            last_streak_day="2019-06-28T00:00:00.000000+0000",
            streak_day=1
        )

        self.assertEqual(expected_day_streak, actual_streak_model)

    @patch('uuid.uuid1')
    @freeze_time("2019-06-28T10:55:17.561547")
    def test_createGameSessionNewDay_successWithTimeOffset(self, mock_uuid):
        
        # set the utc_offset_mins
        response = self.app.post(
            self.utc_offset_mins_path,
            headers=self.get_authorization_header("1"),
            json=dict(utc_offset_mins="840") # 14 hours ahead of UTC, should pass the threshold of the following day
        )

        self.assertStatusCode(response, 200)

        uuid_val = '123'
        mock_uuid.return_value.hex = uuid_val

        request_body = dict(
            start_date="2019-06-28T10:55:17.561547",
            end_date="2019-06-28T10:55:17.561547",
            calibration_id="1",
            game_score="1",
            game_score_tag="1",
            game_start_raw_data="data",
            game_end_raw_data="data",
            game_status="Finish",
            game_type="PacMan",
            gameplay_raw_data="1",
            play_time_in_sec="123",
            reps_grsp="1",
            reps_h="20",
            reps_v="25",
            reps_z="10",
            label_h="TiltRight",
            label_v="Flexion",
            label_z="ShoulderFlexion"
        )

        response = self.app.post(self.path, headers=self.get_authorization_header("1"), json=request_body)
        self.assertStatusCode(response, 200)

        actual_response = response.get_json()
        expected_response = dict(
            success=True,
            game_session_log=dict(
                href='/v1/user/game-session/log',
                params=dict(
                    game_session_id=mock_uuid().hex,
                    raw_data=None,
                )
            )
        )

        self.assertEqual(expected_response, actual_response)
        user = UserModel.get("1")

        actual_streak_model = DayStreakModel.get(user.id).as_dict()
        expected_day_streak = dict(
            user_id=user.id,
            last_streak_day="2019-06-29T00:00:00.000000+0000",
            streak_day=1
        )

        self.assertEqual(expected_day_streak, actual_streak_model)
