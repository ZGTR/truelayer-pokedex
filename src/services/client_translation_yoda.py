import requests
import json
from typing import Optional

from src.bootstrap_stages.stage01 import config
from src.core.metaclasses import SingletonMeta
from src.domain.exceptions.exception_translation_too_many_requests import ExceptionApiTranslationTooManyRequests
from src.domain.exceptions.exception_translation_yoda import ExceptionApiTranslationYodaError


class ClientTranslationYoda(metaclass=SingletonMeta):
    # This is a different service from Shakespeare even though they use the same 3rd party API.
    # This is on purpose to allow exchanging this with any other API. Tests should keep enforcing the same behaviour.

    # Since we're dealing with a 3rd party API, it's good to put in a retry mechanism in the future with
    # a custom MIN, MAX tries and a priority before erroring a request.

    def __init__(self):
        self.basic_url = config.THIRD_PARTY_URL_POKEMON_TRANSLATION_YODA

    def translate(self, description):
        try:
            data = {
                'text': description
            }
            resp = requests.post(self.basic_url, params={}, json=data)
            if resp.status_code == 429:
                raise ExceptionApiTranslationTooManyRequests()
            json = resp.json()
            return json['contents']['translated']
        except:
            raise ExceptionApiTranslationYodaError()