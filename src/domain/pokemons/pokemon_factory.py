import requests
from src.bootstrap_stages.stage01 import config
from src.domain.exceptions.exception_pokeapi_error import ExceptionPokeApiError
from src.domain.exceptions.exception_pokemon_does_not_exits import ExceptionPokemonDoesNotExists
from src.services import ClientPokeApi


class PokemonFactory:

    def __init__(self):
        pass

    def grab(self, pokemon_name):
        try:
            return ClientPokeApi.grab(pokemon_name)
        except:
            raise ExceptionPokeApiError()


