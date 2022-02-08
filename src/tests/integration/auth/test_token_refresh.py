from datetime import datetime, timedelta

from flask_babel import _
from freezegun import freeze_time
from werkzeug.exceptions import UnprocessableEntity, Unauthorized, Forbidden

from src.resources import RcTokenRefresh, RcAdminUserSignup
from src.tests.integration.integration_base_test import IntegrationBaseTest


class TokenRefreshTest(IntegrationBaseTest):
    data_sources = ['integration/auth/refresh-users', 'integration/auth/clients']

    login_path = RcTokenRefresh.path
    signup_path = RcAdminUserSignup.path

    @property
    def credentials(self):
        return dict(
            username=self.user_username,
            password='secret'
        )

    @property
    def user_username(self):
        return 'test-refresh@admin.com'

    def setUp(self):
        super().setUp()
        self.refresh_token = create_refresh_token(self.user_username)

    @freeze_time(datetime.utcnow() + timedelta(minutes=2))
    def test_valid_refreshed(self):
        response = self.refresh(self.refresh_token, "1", "1")
        self.assertStatusCode(response, 200)

        actual_response = response.get_json()

        self.assertToken(actual_response, self.user_username, ['access_token', 'expires_in'])

    @freeze_time(datetime.utcnow() + timedelta(minutes=2))
    def test_refreshTwice_refreshed(self):
        self.test_valid_refreshed()
        self.test_valid_refreshed()

    @freeze_time(datetime.utcnow() + timedelta(minutes=2))
    def test_invalid_422verificationFailed(self):
        response = self.refresh(self.refresh_token + '123', "1", "1")
        self.assertStatusCode(response, UnprocessableEntity.code)

        actual_response = response.get_json()
        expected_response = dict(
            msg=_('Signature verification failed')
        )

        self.assertEqual(expected_response, actual_response)

    @freeze_time(datetime.utcnow() + timedelta(minutes=2))
    def test_invalidClientIdAndClientSecret_forbidden(self):
        response = self.refresh(self.refresh_token, 'not-defined-client-id', 'not-defined-client-secret')
        self.assertStatusCode(response, Forbidden.code)

        actual_response = response.get_json()
        expected_response = dict(
            reply=_('You are not an authorized client.'),
            success=False,
        )

        self.assertEqual(expected_response, actual_response)

    @freeze_time(datetime.utcnow() + timedelta(minutes=2))
    def test_invalidClientSecret_forbidden(self):
        response = self.refresh(self.refresh_token, "1", 'not-defined-client-secret')
        self.assertStatusCode(response, Forbidden.code)

        actual_response = response.get_json()
        expected_response = dict(
            reply=_('You are not an authorized client.'),
            success=False,
        )

        self.assertEqual(expected_response, actual_response)

    @freeze_time(datetime.utcnow() + timedelta(minutes=2))
    def test_invalidClientId_forbidden(self):
        response = self.refresh(self.refresh_token, "not-defined-client-id", '1')
        self.assertStatusCode(response, Forbidden.code)

        actual_response = response.get_json()
        expected_response = dict(
            reply=_('You are not an authorized client.'),
            success=False,
        )

        self.assertEqual(expected_response, actual_response)

    @freeze_time(datetime.utcnow() + timedelta(minutes=2))
    def test_passAccessToken_422onlyRefreshTokens(self):
        access_token = create_access_token(self.user_username)
        response = self.refresh(access_token, "1", "1")
        self.assertStatusCode(response, UnprocessableEntity.code)

        actual_response = response.get_json()
        expected_response = dict(
            msg=_('Only refresh tokens are allowed'),
        )

        self.assertEqual(expected_response, actual_response)

    @freeze_time(datetime.utcnow() + timedelta(minutes=2))
    def test_expiredRefreshToken_401(self):
        with freeze_time(datetime.utcnow()) as frozen_time:
            refresh_token = create_refresh_token(self.user_username)

            frozen_time.move_to(datetime.now() + timedelta(weeks=10))

            response = self.refresh(refresh_token, "1", "1")
            self.assertIsNotNone(response)
            self.assertStatusCode(response, Unauthorized.code)

            actual_response = response.get_json()
            expected_response = dict(
                error_code=401,
                error_description="Access token has expired."
            )

            self.assertEqual(actual_response, expected_response)
