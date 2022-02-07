from unittest.mock import patch

from freezegun import freeze_time
from src.bootstrap_stages.stage00.logger_setup import logger
from src.tests.integration.integration_base_test import IntegrationBaseTest


class DailyUserRankingMultiUserTest(IntegrationBaseTest):
    path = "/v1/user/rankings/daily/digest"
    utc_offset_mins_path = "/v1/user/utc_offset_mins"

    data_sources = [
        'integration/user/progress-day-current/day_leaderboard_users',
        'integration/user/progress-day-current/day_game_sessions',
        'integration/user/progress-day-current/day_leaderboard_leaderboard',
        'integration/user/progress-day-current/day_streaks'
    ]

    @freeze_time("2021-10-28T04:10:00.000001")
    def test_getTodayRankingMultiUser12(self):
        header = self.get_authorization_header("AtanDredandoz")
        response = self.app.get(self.path, headers=header)
        self.assertStatusCode(response, 200)

        actual_response = response.get_json()

        expected_response = {
            'rankings': [
                {
                    'user_id': '820',
                    'username': 'Atan20',
                    'sum_score': 470,
                    'sum_reps': 320,
                    'sum_minutes': 150,
                    'streak': {'streak_days': 0, 'is_streaked_today': False},
                    'position': 1,
                    'is_top_player': True
                }, {
                    'user_id': '812',
                    'username': 'Atan12',
                    'sum_score': 390,
                    'sum_reps': 240,
                    'sum_minutes': 150,
                    'is_you': True,
                    'streak': {'streak_days': 0, 'is_streaked_today': False},
                    'position': 9
                }, {
                    'user_id': '811',
                    'username': 'Atan11',
                    'sum_score': 380,
                    'sum_reps': 230,
                    'sum_minutes': 150,
                    'streak': {'streak_days': 0, 'is_streaked_today': False},
                    'position': 10
                }, {
                    'user_id': '810',
                    'username': 'Atan10',
                    'sum_score': 370,
                    'sum_reps': 220,
                    'sum_minutes': 150,
                    'streak': {'streak_days': 0, 'is_streaked_today': False},
                    'position': 11
                }
            ],
            'success': True
        }

        self.assertEqual(expected_response, actual_response)

    @freeze_time("2021-10-28T04:10:00.000001")
    @patch("secrets.randbelow")
    @patch("secrets.choice")
    def test_getTodayRankingMultiUser03HasBots(self, mock_choice, mock_randbelow):

        mock_randbelow.return_value = 1
        mock_choice.return_value = 'Felix.The.Fenix'

        header = self.get_authorization_header("AtanDredantree")
        response = self.app.get(self.path, headers=header)
        self.assertStatusCode(response, 200)

        actual_response = response.get_json()

        expected_response = {
            'rankings': [
                {
                    'user_id': '820',
                    'username': 'Atan20',
                    'sum_score': 470,
                    'sum_reps': 320,
                    'sum_minutes': 150,
                    'streak': {'streak_days': 0, 'is_streaked_today': False},
                    'position': 1,
                    'is_top_player': True
                }, {
                    'is_bot': True,
                    'user_id': 'nfx_bot_0',
                    'username': 'Felix.The.Fenix',
                    'sum_score': 0.025555555555555557,
                    'sum_reps': 1,
                    'sum_minutes': 1,
                    'streak': {'streak_days': 1, 'is_streaked_today': True},
                    'position': 2
                }, {
                    'is_bot': True,
                    'user_id': 'nfx_bot_1',
                    'username': 'Felix.The.Fenix',
                    'sum_score': 0.025555555555555557,
                    'sum_reps': 1,
                    'sum_minutes': 1,
                    'streak': {'streak_days': 1, 'is_streaked_today': True},
                    'position': 3
                }, {
                    'user_id': '803',
                    'username': 'Atan03',
                    'sum_score': 0,
                    'sum_reps': 0,
                    'sum_minutes': 0,
                    'is_you': True,
                    'streak': {'streak_days': 0, 'is_streaked_today': False},
                    'position': 18
                }
            ],
            'success': True
        }

        self.assertEqual(expected_response, actual_response)