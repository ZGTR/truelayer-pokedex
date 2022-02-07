from unittest.mock import patch
from freezegun import freeze_time

from src.tests.integration.integration_base_test import IntegrationBaseTest


class UserProgressDayCurrentTest(IntegrationBaseTest):
    path = "/v1/user/progress/day/current"
    utc_offset_mins_path = "/v1/user/utc_offset_mins"

    data_sources = [
        'integration/default-users',
        'integration/user/progress-day-current/streaks',
        'integration/user/progress-day-current/targets'
    ]

    @freeze_time("2019-06-28T10:55:17.561547")
    def test_getTodayStats_success(self):
        response = self.app.get(self.path, headers=self.get_authorization_header("1"))
        self.assertStatusCode(response, 200)

        actual_response = response.get_json()
        expected_response = {
            'days_of_week_active': [
                {
                    'active': False,
                    'date': '2019-06-24T00:00:00+00:00',
                    'day_of_week': 0
                },
                {
                    'active': False,
                    'date': '2019-06-25T00:00:00+00:00',
                    'day_of_week': 1
                },
                {
                    'active': False,
                    'date': '2019-06-26T00:00:00+00:00',
                    'day_of_week': 2
                },
                {
                    'active': False,
                    'date': '2019-06-27T00:00:00+00:00',
                    'day_of_week': 3
                },
                {
                    'active': False,
                    'date': '2019-06-28T00:00:00+00:00',
                    'day_of_week': 4
                }
            ],
            'minutes': {
                'play_time_in_sec': 0,
                'progress': {
                    'footnote': '60 minutes is recommended today.',
                    'pie': {
                        'pie_max': 1,
                        'pie_min': 0,
                        'progress': 0,
                        'progress_max': 60,
                        'progress_normalized': 0,
                        'subtitle': "/60' daily",
                        'title': 0
                    },
                    'title': 'My Minutes Played'
                }
            },
            'reps': {
                'progress': {
                    'footnote': '400 reps is recommended today.',
                    'pie': {
                        'pie_max': 1,
                        'pie_min': 0,
                        'progress': 0,
                        'progress_max': 400,
                        'progress_normalized': 0,
                        'subtitle': '/400 reps',
                        'title': 0
                    },
                    'title': 'My Repetitions'
                }
            },
            'streak': {
                'is_streaked_today': False,
                'streak_days': 0
            },
            'success': True
        }

        self.assertEqual(expected_response, actual_response)

    @patch('uuid.uuid1')
    @freeze_time("2019-06-28T10:55:17.561547")
    def test_playGameSessionAndGetStats_updatedStats(self, mock_uuid):
        uuid_val = '123'
        mock_uuid.return_value.hex = uuid_val

        request_body = dict(
            start_date="2019-06-28T10:55:17.561547",
            end_date="2019-06-28T10:55:17.561547",
            calibration_id="1",
            game_score="45",
            game_score_tag="45",
            game_start_raw_data="data",
            game_end_raw_data="data",
            game_status="Finish",
            game_type="PacMan",
            gameplay_raw_data="1",
            play_time_in_sec="2700",
            reps_grsp="1",
            reps_h="45",
            reps_v="20",
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
            'days_of_week_active': [
                {
                    'active': False,
                    'date': '2019-06-24T00:00:00+00:00',
                    'day_of_week': 0
                },
                {
                    'active': False,
                    'date': '2019-06-25T00:00:00+00:00',
                    'day_of_week': 1
                },
                {
                    'active': False,
                    'date': '2019-06-26T00:00:00+00:00',
                    'day_of_week': 2
                },
                {
                    'active': False,
                    'date': '2019-06-27T00:00:00+00:00',
                    'day_of_week': 3
                },
                {
                    'active': True,
                    'date': '2019-06-28T00:00:00+00:00',
                    'day_of_week': 4
                }
            ],
            'minutes': {
                'play_time_in_sec': 45,
                'progress': {
                    'footnote': '60 minutes is recommended today.',
                    'pie': {
                        'pie_max': 1,
                        'pie_min': 0,
                        'progress': 45,
                        'progress_max': 60,
                        'progress_normalized': 1.0,
                        'subtitle': "/60' daily",
                        'title': 45
                    },
                    'title': 'My Minutes Played'
                }
            },
            'reps': {
                'progress': {
                    'footnote': '400 reps is recommended today.',
                    'pie': {
                        'pie_max': 1,
                        'pie_min': 0,
                        'progress': 66,
                        'progress_max': 400,
                        'progress_normalized': 0.22,
                        'subtitle': '/400 reps',
                        'title': 66
                    },
                    'title': 'My Repetitions'
                }
            },
            'streak': {
                'is_streaked_today': True,
                'streak_days': 10
            },
            'success': True
        }

        self.assertEqual(expected_response, actual_response)


    @patch('uuid.uuid1')
    @freeze_time("2019-06-28T10:55:17.561547")
    def test_playGameSessionAndGetStats_updatedStatsWithTimeOffset(self, mock_uuid):

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
            game_score="45",
            game_score_tag="45",
            game_start_raw_data="data",
            game_end_raw_data="data",
            game_status="Finish",
            game_type="PacMan",
            gameplay_raw_data="1",
            play_time_in_sec="2700",
            reps_grsp="1",
            reps_h="45",
            reps_v="20",
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
            'days_of_week_active': [
                {
                    'active': False,
                    'date': '2019-06-24T00:00:00+00:00',
                    'day_of_week': 0
                },
                {
                    'active': False,
                    'date': '2019-06-25T00:00:00+00:00',
                    'day_of_week': 1
                },
                {
                    'active': False,
                    'date': '2019-06-26T00:00:00+00:00',
                    'day_of_week': 2
                },
                {
                    'active': False,
                    'date': '2019-06-27T00:00:00+00:00',
                    'day_of_week': 3
                },
                {
                    'active': True,
                    'date': '2019-06-28T00:00:00+00:00',
                    'day_of_week': 4
                },
                {
                    'active': False,
                    'date': '2019-06-29T00:00:00+00:00',
                    'day_of_week': 5
                }
            ],
            'minutes': {
                'play_time_in_sec': 45,
                'progress': {
                    'footnote': '60 minutes is recommended today.',
                    'pie': {
                        'pie_max': 1,
                        'pie_min': 0,
                        'progress': 45,
                        'progress_max': 60,
                        'progress_normalized': 1.0,
                        'subtitle': "/60' daily",
                        'title': 45
                    },
                    'title': 'My Minutes Played'
                }
            },
            'reps': {
                'progress': {
                    'footnote': '400 reps is recommended today.',
                    'pie': {
                        'pie_max': 1,
                        'pie_min': 0,
                        'progress': 66,
                        'progress_max': 400,
                        'progress_normalized': 0.22,
                        'subtitle': '/400 reps',
                        'title': 66
                    },
                    'title': 'My Repetitions'
                }
            },
            'streak': {
                'is_streaked_today': True,
                'streak_days': 10
            },
            'success': True
        }

        self.assertEqual(expected_response, actual_response)
