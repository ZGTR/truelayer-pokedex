from freezegun import freeze_time

from src.enums.period_aggregator_type import PeriodAggregatorType
from src.services.cloudfront import CloudFront
from src.tests.integration.integration_base_test import IntegrationBaseTest


class TestPhysioWeeklyDashboard(IntegrationBaseTest):
    path = "/v1/physio/dashboard"
    utc_offset_mins_path = "/v1/user/utc_offset_mins"

    data_sources = [
        'integration/default-users',
        'integration/physio/progress-week-current/game-sessions',
        'integration/physio/progress-week-current/streaks',
        'integration/physio/progress-week-current/users'
    ]

    @freeze_time("2021-04-01T10:55:17.561547")
    def test_getWeekStats_withoutAggregator_success(self):
        request_body = dict(
        )

        response = self.app.post(self.path, headers=self.get_authorization_header("1"), json=request_body)
        self.assertStatusCode(response, 200)

        actual_response = response.get_json()
        expected_response = {
            'actions': {
                'current_month': {
                    'href': '/v1/physio/dashboard',
                    'params': {
                        'period_aggregator': '2021-04-01T10:55:17.561547+00:00',
                        'period_type': PeriodAggregatorType.MONTH.value,
                    }
                },
                'prev': {
                    'href': '/v1/physio/dashboard',
                    'params': {
                        'period_aggregator': '2021-03-22T00:00:00+00:00',
                        'period_type': PeriodAggregatorType.WEEK.value,
                    }
                },
            },
            'email': 'user@email.com',
            'selected_state': 'week',
            'selected_period': 'March 29 to April 5 of 2021 (Week 13)',
            'pdf_report_file_name': 'Neurofenix-Progress-Report-1-2021-Week13-(March-29 to April-05).pdf',
            'stats': [
                {
                    'title': "Active Days",
                    'subtitle': "Minutes trained each day",
                    'sections': [
                        {
                            'type': 'active-days',
                            'days': [
                                {
                                    "name": "Mon",
                                    "count": 0,
                                    "unit": "minutes",
                                },
                                {
                                    "name": "Tue",
                                    "count": 0,
                                    "unit": "minutes",
                                },
                                {
                                    "name": "Wed",
                                    "count": 0,
                                    "unit": "minutes",
                                },
                                {
                                    "name": "Thu",
                                    "count": 2,
                                    "unit": "minutes",
                                },
                                {
                                    "name": "Fri",
                                    "count": 0,
                                    "unit": "minutes",
                                },
                                {
                                    "name": "Sat",
                                    "count": 0,
                                    "unit": "minutes",
                                },
                                {
                                    "name": "Sun",
                                    "count": 0,
                                    "unit": "minutes",
                                },
                            ]
                        },
                    ],
                },
                {
                    'title': "Therapy Time",
                    'sections': [
                        {
                            'type': 'metrics',
                            'metrics': [
                                {
                                    'title': "Total Overall",
                                    'text_color': '#28abe2',
                                    "count": 2,
                                    "unit": "minutes",
                                    "is_increased": True,
                                    "percent": "100%",
                                    'subtitle': "2 minutes more than previous period"
                                },
                            ],
                        },
                        {
                            'type': 'metrics',
                            'metrics': [
                                {
                                    'title': "Average daily across the whole period",
                                    'text_color': '#28abe2',
                                    "count": 0.3,
                                    "unit": "minutes",
                                    "is_increased": True,
                                    "percent": "100%",
                                    'subtitle': "0.3 minutes more than previous period"
                                },
                                {
                                    'title': "Average daily across active days only",
                                    'text_color': '#28abe2',
                                    "count": 2,
                                    "unit": "minutes",
                                    "is_increased": True,
                                    "percent": '100%',
                                    'subtitle': "2 minutes more than previous period"
                                },
                                {
                                    'title': "Active days",
                                    "count": 1,
                                    "unit": "active days",
                                    'text_color': '#28abe2',
                                    "is_increased": True,
                                    "percent": '100%',
                                    'subtitle': "1 day more than previous period"
                                },
                            ],
                        }
                    ],
                },
                {
                    'title': "Repetitions",
                    'sections': [
                        {
                            'type': 'metrics',
                            'metrics': [
                                {
                                    'title': "Total Overall",
                                    'text_color': '#28abe2',
                                    "count": 70,
                                    "unit": "reps",
                                    "is_increased": True,
                                    "percent": "100%",
                                    'subtitle': "70 reps more than previous period"
                                },
                            ],
                        },
                        {
                            'type': 'metrics',
                            'metrics': [
                                {
                                    'title': "Forearm Pronation/ Supination",
                                    'image_url': CloudFront.image_url('pronation-supination-colored.png'),
                                    'text_color': '#37b34a',
                                    "count": 123,
                                    "unit": "reps",
                                    "is_increased": True,
                                    "percent": "100%",
                                    'subtitle': "123 reps more than previous period"
                                },
                                {
                                    'title': "Wrist Flexion/Extension",
                                    'image_url': CloudFront.image_url('flexion-extension-colored.png'),
                                    'text_color': '#652d90',
                                    "count": 123,
                                    "unit": "reps",
                                    "is_increased": True,
                                    "percent": "100%",
                                    'subtitle': "123 reps more than previous period"
                                },
                                {
                                    'title': "Grasp and Release",
                                    'image_url': CloudFront.image_url('grip-release-colored.png'),
                                    'text_color': '#f15a24',
                                    "count": 123,
                                    "unit": "reps",
                                    "is_increased": True,
                                    "percent": "100%",
                                    'subtitle': "123 reps more than previous period"
                                },
                            ],
                        },
                    ],
                },
                {
                    'title': 'Repetitions VS Days',
                    'sections': [
                        {
                            'type': 'bar-chart',
                            'data': [
                                {
                                    'name': 'Mon',
                                    'value': 0,
                                },
                                {
                                    'name': 'Tue',
                                    'value': 0,
                                },
                                {
                                    'name': 'Wed',
                                    'value': 0,
                                },
                                {
                                    'name': 'Thu',
                                    'value': 70,
                                },
                                {
                                    'name': 'Fri',
                                    'value': 0,
                                },
                                {
                                    'name': 'Sat',
                                    'value': 0,
                                },
                                {
                                    'name': 'Sun',
                                    'value': 0,
                                },
                            ],
                        },
                    ],
                },
            ],
            'success': True,
        }

        self.assertEqual(expected_response, actual_response)

    @freeze_time("2021-04-01T10:55:17.561547")
    def test_getWeekStats_withWeekAggregator_success(self):
        request_body = dict(
            period_aggregator="2021-04-02T10:55:17.561547"
        )

        response = self.app.post(self.path, headers=self.get_authorization_header("1"), json=request_body)
        self.assertStatusCode(response, 200)

        actual_response = response.get_json()
        expected_response = {
            'actions': {
                'current_month': {
                    'href': '/v1/physio/dashboard',
                    'params': {
                        'period_aggregator': '2021-04-01T10:55:17.561547+00:00',
                        'period_type': PeriodAggregatorType.MONTH.value,
                    }
                },
                'prev': {
                    'href': '/v1/physio/dashboard',
                    'params': {
                        'period_aggregator': '2021-03-22T00:00:00+00:00',
                        'period_type': PeriodAggregatorType.WEEK.value,
                    }
                },
            },
            'email': 'user@email.com',
            'selected_state': 'week',
            'selected_period': "March 29 to April 5 of 2021 (Week 13)",
            'pdf_report_file_name': 'Neurofenix-Progress-Report-1-2021-Week13-(March-29 to April-05).pdf',
            'stats': [
                {
                    'title': "Active Days",
                    'subtitle': "Minutes trained each day",
                    'sections': [
                        {
                            'type': 'active-days',
                            'days': [
                                {
                                    "name": "Mon",
                                    "count": 0,
                                    "unit": "minutes",
                                },
                                {
                                    "name": "Tue",
                                    "count": 0,
                                    "unit": "minutes",
                                },
                                {
                                    "name": "Wed",
                                    "count": 0,
                                    "unit": "minutes",
                                },
                                {
                                    "name": "Thu",
                                    "count": 2,
                                    "unit": "minutes",
                                },
                                {
                                    "name": "Fri",
                                    "count": 0,
                                    "unit": "minutes",
                                },
                                {
                                    "name": "Sat",
                                    "count": 0,
                                    "unit": "minutes",
                                },
                                {
                                    "name": "Sun",
                                    "count": 0,
                                    "unit": "minutes",
                                },
                            ]
                        },
                    ],
                },
                {
                    'title': "Therapy Time",
                    'sections': [
                        {
                            'type': 'metrics',
                            'metrics': [
                                {
                                    'title': "Total Overall",
                                    'text_color': '#28abe2',
                                    "count": 2,
                                    "unit": "minutes",
                                    "is_increased": True,
                                    "percent": "100%",
                                    'subtitle': "2 minutes more than previous period"
                                },
                            ],
                        },
                        {
                            'type': 'metrics',
                            'metrics': [
                                {
                                    'title': "Average daily across the whole period",
                                    'text_color': '#28abe2',
                                    "count": 0.3,
                                    "unit": "minutes",
                                    "is_increased": True,
                                    "percent": "100%",
                                    'subtitle': "0.3 minutes more than previous period"
                                },
                                {
                                    'title': "Average daily across active days only",
                                    'text_color': '#28abe2',
                                    "count": 2,
                                    "unit": "minutes",
                                    "is_increased": True,
                                    "percent": '100%',
                                    'subtitle': "2 minutes more than previous period"
                                },
                                {
                                    'title': "Active days",
                                    "count": 1,
                                    "unit": "active days",
                                    'text_color': '#28abe2',
                                    "is_increased": True,
                                    "percent": '100%',
                                    'subtitle': "1 day more than previous period"
                                },
                            ],
                        },
                    ],
                },
                {
                    'title': "Repetitions",
                    'sections': [
                        {
                            'type': 'metrics',
                            'metrics': [
                                {
                                    'title': "Total Overall",
                                    'text_color': '#28abe2',
                                    "count": 70,
                                    "unit": "reps",
                                    "is_increased": True,
                                    "percent": "100%",
                                    'subtitle': "70 reps more than previous period"
                                },
                            ],
                        },
                        {
                            'type': 'metrics',
                            'metrics': [
                                {
                                    'title': "Forearm Pronation/ Supination",
                                    'image_url': CloudFront.image_url('pronation-supination-colored.png'),
                                    'text_color': '#37b34a',
                                    "count": 123,
                                    "unit": "reps",
                                    "is_increased": True,
                                    "percent": "100%",
                                    'subtitle': "123 reps more than previous period"
                                },
                                {
                                    'title': "Wrist Flexion/Extension",
                                    'image_url': CloudFront.image_url('flexion-extension-colored.png'),
                                    'text_color': '#652d90',
                                    "count": 123,
                                    "unit": "reps",
                                    "is_increased": True,
                                    "percent": "100%",
                                    'subtitle': "123 reps more than previous period"
                                },
                                {
                                    'title': "Grasp and Release",
                                    'image_url': CloudFront.image_url('grip-release-colored.png'),
                                    'text_color': '#f15a24',
                                    "count": 123,
                                    "unit": "reps",
                                    "is_increased": True,
                                    "percent": "100%",
                                    'subtitle': "123 reps more than previous period"
                                },
                            ],
                        },
                    ],
                },
                {
                    'title': 'Repetitions VS Days',
                    'sections': [
                        {
                            'type': 'bar-chart',
                            'data': [
                                {
                                    'name': 'Mon',
                                    'value': 0,
                                },
                                {
                                    'name': 'Tue',
                                    'value': 0,
                                },
                                {
                                    'name': 'Wed',
                                    'value': 0,
                                },
                                {
                                    'name': 'Thu',
                                    'value': 70,
                                },
                                {
                                    'name': 'Fri',
                                    'value': 0,
                                },
                                {
                                    'name': 'Sat',
                                    'value': 0,
                                },
                                {
                                    'name': 'Sun',
                                    'value': 0,
                                },
                            ],
                        },
                    ],
                },
            ],
            'success': True,
        }

        self.assertEqual(expected_response, actual_response)

    @freeze_time("2021-04-01T10:55:17.561547")
    def test_getWeekStats_oldEmptyWeek_success(self):
        request_body = dict(
            period_aggregator="2020-04-01T10:55:17.561547"
        )

        response = self.app.post(self.path, headers=self.get_authorization_header("1"), json=request_body)
        self.assertStatusCode(response, 200)

        actual_response = response.get_json()
        expected_response = {
            'actions': {
                'current_month': {
                    'href': '/v1/physio/dashboard',
                    'params': {
                        'period_aggregator': '2021-04-01T10:55:17.561547+00:00',
                        'period_type': PeriodAggregatorType.MONTH.value,
                    }
                },
                'prev': {
                    'href': '/v1/physio/dashboard',
                    'params': {
                        'period_aggregator': '2020-03-23T00:00:00+00:00',
                        'period_type': PeriodAggregatorType.WEEK.value,
                    }
                },
                'next': {
                    'href': '/v1/physio/dashboard',
                    'params': {
                        'period_aggregator': '2020-04-06T00:00:00+00:00',
                        'period_type': PeriodAggregatorType.WEEK.value,
                    }
                },
            },
            'email': 'user@email.com',
            'selected_state': 'week',
            'selected_period': 'March 30 to April 6 of 2020 (Week 14)',
            'pdf_report_file_name': 'Neurofenix-Progress-Report-1-2020-Week14-(March-30 to April-06).pdf',
            'stats': [
                {
                    'title': "Active Days",
                    'subtitle': "Minutes trained each day",
                    'sections': [
                        {
                            'type': 'active-days',
                            'days': [
                                {
                                    "name": "Mon",
                                    "count": 0,
                                    "unit": "minutes",
                                },
                                {
                                    "name": "Tue",
                                    "count": 0,
                                    "unit": "minutes",
                                },
                                {
                                    "name": "Wed",
                                    "count": 0,
                                    "unit": "minutes",
                                },
                                {
                                    "name": "Thu",
                                    "count": 0,
                                    "unit": "minutes",
                                },
                                {
                                    "name": "Fri",
                                    "count": 0,
                                    "unit": "minutes",
                                },
                                {
                                    "name": "Sat",
                                    "count": 0,
                                    "unit": "minutes",
                                },
                                {
                                    "name": "Sun",
                                    "count": 0,
                                    "unit": "minutes",
                                },
                            ]
                        }
                    ],
                },
                {
                    'title': "Therapy Time",
                    'sections': [
                        {
                            'type': 'metrics',
                            'metrics': [
                                {
                                    'title': "Total Overall",
                                    'text_color': '#28abe2',
                                    "count": 0,
                                    "unit": "minutes",
                                    "is_increased": False,
                                    "percent": "0%",
                                    'subtitle': "Same as previous period",
                                },
                            ]
                        },
                        {
                            'type': 'metrics',
                            'metrics': [
                                {
                                    'title': "Average daily across the whole period",
                                    'text_color': '#28abe2',
                                    "count": 0,
                                    "unit": "minutes",
                                    "is_increased": False,
                                    "percent": "0%",
                                    'subtitle': "Same as previous period",
                                },
                                {
                                    'title': "Average daily across active days only",
                                    'text_color': '#28abe2',
                                    "count": 0,
                                    "unit": "minutes",
                                    "is_increased": False,
                                    "percent": '0%',
                                    'subtitle': "Same as previous period",
                                },
                                {
                                    'title': "Active days",
                                    "count": 0,
                                    "unit": "active days",
                                    'text_color': '#28abe2',
                                    "is_increased": False,
                                    "percent": '0%',
                                    'subtitle': "Same as previous period",
                                },
                            ],
                        },
                    ],
                },
                {
                    'title': "Repetitions",
                    'sections': [
                        {
                            'type': 'metrics',
                            'metrics': [
                                {
                                    'title': "Total Overall",
                                    'text_color': '#28abe2',
                                    "count": 0,
                                    "unit": "reps",
                                    "is_increased": False,
                                    "percent": "0%",
                                    'subtitle': "Same as previous period",
                                },
                            ]
                        },
                        {
                            'type': 'metrics',
                            'metrics': [
                                {
                                    'title': "Forearm Pronation/ Supination",
                                    'image_url': CloudFront.image_url('pronation-supination-colored.png'),
                                    'text_color': '#37b34a',
                                    "count": 0,
                                    "unit": "reps",
                                    "is_increased": False,
                                    "percent": "0%",
                                    'subtitle': "Same as previous period",
                                },
                                {
                                    'title': "Wrist Flexion/Extension",
                                    'image_url': CloudFront.image_url('flexion-extension-colored.png'),
                                    'text_color': '#652d90',
                                    "count": 0,
                                    "unit": "reps",
                                    "is_increased": False,
                                    "percent": "0%",
                                    'subtitle': "Same as previous period",
                                },
                                {
                                    'title': "Grasp and Release",
                                    'image_url': CloudFront.image_url('grip-release-colored.png'),
                                    'text_color': '#f15a24',
                                    "count": 0,
                                    "unit": "reps",
                                    "is_increased": False,
                                    "percent": "0%",
                                    'subtitle': "Same as previous period",
                                },
                            ],
                        },
                    ],
                },
                {
                    'title': 'Repetitions VS Days',
                    'sections': [
                        {
                            'type': 'bar-chart',
                            'data': [
                                {
                                    'name': 'Mon',
                                    'value': 0,
                                },
                                {
                                    'name': 'Tue',
                                    'value': 0,
                                },
                                {
                                    'name': "Wed",
                                    'value': 0,
                                },
                                {
                                    'name': 'Thu',
                                    'value': 0,
                                },
                                {
                                    'name': 'Fri',
                                    'value': 0,
                                },
                                {
                                    'name': 'Sat',
                                    'value': 0,
                                },
                                {
                                    'name': 'Sun',
                                    'value': 0,
                                },
                            ],
                        },
                    ],
                },
            ],
            'success': True,
        }

        self.assertEqual(expected_response, actual_response)

    @freeze_time("2021-04-01T10:55:17.561547")
    def test_getWeekStats_oldEmptyWeek_successWithTimezone(self):

        response = self.app.post(
            self.utc_offset_mins_path,
            headers=self.get_authorization_header("1"),
            json=dict(utc_offset_mins="120")
        )

        self.assertStatusCode(response, 200)

        request_body = dict(
            period_aggregator="2020-04-01T10:55:17.561547"
        )

        response = self.app.post(self.path, headers=self.get_authorization_header("1"), json=request_body)
        self.assertStatusCode(response, 200)

        actual_response = response.get_json()
        expected_response = {
            'actions': {
                'current_month': {
                    'href': '/v1/physio/dashboard',
                    'params': {
                        'period_aggregator': '2021-04-01T12:55:17.561547+02:00',
                        'period_type': PeriodAggregatorType.MONTH.value,
                    }
                },
                'prev': {
                    'href': '/v1/physio/dashboard',
                    'params': {
                        'period_aggregator': '2020-03-23T00:00:00+02:00',
                        'period_type': PeriodAggregatorType.WEEK.value,
                    }
                },
                'next': {
                    'href': '/v1/physio/dashboard',
                    'params': {
                        'period_aggregator': '2020-04-06T00:00:00+02:00',
                        'period_type': PeriodAggregatorType.WEEK.value,
                    }
                },
            },
            'email': 'user@email.com',
            'selected_state': 'week',
            'selected_period': 'March 30 to April 6 of 2020 (Week 14)',
            'pdf_report_file_name': 'Neurofenix-Progress-Report-1-2020-Week14-(March-30 to April-06).pdf',
            'stats': [
                {
                    'title': "Active Days",
                    'subtitle': "Minutes trained each day",
                    'sections': [
                        {
                            'type': 'active-days',
                            'days': [
                                {
                                    "name": "Mon",
                                    "count": 0,
                                    "unit": "minutes",
                                },
                                {
                                    "name": "Tue",
                                    "count": 0,
                                    "unit": "minutes",
                                },
                                {
                                    "name": "Wed",
                                    "count": 0,
                                    "unit": "minutes",
                                },
                                {
                                    "name": "Thu",
                                    "count": 0,
                                    "unit": "minutes",
                                },
                                {
                                    "name": "Fri",
                                    "count": 0,
                                    "unit": "minutes",
                                },
                                {
                                    "name": "Sat",
                                    "count": 0,
                                    "unit": "minutes",
                                },
                                {
                                    "name": "Sun",
                                    "count": 0,
                                    "unit": "minutes",
                                },
                            ]
                        }
                    ],
                },
                {
                    'title': "Therapy Time",
                    'sections': [
                        {
                            'type': 'metrics',
                            'metrics': [
                                {
                                    'title': "Total Overall",
                                    'text_color': '#28abe2',
                                    "count": 0,
                                    "unit": "minutes",
                                    "is_increased": False,
                                    "percent": "0%",
                                    'subtitle': "Same as previous period",
                                },
                            ]
                        },
                        {
                            'type': 'metrics',
                            'metrics': [
                                {
                                    'title': "Average daily across the whole period",
                                    'text_color': '#28abe2',
                                    "count": 0,
                                    "unit": "minutes",
                                    "is_increased": False,
                                    "percent": "0%",
                                    'subtitle': "Same as previous period",
                                },
                                {
                                    'title': "Average daily across active days only",
                                    'text_color': '#28abe2',
                                    "count": 0,
                                    "unit": "minutes",
                                    "is_increased": False,
                                    "percent": '0%',
                                    'subtitle': "Same as previous period",
                                },
                                {
                                    'title': "Active days",
                                    "count": 0,
                                    "unit": "active days",
                                    'text_color': '#28abe2',
                                    "is_increased": False,
                                    "percent": '0%',
                                    'subtitle': "Same as previous period",
                                },
                            ],
                        },
                    ],
                },
                {
                    'title': "Repetitions",
                    'sections': [
                        {
                            'type': 'metrics',
                            'metrics': [
                                {
                                    'title': "Total Overall",
                                    'text_color': '#28abe2',
                                    "count": 0,
                                    "unit": "reps",
                                    "is_increased": False,
                                    "percent": "0%",
                                    'subtitle': "Same as previous period",
                                },
                            ]
                        },
                        {
                            'type': 'metrics',
                            'metrics': [
                                {
                                    'title': "Forearm Pronation/ Supination",
                                    'image_url': CloudFront.image_url('pronation-supination-colored.png'),
                                    'text_color': '#37b34a',
                                    "count": 0,
                                    "unit": "reps",
                                    "is_increased": False,
                                    "percent": "0%",
                                    'subtitle': "Same as previous period",
                                },
                                {
                                    'title': "Wrist Flexion/Extension",
                                    'image_url': CloudFront.image_url('flexion-extension-colored.png'),
                                    'text_color': '#652d90',
                                    "count": 0,
                                    "unit": "reps",
                                    "is_increased": False,
                                    "percent": "0%",
                                    'subtitle': "Same as previous period",
                                },
                                {
                                    'title': "Grasp and Release",
                                    'image_url': CloudFront.image_url('grip-release-colored.png'),
                                    'text_color': '#f15a24',
                                    "count": 0,
                                    "unit": "reps",
                                    "is_increased": False,
                                    "percent": "0%",
                                    'subtitle': "Same as previous period",
                                },
                            ],
                        },
                    ],
                },
                {
                    'title': 'Repetitions VS Days',
                    'sections': [
                        {
                            'type': 'bar-chart',
                            'data': [
                                {
                                    'name': 'Mon',
                                    'value': 0,
                                },
                                {
                                    'name': 'Tue',
                                    'value': 0,
                                },
                                {
                                    'name': "Wed",
                                    'value': 0,
                                },
                                {
                                    'name': 'Thu',
                                    'value': 0,
                                },
                                {
                                    'name': 'Fri',
                                    'value': 0,
                                },
                                {
                                    'name': 'Sat',
                                    'value': 0,
                                },
                                {
                                    'name': 'Sun',
                                    'value': 0,
                                },
                            ],
                        },
                    ],
                },
            ],
            'success': True,
        }

        self.assertEqual(expected_response, actual_response)
