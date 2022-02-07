from datetime import datetime
from unittest.mock import patch

from dateutil.tz import tzutc
from flask_babel import _
from freezegun import freeze_time
from werkzeug.exceptions import BadRequest

from src.tests.integration.integration_base_test import IntegrationBaseTest


class SignupTest(IntegrationBaseTest):
    data_sources = ['integration/auth/user-groups']
    signup_path = "/admin/v1/user/signup"

    def signup(self, data):
        response = self.app.post(self.signup_path, json=data)
        self.assertIsNotNone(response)
        return response

    @freeze_time(datetime.now(tz=tzutc()))
    @patch('uuid.uuid1')
    def test_valid_signedUp(self, uuid):
        uuid.return_value.hex = 'some-new-random-uuid'
        user = dict(
            username="signup-test@admin.com",
            email="signup-test@admin.com",
            password="secret",
            firstname="firstname",
            lastname="lastname",
            user_group='NFX_HQ',
            country='uk'
        )

        response = self.signup(user)
        self.assertStatusCode(response, 200)
        data = response.get_json()

        user['id'] = uuid().hex
        self.assertUserSignedUp(data, user)

    def test_differentUsernameAndEmail_400emailNotSameAsUsername(self):
        user = dict(
            username="signup-username@admin.com",
            email="signup-email@admin.com",
            password="secret",
            firstname="firstname",
            lastname="lastname",
            user_group='NFX_HQ',
            country='uk',
        )

        response = self.signup(user)
        self.assertEqual(response.status_code, BadRequest.code)

        actual_response = response.get_json()
        expected_response = dict(
            reply="Missing: email_username: ['Email is not the same as Username. For now this is not permitted.']",
            success=False,
        )

        self.assertEqual(actual_response, expected_response)

    def test_missingFields_400Missing(self):
        user = dict(
            password="1",
        )

        response = self.signup(user)
        self.assertEqual(response.status_code, 400)

        actual_json = response.get_json()
        expected_json = dict(
            reply='',
            success=False,
        )

        self.assertDictStructure(actual_json, expected_json)

    @patch('uuid.uuid1')
    @freeze_time(datetime.now())
    def test_userAlreadyExists_emailExists(self, uuid):
        uuid.return_value.hex = 'some-random-uuid'
        user = dict(
            username="signup-test2@admin.com",
            email="signup-test2@admin.com",
            password="secret",
            firstname="firstname",
            lastname="lastname",
            user_group='NFX_HQ',
            country = 'uk',
        )

        # first time
        response = self.signup(user)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertUserSignedUp(data, dict(**user, id=uuid().hex))

        # second time (duplicated email)
        response = self.signup(user)
        self.assertEqual(response.status_code, BadRequest.code)

        actual_response = response.get_json()
        expected_response = dict(
            reply=_('An account with the same Email address already exists. Please make sure the Email you '
                    'provided is correct or signup using a different email address.'),
            success=False,
        )

        self.assertEqual(actual_response, expected_response)
