from marshmallow import fields
from marshmallow.validate import OneOf

from src.bootstrap.bootstrap_the_app import api
from src.core.schema import BaseSchema
from src.domain import *
from src.domain.translation_strategies.pokemon_translation_strategy import PokemonTranslationStrategy


class PokemonTrasnlationStrategyYoda(PokemonTranslationStrategy):

    def __init__(self):
        pass

    def translate(self, description):
        return None
