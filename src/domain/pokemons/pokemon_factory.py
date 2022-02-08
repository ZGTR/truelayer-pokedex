import requests
from src.bootstrap_stages.stage01 import config
from src.domain.exceptions.exception_pokeapi_error import ExceptionPokeApiError
from src.domain.exceptions.exception_pokemon_does_not_exits import ExceptionPokemonDoesNotExists
from src.services import ClientPokeApi, SingletonMeta


class PokemonFactory(metaclass=SingletonMeta):

    def __init__(self):
        pass

    @classmethod
    def grab(cls, pokemon_name):
        try:
            # Better to make ClientPokeApi as a singleton module.
            return ClientPokeApi().grab(pokemon_name)
        except:
            raise ExceptionPokeApiError()


