import requests
from string import Template

from src.bootstrap_stages.stage01 import config
from src.core.metaclasses import SingletonMeta
from src.domain.exceptions.exception_pokeapi_error import ExceptionPokeApiError
from src.domain.pokemons.pokemon import Pokemon


class ClientPokeApi(metaclass=SingletonMeta):
    # Since we're dealing with a 3rd party API, it's good to put in a retry mechanism in the future with
    # a custom MIN, MAX tries and a priority before erroring a request.

    def __init__(self):
        self.basic_url = Template(f'{config.THIRD_PARTY_URL_POKEMON_BASIC_INFO}/$pokemon_name')

    def grab(self, pokemon_name):
        try:
            url = self.basic_url.substitute(pokemon_name=pokemon_name)
            details = requests.get(url).json()
            return self._build_pokemon(pokemon_name, details)
        except:
            raise ExceptionPokeApiError()

    def _build_pokemon(self, name, details):
        description = details['flavor_text_entries'][0]['flavor_text']
        habitat = details['habitat']['name']
        is_legendary = details['is_legendary']
        return Pokemon(name, description, habitat, is_legendary)
