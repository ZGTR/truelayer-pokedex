from src.tests.integration.integration_base_test import IntegrationBaseTest


class AdminGameSessionsTest(IntegrationBaseTest):
    path = "/admin/v1/game-sessions"

    data_sources = ['integration/admin/game-sessions']

    # def test_allGameSessions_success(self):
    def allGameSessions_success(self):
        response = self.app.get(self.path)

        actual_response = response.get_json()
        expected_response = dict(
            success=True,
            items=[
                {
                    'calibration_id': '1',
                    'end_date': '2019-06-28T10:55:17.561547+0000',
                    'game_end_raw_data': '""',
                    'game_score': '1223',
                    'game_score_tag': '123',
                    'game_start_raw_data': '""',
                    'game_status': 'Finish',
                    'game_type': 'PacMan',
                    'gameplay_raw_data': '""',
                    'id': '123456789',
                    'log_file_name': 'file_name.json',
                    'play_time_in_sec': '123',
                    'reps_grsp': '123',
                    'reps_h': '123',
                    'reps_overall': 0,
                    'reps_v': '123',
                    'start_date': '2019-06-28T10:55:17.561547+0000',
                    'user_id': '123'
                }
            ]
        )

        self.assertEqual(expected_response, actual_response)
