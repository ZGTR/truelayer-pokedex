from freezegun import freeze_time

from src.bootstrap_stages.stage00.logger_setup import logger
from src.domain import PlayersRankings
from src.tests.integration.integration_base_test import IntegrationBaseTest


class UserRankingDailyAllTest(IntegrationBaseTest):
    path = "/v1/user/rankings/daily/all"
    utc_offset_mins_path = "/v1/user/utc_offset_mins"

    data_sources = [
        'integration/default-users',
        'integration/user/user_ranking/all/daily_all',
        'integration/user/user_ranking/all/daily_all_users',
        'integration/user/user_ranking/all/daily_all_game_sessions',
        'integration/user/user_ranking/all/daily_all_streaks',
        'integration/user/user_ranking/daily/daily_leaderboard_20190728'
    ]

    @freeze_time("2019-07-28T10:55:17.561547")
    def test_getTodayRanking_lastStreakToday_userFirst(self):
        PlayersRankings().populate_leaderboard_table_from_sessions()

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
                        'streak_days': 10
                    },
                    'sum_minutes': 2,
                    'sum_reps': 123,
                    'sum_score': 0.044444444444444446,
                    'user_id': '1',
                    'username': 'firstname'
                },
                {
                    'position': 2,
                    'streak': {
                        'is_streaked_today': False,
                        'streak_days': 0
                    },
                    'sum_minutes': 0,
                    'sum_reps': 0,
                    'sum_score': 0,
                    'user_id': '2',
                    'username': 'firstname2'
                }
            ],
            'success': True
        }

        self.assertEqual(expected_response, actual_response)


    @freeze_time("2019-07-28T10:55:17.561547")
    def test_getTodayRanking_lastStreakToday_userFirstWithTimeOffset(self):
        PlayersRankings().populate_leaderboard_table_from_sessions()

        # set the utc_offset_mins
        response = self.app.post(
            self.utc_offset_mins_path,
            headers=self.get_authorization_header("1"),
            json=dict(utc_offset_mins="840") # 14 hours ahead of UTC, should pass the threshold of the following day
        )

        self.assertStatusCode(response, 200)

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
                    'position': 2,
                    'streak': {
                        'is_streaked_today': False,
                        'streak_days': 0
                    },
                    'sum_minutes': 0,
                    'sum_reps': 0,
                    'sum_score': 0,
                    'user_id': '2',
                    'username': 'firstname2'
                }
            ],
            'success': True
        }

        self.assertEqual(expected_response, actual_response)

    @freeze_time("2019-07-29T10:55:17.561547")
    def test_getTodayRanking_lastStreakYday_userFirst(self):
        PlayersRankings().populate_leaderboard_table_from_sessions()

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
                        'is_streaked_today': False,
                        'streak_days': 10
                    },
                    'sum_minutes': 0,
                    'sum_reps': 0,
                    'sum_score': 0,
                    'user_id': '1',
                    'username': 'firstname'
                },
                {
                    'position': 2,
                    'streak': {
                        'is_streaked_today': False,
                        'streak_days': 0
                    },
                    'sum_minutes': 0,
                    'sum_reps': 0,
                    'sum_score': 0,
                    'user_id': '2',
                    'username': 'firstname2'
                }
            ],
            'success': True
        }

        self.assertEqual(expected_response, actual_response)

    @freeze_time("2019-07-29T10:55:17.561547")
    def test_getTodayRanking_lastStreakYday_userFirstWithTimeOffset(self):
        PlayersRankings().populate_leaderboard_table_from_sessions()

        # set the utc_offset_mins
        response = self.app.post(
            self.utc_offset_mins_path,
            headers=self.get_authorization_header("1"),
            json=dict(utc_offset_mins="840") # 14 hours ahead of UTC, should pass the threshold of the following day
        )

        self.assertStatusCode(response, 200)

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
                        'is_streaked_today': False,
                        'streak_days': 0
                    },
                    'sum_minutes': 0,
                    'sum_reps': 0,
                    'sum_score': 0,
                    'user_id': '1',
                    'username': 'firstname'
                },
                {
                    'position': 2,
                    'streak': {
                        'is_streaked_today': False,
                        'streak_days': 0
                    },
                    'sum_minutes': 0,
                    'sum_reps': 0,
                    'sum_score': 0,
                    'user_id': '2',
                    'username': 'firstname2'
                }
            ],
            'success': True
        }

        self.assertEqual(expected_response, actual_response)

    @freeze_time("2019-07-30T10:55:17.561547")
    def test_getTodayRanking_lastStreakBeforeYday_userFirst(self):
        PlayersRankings().populate_leaderboard_table_from_sessions()

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
                        'is_streaked_today': False,
                        'streak_days': 0
                    },
                    'sum_minutes': 0,
                    'sum_reps': 0,
                    'sum_score': 0,
                    'user_id': '1',
                    'username': 'firstname'
                },
                {
                    'position': 2,
                    'streak': {
                        'is_streaked_today': False,
                        'streak_days': 0
                    },
                    'sum_minutes': 0,
                    'sum_reps': 0,
                    'sum_score': 0,
                    'user_id': '2',
                    'username': 'firstname2'
                }
            ],
            'success': True
        }

        self.assertEqual(expected_response, actual_response)
