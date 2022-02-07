from unittest.mock import patch

from freezegun import freeze_time

from src.tests.integration.integration_base_test import IntegrationBaseTest


class UserProgressWeekTest(IntegrationBaseTest):
    path = "/v1/user/progress/week"

    data_sources = [
        'integration/default-users',
        'integration/user/progress-week-current/streaks',
        'integration/user/progress-week-current/users'
    ]

    @freeze_time("2019-06-28T10:55:17.561547")
    def test_getWeekStats_success(self):
        request_body = dict(
            week_aggregator="2019-06-28T10:55:17.561547"
        )

        response = self.app.post(self.path, headers=self.get_authorization_header("1"), json=request_body)
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
                    },
                    {
                        'position': 2,
                        'sum_minutes': 0,
                        'sum_reps': 0,
                        'sum_score': 0,
                        'user_id': '2',
                        'username': 'firstname2'
                    }
                ]
            }
        }

        self.assertEqual(expected_response, actual_response)

    @freeze_time("2019-07-28T10:55:17.561547")
    def test_getTwoWeeksAgoStats_success(self):
        request_body = dict(
            week_aggregator="2019-06-28T10:55:17.561547"
        )

        response = self.app.post(self.path, headers=self.get_authorization_header("1"), json=request_body)
        self.assertStatusCode(response, 200)

        actual_response = response.get_json()
        expected_response = {
            'actions': {
                'next_week': {
                    'href': '/v1/user/progress/week',
                    'params': {
                        'week_aggregator': '2019-07-01T00:00:00+00:00'
                    }
                },
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
                    },
                    {
                        'position': 2,
                        'sum_minutes': 0,
                        'sum_reps': 0,
                        'sum_score': 0,
                        'user_id': '2',
                        'username': 'firstname2'
                    }
                ]
            }
        }

        self.assertEqual(expected_response, actual_response)

    @patch('uuid.uuid1')
    @freeze_time("2019-06-28T10:55:17.561547")
    def test_getWeekStatsAfterPlayingGameSession_success(self, mock_uuid):
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

        request_body = dict(
            week_aggregator="2019-06-24T10:55:17.561547"
        )
        response = self.app.post(self.path, headers=self.get_authorization_header("1"), json=request_body)
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
                'game_sessions_count': 1,
                'minutes': {
                    'progress': {
                        'footnote': '45 minutes is recommended.',
                        'pie': {
                            'pie_max': 1,
                            'pie_min': 0,
                            'progress': 7,
                            'progress_max': 45,
                            'progress_normalized': 0.15555555555555556,
                            'subtitle': "/45'",
                            'title': 7
                        },
                        'title': 'My Minutes Played Average/Day'
                    },
                    'stats': {
                        'avg': 7,
                        'sum': 45
                    }
                },
                'reps': {
                    'progress': {
                        'footnote': '300 reps is recommended.',
                        'pie': {
                            'pie_max': 1,
                            'pie_min': 0,
                            'progress': 43,
                            'progress_max': 300,
                            'progress_normalized': 0.14333333333333334,
                            'subtitle': '/300 reps',
                            'title': 43
                        },
                        'title': 'My Repetitions Average/Day'
                    },
                    'stats': {
                        'avg': 43,
                        'sum': 300
                    }
                }
            },
            'success': True,
            'top_player': {
                'player': {
                    'is_top_player': True,
                    'is_you': True,
                    'position': 1,
                    'sum_minutes': 7,
                    'sum_reps': 43,
                    'sum_score': 0.29888888888888887,
                    'user_id': '1',
                    'username': 'firstname'
                },
                'stats': {
                    'game_sessions_count': 1,
                    'minutes': {
                        'progress': {
                            'footnote': '45 minutes is recommended.',
                            'pie': {
                                'pie_max': 1,
                                'pie_min': 0,
                                'progress': 7,
                                'progress_max': 45,
                                'progress_normalized': 0.15555555555555556,
                                'subtitle': "/45'",
                                'title': 7
                            },
                            'title': 'My Minutes Played Average/Day'
                        },
                        'stats': {
                            'avg': 7,
                            'sum': 45
                        }
                    },
                    'reps': {
                        'progress': {
                            'footnote': '300 reps is recommended.',
                            'pie': {
                                'pie_max': 1,
                                'pie_min': 0,
                                'progress': 43,
                                'progress_max': 300,
                                'progress_normalized': 0.14333333333333334,
                                'subtitle': '/300 reps',
                                'title': 43
                            },
                            'title': 'My Repetitions Average/Day'
                        },
                        'stats': {
                            'avg': 43,
                            'sum': 300
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
                        'sum_minutes': 7,
                        'sum_reps': 43,
                        'sum_score': 0.29888888888888887,
                        'user_id': '1',
                        'username': 'firstname'
                    },
                    {
                        'position': 2,
                        'sum_minutes': 0,
                        'sum_reps': 0,
                        'sum_score': 0,
                        'user_id': '2',
                        'username': 'firstname2'
                    }
                ]
            }
        }

        self.assertEqual(expected_response, actual_response)
