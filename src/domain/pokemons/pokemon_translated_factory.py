import requests
from src.bootstrap_stages.stage01 import config
from src.domain.exceptions.exception_pokeapi_error import ExceptionPokeApiError
from src.domain.exceptions.exception_pokemon_does_not_exits import ExceptionPokemonDoesNotExists
from src.domain.translation_strategies.pokemon_translation_factory import PokemonTranslationFactory
from src.domain.translation_strategies.pokemon_translation_strategy_standard import PokemonTranslationStrategyStandard
from src.services import ClientPokeApi, SingletonMeta


class PokemonTranslatedFactory(metaclass=SingletonMeta):

    def __init__(self):
        pass

    def grab(self, pokemon_name):
        try:
            pokemon = ClientPokeApi().grab(pokemon_name)
            strategy = PokemonTranslationFactory().create_strategy(pokemon)
            pokemon.description = strategy.translate(pokemon.description)
            return pokemon
        except:
            pokemon.description = PokemonTranslationStrategyStandard().translate(pokemon.description)
            return pokemon


