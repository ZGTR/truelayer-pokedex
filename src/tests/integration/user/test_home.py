from src.tests.integration.integration_base_test import IntegrationBaseTest


class UserHomeTest(IntegrationBaseTest):
    path = "/v1/user/home"

    data_sources = ['integration/default-users', 'integration/user/home/nfx-astarte-game']

    def test_get_success(self):
        response = self.app.get(self.path, headers=self.get_authorization_header("1"))

        self.assertStatusCode(response, 200)
        actual_response = response.get_json()

        actual_games = actual_response['games']['available_games']

        expected_games = [
            {
                'active': True,
                'game_type': 'SimpleTracker',
                # TODO: This should be a string. But this is a temp fix for the current deployment of the client app.
                'id': 987654321,
                'order': 1,
                "title": "Simple Tracker",
                "subtitle": "A good game",
                "description": "A good description of the good game",
                "instruction_video_url": "url.com"
            }
        ]
        self.assertEqual(expected_games, actual_games)
        self.assertIsNotNone(actual_response['mobile_app_init'])

        actual_actions = actual_response['actions']
        expected_actions_structure = {
            'calibration': {
                'href': '/v1/user/calibration',
                'params': {
                    'nfx_device_name': None,
                    'raw_data': None
                }
            },
            'game_specific_leaderboard': {
                'href': '/v1/user/game-specific-leaderboard',
                'params': {
                    'game_type': None
                }
            },
            'progress_day_current': {
                'href': '/v1/user/progress/day/current'
            },
            'progress_week_current': {
                'href': '/v1/user/progress/week/current'
            },
            'rankings_daily_all': {
                'href': '/v1/user/rankings/daily/all'
            },
            'rankings_daily_digest': {
                'href': '/v1/user/rankings/daily/digest'
            },
            'request_goodie_email': {
                'href': '/v1/user/nhs-user-email',
                'params': {
                    'email': None
                }
            },
            'game_specific_leaderboard': {
                'href': '/v1/user/game-specific-leaderboard',
                'params': {
                    'game_type': None
                }
            }
        }
        self.assertEqual(expected_actions_structure, actual_actions)
