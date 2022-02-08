import requests
import json
from typing import Optional

from src.bootstrap_stages.stage01 import config
from src.core import SingletonMeta


class ClientTranslationYoda(metaclass=SingletonMeta):
    def __init__(self):
        self.basic_url = config.THIRD_PARTY_URL_POKEMON_TRANSLATION_YODA

    def grab(self, pokemon_name):
        try:
            initial_response = requests.get(self.basic_url, params=pokemon_name)
            details_url = initial_response['species'].url
            details = requests.get(details_url)
            return self._build_pokemon(pokemon_name, details)
        except:
            raise ExceptionPokeApiError()

    def _build_pokemon(self, name, details):
        description = details['flavor_text_entries'][0].flavor_text
        habitat = details['habitat'].name
        is_legendary = details['is_legendary']
        return Pokemon(name, description, habitat, is_legendary)