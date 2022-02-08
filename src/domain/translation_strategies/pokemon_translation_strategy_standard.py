from marshmallow import fields
from marshmallow.validate import OneOf

from src.bootstrap.bootstrap_the_app import api
from src.core.resource import BaseResource
from src.core.schema import BaseSchema
from src.domain import *
from src.domain.translation_strategies.pokemon_translation_strategy import PokemonTranslationStrategy


class PokemonTranslationStrategyStandard(PokemonTranslationStrategy):
    # Although this only return the same description, this makes it easier for the future
    # to change, test and mock the behaviour.

    def __init__(self):
        pass

    def translate(self, description):
        return description
