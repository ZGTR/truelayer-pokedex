from unittest.mock import patch

from freezegun import freeze_time

from src.models import UserModel, DayStreakModel
from src.tests.integration.integration_base_test import IntegrationBaseTest


class GameSessionTest(IntegrationBaseTest):
    path = "/v1/user/game-session"
    utc_offset_mins_path = "/v1/user/utc_offset_mins"

    data_sources = ['integration/default-users', 'integration/user/game-session/day-streaks']

    dateDay1 = "2019-06-28T10:55:17.561547+0000"
    dateDay2 = "2019-06-29T10:55:17.561547+0000"
    dateDay3 = "2019-06-30T10:55:17.561547+0000"

    @patch('uuid.uuid1')
    @freeze_time(dateDay1)
    def test_createGameSessionWithLastDayStreakToday_updateDayStreak(self, mock_uuid):
        mock_uuid.return_value.hex = '123'

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
            reps_v="35",
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

    @patch('uuid.uuid1')
    @freeze_time(dateDay2)
    def test_createGameSessionWithLastDayStreakYday_updateDayStreak(self, mock_uuid):
        mock_uuid.return_value.hex = '123'

        request_body = dict(
            start_date="2019-06-29T10:55:17.561547",
            end_date="2019-06-29T10:55:17.561547",
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
            reps_v="35",
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
            streak_day=11
        )

        self.assertEqual(expected_day_streak, actual_streak_model)

    @patch('uuid.uuid1')
    @freeze_time(dateDay3)
    def test_createGameSessionWithLastDayStreakYday_resetDayStreak(self, mock_uuid):
        mock_uuid.return_value.hex = '123'

        request_body = dict(
            start_date="2019-06-30T10:55:17.561547",
            end_date="2019-06-30T10:55:17.561547",
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
            reps_v="35",
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
            last_streak_day="2019-06-30T00:00:00.000000+0000",
            streak_day=1
        )

        self.assertEqual(expected_day_streak, actual_streak_model)

    @patch('uuid.uuid1')
    @freeze_time(dateDay3)
    def test_createGameSessionWithLastDayStreakYdayTimeZoneBehind_updateDayStreak(self, mock_uuid):
        # this test runs with a user who is in a timezone 11 hours behind UTC, meaning 
        # they are playing, from a UTC perspective, yesterday (29/06) (the freeze_time() function 
        # freezes the UTC today date at 30/06). This means that their streak from 28/06 can be 
        # continued, where a player in UTC (today: 30/06) could not continue the streak

        mock_uuid.return_value.hex = '123'

        request_body = dict(
            start_date="2019-06-30T10:55:17.561547",
            end_date="2019-06-30T10:55:17.561547",
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
            reps_v="35",
        )

        # set the utc_offset_mins
        self.app.post(
            self.utc_offset_mins_path,
            headers=self.get_authorization_header("1"),
            json=dict(utc_offset_mins="-660") # 11 hours behind UTC, should pass the threshold of the previous day
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
            streak_day=11
        )

        self.assertEqual(expected_day_streak, actual_streak_model)


    @patch('uuid.uuid1')
    @freeze_time(dateDay2)
    def test_createGameSessionWithLastDayStreakYdayTimeZoneAhead_resetDayStreak(self, mock_uuid):
        # this test runs with a user who is in a timezone 14 hours ahead of UTC, meaning 
        # they are playing, from a UTC perspective, tomorrow (30/06). This means that their streak from 
        # 28/06 cannot be continued, where a player in UTC (today: 29/06) could continue the streak

        mock_uuid.return_value.hex = '123'

        request_body = dict(
            start_date="2019-06-30T10:55:17.561547",
            end_date="2019-06-30T10:55:17.561547",
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
            reps_v="35",
        )

        # set the utc_offset_mins
        self.app.post(
            self.utc_offset_mins_path,
            headers=self.get_authorization_header("1"),
            json=dict(utc_offset_mins="840") # 14 hours ahead of UTC, should pass the threshold of the following day
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
            last_streak_day="2019-06-30T00:00:00.000000+0000",
            streak_day=1
        )

        self.assertEqual(expected_day_streak, actual_streak_model)


    @patch('uuid.uuid1')
    @freeze_time(dateDay1)
    def test_createGameSessionWithLastDayStreakYdayTimeZoneAhead_updateDayStreak(self, mock_uuid):
        # this test runs with a user who is in a timezone 14 hours ahead of UTC, meaning 
        # they are playing, from a UTC perspective, tomorrow (29/06). This means that their streak from 
        # 28/06 can be continued and is expected to be incremented by 1 to 11.

        mock_uuid.return_value.hex = '123'

        request_body = dict(
            start_date="2019-06-29T10:55:17.561547",
            end_date="2019-06-29T10:55:17.561547",
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
            reps_v="35",
        )

        # set the utc_offset_mins
        self.app.post(
            self.utc_offset_mins_path,
            headers=self.get_authorization_header("1"),
            json=dict(utc_offset_mins="840") # 14 hours ahead of UTC, should pass the threshold of the following day
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
            streak_day=11
        )

        self.assertEqual(expected_day_streak, actual_streak_model)
