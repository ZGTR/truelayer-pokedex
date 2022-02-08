import requests
from src.bootstrap_stages.stage01 import config
from src.domain.exceptions.exception_pokeapi_error import ExceptionPokeApiError
from src.domain.exceptions.exception_pokemon_does_not_exits import ExceptionPokemonDoesNotExists
from src.domain.translation_strategies.pokemon_translation_factory import PokemonTranslationFactory
from src.services import ClientPokeApi, SingletonMeta


class PokemonTranslatedFactory(metaclass=SingletonMeta):

    def __init__(self):
        pass

    def grab(self, pokemon_name):
        try:
            pokemon = ClientPokeApi().grab(pokemon_name)
            print(f'---pokemon={pokemon.__dict__}')
            print(f'---pre/pokemon.description={pokemon.description}')

            strategy = PokemonTranslationFactory().create_strategy(pokemon)
            print(f'---strategy={strategy}')
            pokemon.description = strategy.translate(pokemon.description)
            print(f'---post/pokemon.description={pokemon.description}')
            return pokemon
        except:
            # Should be a different exception based on error in PokeAPI or Translation.
            raise ExceptionPokeApiError()


