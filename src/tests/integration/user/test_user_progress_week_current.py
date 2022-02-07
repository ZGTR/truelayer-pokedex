from freezegun import freeze_time

from src.tests.integration.integration_base_test import IntegrationBaseTest


class UserProgressWeekCurrentTest(IntegrationBaseTest):
    path = "/v1/user/progress/week/current"

    data_sources = [
        'integration/default-users',
    ]

    @freeze_time("2019-06-28T10:55:17.561547")
    def test_getWeekStats_success(self):
        response = self.app.get(self.path, headers=self.get_authorization_header("1"))
        self.assertStatusCode(response, 200)

        actual_response = response.get_json()
        expected_response = {
            'actions': {
                'prev_week': {
                    'href': '/v1/user/progress/week',
                    'params': {
                        'week_aggregator': '2019-06-17T00:00:00+00:00'
                    }
                },
                'selected_week': {
                    'href': '/v1/user/progress/week',
                    'params': {
                        'week_aggregator': '2019-06-24T00:00:00+00:00'
                    }
                }
            },
            'stats': {
                'game_sessions_count': 0,
                'minutes': {
                    'progress': {
                        'footnote': '45 minutes is recommended.',
                        'pie': {
                            'pie_max': 1,
                            'pie_min': 0,
                            'progress': 0,
                            'progress_max': 45,
                            'progress_normalized': 0,
                            'subtitle': "/45'",
                            'title': 0
                        },
                        'title': 'My Minutes Played Average/Day'
                    },
                    'stats': {
                        'avg': 0,
                        'sum': 0
                    }
                },
                'reps': {
                    'progress': {
                        'footnote': '300 reps is recommended.',
                        'pie': {
                            'pie_max': 1,
                            'pie_min': 0,
                            'progress': 0,
                            'progress_max': 300,
                            'progress_normalized': 0,
                            'subtitle': '/300 reps',
                            'title': 0
                        },
                        'title': 'My Repetitions Average/Day'
                    },
                    'stats': {
                        'avg': 0,
                        'sum': 0
                    }
                }
            },
            'success': True,
            'top_player': {
                'player': {
                    'is_top_player': True,
                    'is_you': True,
                    'position': 1,
                    'sum_minutes': 0,
                    'sum_reps': 0,
                    'sum_score': 0,
                    'user_id': '1',
                    'username': 'firstname'
                },
                'stats': {
                    'game_sessions_count': 0,
                    'minutes': {
                        'progress': {
                            'footnote': '45 minutes is '
                                        'recommended.',
                            'pie': {
                                'pie_max': 1,
                                'pie_min': 0,
                                'progress': 0,
                                'progress_max': 45,
                                'progress_normalized': 0,
                                'subtitle': "/45'",
                                'title': 0
                            },
                            'title': 'My Minutes Played '
                                     'Average/Day'
                        },
                        'stats': {
                            'avg': 0,
                            'sum': 0
                        }
                    },
                    'reps': {
                        'progress': {
                            'footnote': '300 reps is '
                                        'recommended.',
                            'pie': {
                                'pie_max': 1,
                                'pie_min': 0,
                                'progress': 0,
                                'progress_max': 300,
                                'progress_normalized': 0,
                                'subtitle': '/300 reps',
                                'title': 0
                            },
                            'title': 'My Repetitions '
                                     'Average/Day'
                        },
                        'stats': {
                            'avg': 0,
                            'sum': 0
                        }
                    }
                }
            },
            'user_rankings': {
                'rankings': [
                    {
                        'is_top_player': True,
                        'is_you': True,
                        'position': 1,
                        'sum_minutes': 0,
                        'sum_reps': 0,
                        'sum_score': 0,
                        'user_id': '1',
                        'username': 'firstname'
                    }
                ]
            }
        }

        self.assertEqual(expected_response, actual_response)
