from datetime import datetime
from unittest.mock import patch
from flask_jwt_extended import current_user
from dateutil.tz import tzutc
from freezegun import freeze_time

from src.enums import Country
from src.helpers.date_helper import get_now, get_user_current_datetime
from src.tests.integration.integration_base_test import IntegrationBaseTest


@patch('src.analytics.analytics_segment.analytics')
class UserAnalyticsTest(IntegrationBaseTest):
    path = "/v2/mobile-app/services/log/app-event"
    utc_offset_mins_path = "/v1/user/utc_offset_mins"

    data_sources = [
        'integration/default-users',
        'integration/user/analytics/users',
    ]

    @freeze_time("2019-06-28T10:55:17.561547")
    def test_logEventWithUserId_doesntHaveCountry_success(self, mock_analytics):
        request_body = dict(
            event_name="show-screen",
            user_id="1",
            device_os="Fuchsia"
        )
        response = self.app.post(self.path, json=request_body)

        self.assertStatusCode(response, 200)
        actual_response = response.get_json()
        expected_response = dict(success=True)

        self.assertEqual(expected_response, actual_response)
        self.assertEqual(mock_analytics.identify.call_count, 1)
        self.assertEqual(mock_analytics.track.call_count, 1)
        mock_analytics.track.assert_called_with(
            "1",
            "show-screen",
            dict(**request_body, date=get_now().isoformat())
        )

        expected_identify_data = dict(
            firstname='firstname',
            lastname='lastname',
            email='user@email.com',
            created_at=datetime.now(tz=tzutc()),
            country='us',
        )

        mock_analytics.identify.assert_called_with(
            "1",
            expected_identify_data
        )

    @freeze_time("2019-06-28T10:55:17.561547")
    def test_logEventWithUserId_doesntHaveCountry_successWithTimeOffset(self, mock_analytics):
        
        # set the utc_offset_mins
        response = self.app.post(
            self.utc_offset_mins_path,
            headers=self.get_authorization_header("1"),
            json=dict(utc_offset_mins="840") # 14 hours ahead of UTC, should pass the threshold of the following day
        )

        self.assertStatusCode(response, 200)
        
        request_body = dict(
            event_name="show-screen",
            user_id="1",
            device_os="Fuchsia"
        )
        response = self.app.post(self.path, json=request_body)

        self.assertStatusCode(response, 200)
        actual_response = response.get_json()
        expected_response = dict(success=True)

        self.assertEqual(expected_response, actual_response)
        self.assertEqual(mock_analytics.identify.call_count, 1)
        self.assertEqual(mock_analytics.track.call_count, 1)
        # expected data
        
        users_now = get_user_current_datetime(current_user.id)
        
        mock_analytics.track.assert_called_with(
            "1",
            "show-screen",
            dict(**request_body, date=users_now.isoformat())
        )

        expected_identify_data = dict(
            firstname='firstname',
            lastname='lastname',
            email='user@email.com',
            created_at=datetime.now(tz=tzutc()),
            country='us',
        )

        mock_analytics.identify.assert_called_with(
            "1",
            expected_identify_data
        )

    @freeze_time("2019-06-28T10:55:17.561547")
    def test_logEventWithUserId_withoutCountry_success(self, mock_analytics):
        request_body = dict(
            event_name="show-screen",
            user_id="2",
            device_os="Fuchsia"
        )
        response = self.app.post(self.path, json=request_body)

        self.assertStatusCode(response, 200)
        actual_response = response.get_json()
        expected_response = dict(success=True)

        self.assertEqual(expected_response, actual_response)
        self.assertEqual(mock_analytics.identify.call_count, 1)
        self.assertEqual(mock_analytics.track.call_count, 1)
        mock_analytics.track.assert_called_with(
            "2",
            "show-screen",
            dict(**request_body, date=get_now().isoformat())
        )

        expected_identify_data = dict(
            firstname='firstname-2',
            lastname='lastname-2',
            email='user-2@email.com',
            created_at=datetime.now(tz=tzutc()),
            country=Country.UK.value,
        )

        mock_analytics.identify.assert_called_with(
            "2",
            expected_identify_data
        )

    def test_logEventWithNotFoundUserId_success(self, mock_analytics):
        request_body = dict(
            event_name="show-screen",
            user_id="not-found-id"
        )
        response = self.app.post(self.path, json=request_body)

        self.assertStatusCode(response, 404)
        actual_response = response.get_json()
        expected_response = {
            'error': 404,
            'text': 'Item does not exist'
        }

        self.assertEqual(expected_response, actual_response)

    @freeze_time("2019-06-28T10:55:17.561547")
    def test_logEventWithoutUserId_success(self, mock_analytics):
        request_body = dict(
            event_name="show-screen",
        )
        response = self.app.post(self.path, json=request_body)

        self.assertStatusCode(response, 200)
        actual_response = response.get_json()
        expected_response = dict(
            success=True
        )

        self.assertEqual(expected_response, actual_response)
        self.assertEqual(mock_analytics.identify.call_count, 0)
        self.assertEqual(mock_analytics.track.call_count, 1)
        mock_analytics.track.assert_called_with(
            "unknown-user-id",
            "show-screen",
            dict(**request_body, user_id="unknown-user-id", date=get_now().isoformat())
        )
