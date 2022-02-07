from src.tests.integration.integration_base_test import IntegrationBaseTest


class NfxAstarteGamesTest(IntegrationBaseTest):
    path = "/v1/nfx-astarte-games"

    data_sources = ['integration/default-users', 'integration/user/nfx-astarte-game']

    def test_allGames_success(self):
        response = self.app.get(self.path, headers=self.get_authorization_header("1"))

        actual_response = response.get_json()
        expected_response = dict(
            success=True,
            items=[
                {
                    "game_type": "SimpleTracker",
                    "order": 1,
                    "active": True,
                    # TODO: This should be a string. But this is a temp fix for the current deployment of the client app.
                    "id": 987654321,
                    "title": "Simple Tracker",
                    "subtitle": "A good game",
                    "description": "A good description of the good game",
                    "instruction_video_url": "url.com"
                }
            ]
        )

        self.assertEqual(expected_response, actual_response)
