from marshmallow import fields
from marshmallow.validate import OneOf

from src.bootstrap.bootstrap_the_app import api
from src.core.resource import BaseResource
from src.core.schema import BaseSchema
from src.domain import *


class PokemonTranslationFactory:

    TRANSLATION_FACTORY_MAP = {
        Pokemon()
    }

    def __init__(self):
        pass

    def create_strategy(self, pokemon):
        try:
            if pokemon.habitat == 'cave' or pokemon.isLegendary:
                PokemonTrasnlationStrategyYoda()
            else
                PokemonTranslationShakespeare()
        except:
            PokemonTranslationStandard()

