import os
from unittest import TestCase

import boto3
from moto import mock_s3, mock_ses

from src.bootstrap.bootstrap_the_app import app
from src.database.migrations.ddb_migrator import DDbMigrator
from src.database.seeds.seeder import Seeder
from src.helpers.utils import Utils


@mock_s3
@mock_ses
class BaseTest(TestCase):
    data_sources = []
    maxDiff = None

    def setUp(self):
        super().setUp()
        self.set_aws_credentials()

        self.app = app.test_client()
        self.app.application.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False

        DDbMigrator.up()

        Seeder.ddb_seed(sources=self.data_sources)

        self.ctx = app.test_request_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()
        DDbMigrator.down()

        super().tearDown()

    def assertKeysIn(self, keys, dictionary):
        dict_keys = dictionary.keys()
        for key in keys:
            self.assertIn(key, dict_keys)

    def assertDictStructure(self, first: dict, second: dict):
        self._assertOneWayDict(second, first)
        self._assertOneWayDict(first, second)

    def _assertOneWayDict(self, first, second):
        for first_key in first.keys():
            self._assertOneKeyStructure(first_key, first, second)

    def _assertOneKeyStructure(self, first_key, first, second):
        self.assertIn(first_key, second)
        first_key_type = type(first[first_key])
        second_key_type = type(second[first_key])
        self.assertEqual(first_key_type, second_key_type)
        if first_key_type is dict:
            self.assertDictStructure(first[first_key], second[first_key])

        elif first_key_type is list:
            first_items = first[first_key]
            second_items = second[first_key]
            self.assertCountEqual(first_items, second_items)

    def assertDate(self, expected_date, actual_date):
        if actual_date:
            if isinstance(actual_date, str):
                actual_date = Utils.str_to_date(actual_date)
        self.assertEqual(expected_date, actual_date)

    def set_aws_credentials(self):
        """Mocked AWS Credentials for moto."""
        os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
        os.environ['AWS_SECURITY_TOKEN'] = 'testing'
        os.environ['AWS_SESSION_TOKEN'] = 'testing'
        boto3.setup_default_session()
