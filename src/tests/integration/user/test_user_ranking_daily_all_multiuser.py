from unittest.mock import patch

from freezegun import freeze_time
from src.bootstrap_stages.stage00.logger_setup import logger
from src.tests.integration.integration_base_test import IntegrationBaseTest


class DailyUserRankingAllMultiUserTest(IntegrationBaseTest):
    path = "/v1/user/rankings/daily/all"
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
                {'user_id': '820', 'username': 'Atan20', 'sum_score': 470, 'sum_reps': 320, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 1, 'is_top_player': True},
                {'user_id': '819', 'username': 'Atan19', 'sum_score': 460, 'sum_reps': 310, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 2},
                {'user_id': '818', 'username': 'Atan18', 'sum_score': 450, 'sum_reps': 300, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 3},
                {'user_id': '817', 'username': 'Atan17', 'sum_score': 440, 'sum_reps': 290, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 4},
                {'user_id': '816', 'username': 'Atan16', 'sum_score': 430, 'sum_reps': 280, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 5},
                {'user_id': '815', 'username': 'Atan15', 'sum_score': 420, 'sum_reps': 270, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 6},
                {'user_id': '814', 'username': 'Atan14', 'sum_score': 410, 'sum_reps': 260, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 7},
                {'user_id': '813', 'username': 'Atan13', 'sum_score': 400, 'sum_reps': 250, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 8},
                {'user_id': '812', 'username': 'Atan12', 'sum_score': 390, 'sum_reps': 240, 'sum_minutes': 150, 'is_you': True, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 9},
                {'user_id': '811', 'username': 'Atan11', 'sum_score': 380, 'sum_reps': 230, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 10},
                {'user_id': '810', 'username': 'Atan10', 'sum_score': 370, 'sum_reps': 220, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 11},
                {'user_id': '809', 'username': 'Atan09', 'sum_score': 360, 'sum_reps': 210, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 12},
                {'user_id': '808', 'username': 'Atan08', 'sum_score': 340, 'sum_reps': 190, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 13},
                {'user_id': '807', 'username': 'Atan07', 'sum_score': 330, 'sum_reps': 180, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 14},
                {'user_id': '806', 'username': 'Atan06', 'sum_score': 320, 'sum_reps': 170, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 15},
                {'user_id': '805', 'username': 'Atan05', 'sum_score': 310, 'sum_reps': 160, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 16},
                {'user_id': '804', 'username': 'Atan04', 'sum_score': 300, 'sum_reps': 150, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 17},
                {'user_id': '800', 'username': 'Atan00', 'sum_score': 0, 'sum_reps': 0, 'sum_minutes': 0, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 18},
                {'user_id': '801', 'username': 'Atan01', 'sum_score': 0, 'sum_reps': 0, 'sum_minutes': 0, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 19},
                {'user_id': '803', 'username': 'Atan03', 'sum_score': 0, 'sum_reps': 0, 'sum_minutes': 0, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 20},
                {'user_id': '802', 'username': 'Atan02', 'sum_score': 0, 'sum_reps': 0, 'sum_minutes': 0, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 21}
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
                {'user_id': '820', 'username': 'Atan20', 'sum_score': 470, 'sum_reps': 320, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 1, 'is_top_player': True},
                {'user_id': '819', 'username': 'Atan19', 'sum_score': 460, 'sum_reps': 310, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 2},
                {'user_id': '818', 'username': 'Atan18', 'sum_score': 450, 'sum_reps': 300, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 3},
                {'user_id': '817', 'username': 'Atan17', 'sum_score': 440, 'sum_reps': 290, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 4},
                {'user_id': '816', 'username': 'Atan16', 'sum_score': 430, 'sum_reps': 280, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 5},
                {'user_id': '815', 'username': 'Atan15', 'sum_score': 420, 'sum_reps': 270, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 6},
                {'user_id': '814', 'username': 'Atan14', 'sum_score': 410, 'sum_reps': 260, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 7},
                {'user_id': '813', 'username': 'Atan13', 'sum_score': 400, 'sum_reps': 250, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 8},
                {'user_id': '812', 'username': 'Atan12', 'sum_score': 390, 'sum_reps': 240, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 9},
                {'user_id': '811', 'username': 'Atan11', 'sum_score': 380, 'sum_reps': 230, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 10},
                {'user_id': '810', 'username': 'Atan10', 'sum_score': 370, 'sum_reps': 220, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 11},
                {'user_id': '809', 'username': 'Atan09', 'sum_score': 360, 'sum_reps': 210, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 12},
                {'user_id': '808', 'username': 'Atan08', 'sum_score': 340, 'sum_reps': 190, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 13},
                {'user_id': '807', 'username': 'Atan07', 'sum_score': 330, 'sum_reps': 180, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 14},
                {'user_id': '806', 'username': 'Atan06', 'sum_score': 320, 'sum_reps': 170, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 15},
                {'user_id': '805', 'username': 'Atan05', 'sum_score': 310, 'sum_reps': 160, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 16},
                {'user_id': '804', 'username': 'Atan04', 'sum_score': 300, 'sum_reps': 150, 'sum_minutes': 150, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 17},
                {'user_id': '803', 'username': 'Atan03', 'sum_score': 0, 'sum_reps': 0, 'sum_minutes': 0, 'is_you': True, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 18},
                {'user_id': '800', 'username': 'Atan00', 'sum_score': 0, 'sum_reps': 0, 'sum_minutes': 0, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 19},
                {'user_id': '801', 'username': 'Atan01', 'sum_score': 0, 'sum_reps': 0, 'sum_minutes': 0, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 20},
                {'user_id': '802', 'username': 'Atan02', 'sum_score': 0, 'sum_reps': 0, 'sum_minutes': 0, 'streak': {'streak_days': 0, 'is_streaked_today': False}, 'position': 21}
            ],
            'success': True
        }

        self.assertEqual(expected_response, actual_response)