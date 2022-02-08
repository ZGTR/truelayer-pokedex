from src.bootstrap.bootstrap_the_app import api
from src.core.resource import BaseResource
from src.core.schema import BaseSchema
from src.domain import *
from src.domain.translation_strategies.pokemon_translation_strategy_shakespeare import \
    PokemonTranslationStrategyShakespeare
from src.domain.translation_strategies.pokemon_translation_strategy_standard import PokemonTranslationStrategyStandard
from src.domain.translation_strategies.pokemon_translation_strategy_yoda import PokemonTrasnlationStrategyYoda


class PokemonTranslationFactory:

    def __init__(self):
        pass

    def create_strategy(self, pokemon):
        try:
            if pokemon.habitat == 'cave' or pokemon.isLegendary:
                return PokemonTrasnlationStrategyYoda()
            else:
                return PokemonTranslationStrategyShakespeare()
        except:
            return PokemonTranslationStrategyStandard()

