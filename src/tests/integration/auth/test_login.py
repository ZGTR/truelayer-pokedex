from datetime import datetime, timedelta

from flask_babel import _
from flask_jwt_extended import create_access_token
from freezegun import freeze_time
from hypothesis import given, settings
from hypothesis.strategies import text, characters
from werkzeug.exceptions import BadRequest, Unauthorized

from src.resources import RcUserLogin, RcAdminUserSignup
from src.tests.integration.integration_base_test import IntegrationBaseTest


class LoginTest(IntegrationBaseTest):
    data_sources = ['integration/auth/login-users']

    login_path = RcUserLogin.path
    signup_path = RcAdminUserSignup.path

    @property
    def credentials(self):
        return dict(
            username=self.user_username,
            password='secret'
        )

    @property
    def user_username(self):
        return 'test-login@admin.com'

    @settings(deadline=None)
    @given(
        username=text(min_size=1).filter(lambda x: x.strip()),
        password=text(min_size=10, max_size=20).filter(lambda x: len(x.strip()) > 6)
    )
    def test_invalidEmail_notRegistered(self, username, password):
        response = self.login(dict(username=username, password=password))
        self.assertIsNotNone(response)
        self.assertStatusCode(response, BadRequest.code)

        data = response.get_json()

        invalid_email_msg = _('The Email you\'re trying to login with isn\'t registered'
                              + ' with Neurofenix. Please make sure it\'s typed in correctly.')

        expected_response = dict(
            reply=invalid_email_msg,
            success=False,
        )
        self.assertEqual(expected_response, data)

    @settings(deadline=None)
    @given(password=text(alphabet=characters(blacklist_characters='secret'), min_size=10, max_size=20))
    def test_invalidPassword_incorrectCode(self, password):
        response = self.login(
            dict(
                username='test-login@admin.com',
                password=password
            )
        )
        self.assertIsNotNone(response)
        self.assertStatusCode(response, BadRequest.code)

        data = response.get_json()

        invalid_password_msg = _('Incorrect Activation Code. Please try again.')
        expected_response = dict(
            reply=invalid_password_msg,
            success=False,
        )
        self.assertEqual(data, expected_response)

    def test_missingCredentials_400(self):
        response = self.login(dict(username='', password=''))
        self.assertIsNotNone(response)
        self.assertStatusCode(response, 400)

        actual_json = response.get_json()
        expected_json = dict(
            reply='',
            success=False,
        )

        self.assertDictStructure(actual_json, expected_json)

    @freeze_time(datetime.utcnow())
    @freeze_time(datetime.now())
    def test_valid_loggedIn(self):
        response = self.login(self.credentials)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertKeysIn(['token'], data)

        token = data['token']
        expected_username = 'test-login@admin.com'
        self.assertToken(token, expected_username)

    def test_expiredAccessToken_401(self):
        with freeze_time(datetime.utcnow()) as frozen_time:
            access_token = create_access_token(self.user_username)

            frozen_time.move_to(datetime.now() + timedelta(hours=1))

            response = self.revoke_access_token(access_token)
            self.assertIsNotNone(response)
            self.assertStatusCode(response, Unauthorized.code)

            actual_response = response.get_json()
            expected_response = dict(
                error_description='Access token has expired.',
                error_code=401
            )

            self.assertEqual(expected_response, actual_response)
