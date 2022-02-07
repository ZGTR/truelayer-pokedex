from unittest.mock import patch
from freezegun import freeze_time

from src.domain import PlayersRankings
from src.tests.integration.integration_base_test import IntegrationBaseTest


class DailyUserRankingTest(IntegrationBaseTest):
    path = "/v1/user/rankings/daily/digest"
    utc_offset_mins_path = "/v1/user/utc_offset_mins"

    data_sources = [
        'integration/default-users',
        'integration/user/user_ranking/daily/daily',
        'integration/user/user_ranking/daily/daily_users',
        'integration/user/user_ranking/daily/daily_streaks',
        'integration/user/user_ranking/daily/daily_game_sessions',
        'integration/user/user_ranking/daily/daily_leaderboard_20190728'
    ]

    @freeze_time("2019-07-28T10:55:17.561547")
    @patch("secrets.randbelow")
    @patch("secrets.choice")
    def test_getTodayRanking_lastStreakToday_userFirst(self, mock_choice, mock_randbelow):
        mock_randbelow.return_value = 1
        mock_choice.return_value = 'Felix.The.Fenix'

        response = self.app.get(self.path, headers=self.get_authorization_header("1"))
        self.assertStatusCode(response, 200)

        actual_response = response.get_json()
        expected_response = {
            'rankings': [
                {
                    'is_you': True,
                    'is_top_player': True,
                    'position': 1,
                    'streak': {
                        'is_streaked_today': True,
                        'streak_days': 10
                    },
                    'sum_minutes': 2,
                    'sum_reps': 123,
                    'sum_score': 0.044444444444444446,
                    'user_id': '1',
                    'username': 'firstname'
                },
                {
                    'is_bot': True,
                    'position': 2,
                    'streak': {
                        'is_streaked_today': True,
                        'streak_days': 1
                    },
                    'sum_minutes': 1,
                    'sum_reps': 1,
                    'sum_score': 0.025555555555555557,
                    'user_id': 'nfx_bot_0',
                    'username': 'Felix.The.Fenix'
                }
            ],
            'success': True
        }

        self.assertEqual(expected_response, actual_response)

    @freeze_time("2019-07-28T10:55:17.561547")
    @patch("secrets.randbelow")
    @patch("secrets.choice")
    def test_getTodayRanking_lastStreakToday_userFirstWithTimeOffset(self, mock_choice, mock_randbelow):
        # set the utc_offset_mins
        response = self.app.post(
            self.utc_offset_mins_path,
            headers=self.get_authorization_header("1"),
            json=dict(utc_offset_mins="840") # 14 hours ahead of UTC, should pass the threshold of the following day
        )

        self.assertStatusCode(response, 200)
        
        mock_randbelow.return_value = 1
        mock_choice.return_value = 'Felix.The.Fenix'

        response = self.app.get(self.path, headers=self.get_authorization_header("1"))
        self.assertStatusCode(response, 200)

        actual_response = response.get_json()
        expected_response = {
            'rankings': [
                {
                    'is_you': True,
                    'is_top_player': True,
                    'position': 1,
                    'streak': {
                        'is_streaked_today': False,
                        'streak_days': 10
                    },
                    'sum_minutes': 2,
                    'sum_reps': 123,
                    'sum_score': 0.044444444444444446,
                    'user_id': '1',
                    'username': 'firstname'
                },
                {
                    'is_bot': True,
                    'position': 2,
                    'streak': {
                        'is_streaked_today': True,
                        'streak_days': 1
                    },
                    'sum_minutes': 1,
                    'sum_reps': 1,
                    'sum_score': 0.025555555555555557,
                    'user_id': 'nfx_bot_0',
                    'username': 'Felix.The.Fenix'
                }
            ],
            'success': True
        }

        self.assertEqual(expected_response, actual_response)

    @freeze_time("2019-07-29T10:55:17.561547")
    @patch("secrets.randbelow")
    @patch("secrets.choice")
    def test_getTodayRanking_lastStreakYday_userFirst(self, mock_choice, mock_randbelow):
        mock_randbelow.return_value = 1
        mock_choice.return_value = 'Felix.The.Fenix'

        response = self.app.get(self.path, headers=self.get_authorization_header("1"))
        self.assertStatusCode(response, 200)

        actual_response = response.get_json()
        expected_response = {
            'rankings': [
                {
                    'is_bot': True,
                    'is_top_player': True,
                    'position': 1,
                    'streak': {
                        'is_streaked_today': True,
                        'streak_days': 1
                    },
                    'sum_minutes': 1,
                    'sum_reps': 1,
                    'sum_score': 0.025555555555555557,
                    'user_id': 'nfx_bot_0',
                    'username': 'Felix.The.Fenix'
                },
                {
                    'is_you': True,
                    'position': 2,
                    'streak': {
                        'is_streaked_today': False,
                        'streak_days': 10
                    },
                    'sum_minutes': 0,
                    'sum_reps': 0,
                    'sum_score': 0,
                    'user_id': '1',
                    'username': 'firstname'
                }
            ],
            'success': True
        }

        self.assertEqual(expected_response, actual_response)

    @freeze_time("2019-07-29T10:55:17.561547")
    @patch("secrets.randbelow")
    @patch("secrets.choice")
    def test_getTodayRanking_lastStreakYday_userFirstWithTimeOffset(self, mock_choice, mock_randbelow):
        # set the utc_offset_mins
        response = self.app.post(
            self.utc_offset_mins_path,
            headers=self.get_authorization_header("1"),
            json=dict(utc_offset_mins="840") # 14 hours ahead of UTC, should pass the threshold of the following day
        )

        self.assertStatusCode(response, 200)

        mock_randbelow.return_value = 1
        mock_choice.return_value = 'Felix.The.Fenix'

        response = self.app.get(self.path, headers=self.get_authorization_header("1"))
        self.assertStatusCode(response, 200)

        actual_response = response.get_json()
        expected_response = {
            'rankings': [
                {
                    'is_bot': True,
                    'is_top_player': True,
                    'position': 1,
                    'streak': {
                        'is_streaked_today': True,
                        'streak_days': 1
                    },
                    'sum_minutes': 1,
                    'sum_reps': 1,
                    'sum_score': 0.025555555555555557,
                    'user_id': 'nfx_bot_0',
                    'username': 'Felix.The.Fenix'
                },
                {
                    'is_you': True,
                    'position': 2,
                    'streak': {
                        'is_streaked_today': False,
                        'streak_days': 0
                    },
                    'sum_minutes': 0,
                    'sum_reps': 0,
                    'sum_score': 0,
                    'user_id': '1',
                    'username': 'firstname'
                }
            ],
            'success': True
        }

        self.assertEqual(expected_response, actual_response)

    @freeze_time("2019-07-30T10:55:17.561547")
    @patch("secrets.randbelow")
    @patch("secrets.choice")
    def test_getTodayRanking_lastStreakBeforeYday_userFirst(self, mock_choice, mock_randbelow):
        mock_randbelow.return_value = 1
        mock_choice.return_value = 'Felix.The.Fenix'

        response = self.app.get(self.path, headers=self.get_authorization_header("1"))
        self.assertStatusCode(response, 200)

        actual_response = response.get_json()
        expected_response = {
            'rankings': [
                {
                    'is_bot': True,
                    'is_top_player': True,
                    'position': 1,
                    'streak': {
                        'is_streaked_today': True,
                        'streak_days': 1
                    },
                    'sum_minutes': 1,
                    'sum_reps': 1,
                    'sum_score': 0.025555555555555557,
                    'user_id': 'nfx_bot_0',
                    'username': 'Felix.The.Fenix'
                },
                {
                    'is_you': True,
                    'position': 2,
                    'streak': {
                        'is_streaked_today': False,
                        'streak_days': 0
                    },
                    'sum_minutes': 0,
                    'sum_reps': 0,
                    'sum_score': 0,
                    'user_id': '1',
                    'username': 'firstname'
                }
            ],
            'success': True
        }

        self.assertEqual(expected_response, actual_response)

    @freeze_time("2019-07-30T10:55:17.561547")
    @patch("secrets.randbelow")
    @patch("secrets.choice")
    @patch('uuid.uuid1')
    def test_getTodayRankingAfterPlayingGameSession_lastStreakBeforeYday_userFirst(self, mock_uuid, mock_choice, mock_randbelow):
        mock_randbelow.return_value = 1
        mock_choice.return_value = 'Felix.The.Fenix'

        uuid_val = '123'
        mock_uuid.return_value.hex = uuid_val

        request_body = dict(
            start_date="2019-07-30T10:55:17.561547",
            end_date="2019-07-30T10:55:19.561547",
            calibration_id="1",
            game_score="45",
            game_score_tag="45",
            game_start_raw_data="data",
            game_end_raw_data="data",
            game_status="Finish",
            game_type="PacMan",
            gameplay_raw_data="1",
            play_time_in_sec="2700",
            reps_grsp="50",
            reps_h="100",
            reps_v="150",
        )

        response = self.app.post('/v1/user/game-session', headers=self.get_authorization_header("1"), json=request_body)
        self.assertStatusCode(response, 200)

        actual_response = response.get_json()
        expected_response = dict(
            success=True,
            game_session_log=dict(
                href='/v1/user/game-session/log',
                params=dict(
                    game_session_id=uuid_val,
                    raw_data=None,
                )
            )
        )

        self.assertEqual(expected_response, actual_response)

        response = self.app.get(self.path, headers=self.get_authorization_header("1"))
        self.assertStatusCode(response, 200)

        actual_response = response.get_json()
        expected_response = {
            'rankings': [
                {
                    'is_top_player': True,
                    'is_you': True,
                    'position': 1,
                    'streak': {
                        'is_streaked_today': True,
                        'streak_days': 1
                    },
                    'sum_minutes': 45,
                    'sum_reps': 300,
                    'sum_score': 2,
                    'user_id': '1',
                    'username': 'firstname'
                },
                {
                    'is_bot': True,
                    'position': 2,
                    'streak': {
                        'is_streaked_today': True,
                        'streak_days': 1
                    },
                    'sum_minutes': 1,
                    'sum_reps': 1,
                    'sum_score': 0.025555555555555557,
                    'user_id': 'nfx_bot_0',
                    'username': 'Felix.The.Fenix'
                }
            ],
            'success': True
        }

        self.assertEqual(expected_response, actual_response)
