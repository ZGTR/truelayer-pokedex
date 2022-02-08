from src.bootstrap.bootstrap_the_app import api
from src.core.metaclasses import SingletonMeta
from src.core.schema import BaseSchema
from src.domain import *
from src.domain.translation_strategies.pokemon_translation_strategy_shakespeare import \
    PokemonTranslationStrategyShakespeare
from src.domain.translation_strategies.pokemon_translation_strategy_standard import PokemonTranslationStrategyStandard
from src.domain.translation_strategies.pokemon_translation_strategy_yoda import PokemonTrasnlationStrategyYoda


class PokemonTranslationFactory(metaclass=SingletonMeta):

    def __init__(self):
        pass

    def create_strategy(self, pokemon):
        try:
            if pokemon.habitat == 'cave' or pokemon.is_legendary:
                return PokemonTrasnlationStrategyYoda(pokemon.basic_description)
            else:
                return PokemonTranslationStrategyShakespeare(pokemon.basic_description)
        except:
            return PokemonTranslationStrategyStandard(pokemon.basic_description)

