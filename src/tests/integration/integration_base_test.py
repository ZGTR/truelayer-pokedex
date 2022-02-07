from datetime import datetime, timedelta

from src.models.user import UserModel
from src.resources import RcUserLogin, RcUserLogoutAccess, RcTokenRefresh
from src.tests.base_test import BaseTest


class IntegrationBaseTest(BaseTest):
    login_path = RcUserLogin.path
    logout_access_path = RcUserLogoutAccess.path
    refresh_path = RcTokenRefresh.path

    def assertStatusCode(self, response, status_code):
        self.assertEqual(status_code, response.status_code)

    @classmethod
    def get_authorization_header(cls, username):
        return dict(Authorization='Bearer ' + create_access_token(username))

    def revoke_access_token(self, token):
        headers = dict(
            Authorization='Bearer ' + token
        )

        response = self.app.post(self.logout_access_path, headers=headers)
        self.assertIsNotNone(response)

        return response

    def refresh(self, token, client_id, client_secret):
        headers = dict(
            Authorization='Bearer ' + token
        )

        response = self.app.post(
            self.refresh_path,
            headers=headers,
            json=dict(client_id=client_id, client_secret=client_secret)
        )
        self.assertIsNotNone(response)

        return response

    def assertUserSignedUp(self, data, user):
        self.assertIsNotNone(data)

        expected_response = dict(
            username=user['username'],
            firstname=user['firstname'],
            lastname=user['lastname'],
            user_type="PatientBasic",
            password=user['password'],
            email=user['email'],
            country=user.get('country', None),
            id=Utils.get_random_id(),
            creation_date=Utils.date_to_str(datetime.now()),
            impaired_hand='None',
            success=True,
            utc_offset_mins=0
        )

        self.assertEqual(data, expected_response)

        self.assertNotIn('last_login', data)
        self.assertIsNone(UserModel.get(data['id']).last_login)

    def assertAccessToken(self, expected_username, token):
        decoded_token = decode_token(token)
        self.assertKeysIn(['iat', 'nbf', 'jti', 'exp', 'identity', 'user_claims'], decoded_token)

        actual_token_data = dict(
            identity=decoded_token['identity'],
            user_claims=decoded_token['user_claims'],
            type=decoded_token['type'],
            exp=Utils.date_to_str(datetime.utcfromtimestamp(decoded_token['exp']))
        )

        expected_token_data = dict(
            identity=expected_username,
            user_claims=dict(),
            type='access',
            exp=Utils.date_to_str((datetime.utcnow() + timedelta(seconds=15)).replace(microsecond=0))
        )

        self.assertEqual(expected_token_data, actual_token_data)

    def assertRefreshToken(self, expected_username, token):
        decoded_token = decode_token(token)
        self.assertKeysIn(['iat', 'nbf', 'jti', 'exp', 'identity', 'user_claims'], decoded_token)

        actual_token_data = dict(
            identity=decoded_token['identity'],
            user_claims=decoded_token['user_claims'],
            type=decoded_token['type'],
            exp=Utils.date_to_str(datetime.utcfromtimestamp(decoded_token['exp']))
        )

        expected_token_data = dict(
            identity=expected_username,
            user_claims=dict(),
            type='refresh',
            exp=Utils.date_to_str((datetime.utcnow() + timedelta(days=30)).replace(microsecond=0))
        )

        self.assertEqual(actual_token_data, expected_token_data)

    def assertToken(self, token, expected_username, names=None):
        available_options = ['access_token', 'refresh_token', 'expires_in']

        if names is None:
            names = available_options

        # assert parameters
        intersected = list(set(available_options) & set(names))
        self.assertGreater(len(intersected), 0, 'Invalid parameter: names')
        union = set(set(available_options) | set(names))
        self.assertEqual(len(union), len(available_options), 'Invalid parameter: names')

        executed_count = 0
        name = 'access_token'
        if name in names:
            executed_count += 1
            self.assertIn(name, token)
            access_token = token[name]
            self.assertAccessToken(expected_username, access_token)

        name = 'refresh_token'
        if name in names:
            executed_count += 1
            self.assertIn(name, token)
            refresh_token = token[name]
            self.assertRefreshToken(expected_username, refresh_token)

        name = 'expires_in'
        if name in names:
            executed_count += 1
            self.assertExpiresIn(token)

        # assert the count of the executed if branches
        self.assertEqual(executed_count, len(names), 'Invalid parameter: names')

    def assertExpiresIn(self, token):
        self.assertIn('expires_in', token)
        expires_in = token['expires_in']
        self.assertEqual(expires_in, timedelta(seconds=15).total_seconds())

    def login(self, data):
        response = self.app.post(self.login_path, json=data)
        self.assertIsNotNone(response)

        return response
