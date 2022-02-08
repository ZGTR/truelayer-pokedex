import os
import boto3
from unittest import TestCase
from moto import mock_s3, mock_ses

from src.bootstrap.bootstrap_the_app import app

@mock_s3
@mock_ses
class BaseTest(TestCase):
    data_sources = []
    maxDiff = None

    def setUp(self):
        super().setUp()
        self.app = app.test_client()
        self.app.application.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False

        self.ctx = app.test_request_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

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

    def assertStatusCode(self, response, status_code):
        self.assertEqual(status_code, response.status_code)