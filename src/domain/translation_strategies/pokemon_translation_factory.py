from src.bootstrap.bootstrap_the_app import api
from src.core.metaclasses import SingletonMeta
from src.domain import *
from src.domain.translation_strategies.pokemon_translation_strategy import PokemonTranslationStrategy
from src.domain.translation_strategies.pokemon_translation_strategy_shakespeare import \
    PokemonTranslationStrategyShakespeare
from src.domain.translation_strategies.pokemon_translation_strategy_standard import PokemonTranslationStrategyStandard
from src.domain.translation_strategies.pokemon_translation_strategy_yoda import PokemonTranslationStrategyYoda


class PokemonTranslationFactory(metaclass=SingletonMeta):

    def __init__(self):
        pass

    def create_strategy(self, pokemon) -> PokemonTranslationStrategy:
        if pokemon.habitat == 'cave' or pokemon.is_legendary:
            return PokemonTranslationStrategyYoda()
        return PokemonTranslationStrategyShakespeare()

