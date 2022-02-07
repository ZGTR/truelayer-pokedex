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
        'integration/user/user_ranking/daily/daily_leaderboard_20190628'
    ]

    @freeze_time("2019-06-28T10:55:17.561547")
    @patch("secrets.randbelow")
    @patch("secrets.choice")
    def test_getTodayRanking_noStreaks_botFirst(self, mock_choice, mock_randbelow):
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
