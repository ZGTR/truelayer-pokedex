# from freezegun import freeze_time
#
# from src.enums.period_aggregator_type import PeriodAggregatorType
# from src.services.cloudfront import CloudFront
# from src.tests.integration.integration_base_test import IntegrationBaseTest
#
#
# class TestPhysioMonthlyDashboardGameSession1000(IntegrationBaseTest):
#     path = "/v1/physio/dashboard"
#
#     data_sources = [
#         'integration/default-users',
#         'integration/physio/progress-month-max-seconds-game-session/game-sessions',
#         'integration/physio/progress-month-max-seconds-game-session/streaks',
#         'integration/physio/progress-month-max-seconds-game-session/users'
#     ]
#
#     expected_response_for_current_month = {
#             'actions': {
#                 'current_week': {
#                     'href': '/v1/physio/dashboard',
#                     'params': {
#                         'period_type': PeriodAggregatorType.WEEK.value,
#                         'period_aggregator': '2021-04-01T10:55:17.561547'
#                     }
#                 },
#                 'prev': {
#                     'href': '/v1/physio/dashboard',
#                     'params': {
#                         'period_type': PeriodAggregatorType.MONTH.value,
#                         'period_aggregator': '2021-03-01T10:55:17.561547+00:00'
#                     }
#                 },
#             },
#             'email': 'user@email.com',
#             'selected_state': 'month',
#             'selected_period': 'April 1 of 2021',
#             'pdf_report_file_name': 'Neurofenix-Progress-Report-1-2021-April-01.pdf',
#             'stats': [
#                 {
#                     'title': "Therapy Time",
#                     'sections': [
#                         {
#                             'type': 'metrics',
#                             'metrics': [
#                                 {
#                                     'title': "Total Overall",
#                                     'text_color': '#28abe2',
#                                     "count": 48,
#                                     "unit": "minutes",
#                                     "is_increased": True,
#                                     "percent": "100%",
#                                     'subtitle': "19 minute more than previous period"
#                                 },
#                             ],
#                         },
#                         {
#                             'type': 'metrics',
#                             'metrics': [
#                                 {
#                                     'title': "Average daily across the whole period",
#                                     'text_color': '#28abe2',
#                                     "count": 1.6,
#                                     "unit": "minutes",
#                                     "is_increased": True,
#                                     "percent": "100%",
#                                     'subtitle': "0.6 minutes more than previous period"
#                                 },
#                                 {
#                                     'title': "Average daily across active days only",
#                                     'text_color': '#28abe2',
#                                     "count": 48,
#                                     "unit": "minutes",
#                                     "is_increased": True,
#                                     "percent": '100%',
#                                     'subtitle': "1 minute more than previous period"
#                                 },
#                                 {
#                                     'title': "Active days",
#                                     "count": 1,
#                                     "unit": "active days",
#                                     'text_color': '#28abe2',
#                                     "is_increased": False,
#                                     "percent": '0%',
#                                     'subtitle': "Same as previous period"
#                                 },
#                             ],
#                         },
#                     ],
#                 },
#                 {
#                     'title': "Repetitions",
#                     'sections': [
#                         {
#                             'type': 'metrics',
#                             'metrics': [
#                                 {
#                                     'title': "Total Overall",
#                                     'text_color': '#28abe2',
#                                     "count": 1000,
#                                     "unit": "reps",
#                                     "is_increased": True,
#                                     "percent": "100%",
#                                     'subtitle': "500 reps more than previous period"
#                                 },
#                             ],
#                         },
#                         {
#                             'type': 'metrics',
#                             'metrics': [
#                                 {
#                                     'title': "Forearm Pronation/ Supination",
#                                     'image_url': CloudFront.image_url('pronation-supination-colored.png'),
#                                     'text_color': '#37b34a',
#                                     "count": 400,
#                                     "unit": "reps",
#                                     "is_increased": True,
#                                     "percent": "100%",
#                                     'subtitle': "200 reps more than previous period"
#                                 },
#                                 {
#                                     'title': "Wrist Flexion/Extension",
#                                     'image_url': CloudFront.image_url('flexion-extension-colored.png'),
#                                     'text_color': '#652d90',
#                                     "count": 400,
#                                     "unit": "reps",
#                                     "is_increased": True,
#                                     "percent": "100%",
#                                     'subtitle': "200 reps more than previous period"
#                                 },
#                                 {
#                                     'title': "Grasp and Release",
#                                     'image_url': CloudFront.image_url('grip-release-colored.png'),
#                                     'text_color': '#f15a24',
#                                     "count": 200,
#                                     "unit": "reps",
#                                     "is_increased": True,
#                                     "percent": "100%",
#                                     'subtitle': "100 reps more than previous period"
#                                 },
#                             ],
#                         },
#                     ],
#                 },
#                 {
#                     'title': 'Repetitions VS Days',
#                     'sections': [
#                         {
#                             'type': 'bar-chart',
#                             'data': [
#                                 {
#                                     'name': '1',
#                                     'value': 1000,
#                                 },
#                                 *[
#                                     {
#                                         'name': f"{i}",
#                                         'value': 0,
#                                     } for i in range(2, 30)
#                                 ],
#                             ],
#                         },
#                     ],
#                 },
#             ],
#             'success': True,
#         }
#
#     @freeze_time("2021-04-01T10:55:17.561547")
#     def test_getMonthStats_withMonthAggregator_success(self):
#         request_body = dict(
#             period_type=PeriodAggregatorType.MONTH.value,
#             period_aggregator="2021-04-01T10:55:17.561547"
#         )
#
#         response = self.app.post(self.path, headers=self.get_authorization_header("1"), json=request_body)
#         self.assertStatusCode(response, 200)
#
#         actual_response = response.get_json()
#         expected_response = self.expected_response_for_current_month
#
#         self.assertEqual(expected_response, actual_response)
