from src.tests.integration.integration_base_test import IntegrationBaseTest


class CalibrationTest(IntegrationBaseTest):
    path = "/admin/v1/calibrations"

    data_sources = ['integration/default-users', 'integration/admin/calibrations']

    def test_allCalibrations_success(self):
        response = self.app.get(self.path, headers=self.get_authorization_header("1"))

        actual_response = response.get_json()
        expected_response = dict(
            success=True,
            items=[
                {
                    'date': '2020-02-27T20:40:31.408229+0000',
                    'id': '1',
                    'nfx_device_name': 'device',
                    'raw_data': '"data"',
                    'user_id': '123'
                }
            ]
        )

        self.assertEqual(expected_response, actual_response)
