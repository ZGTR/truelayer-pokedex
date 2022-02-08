from marshmallow import fields
from marshmallow.validate import OneOf

from src.bootstrap.bootstrap_the_app import api
from src.domain import *
from src.domain.translation_strategies.pokemon_translation_strategy import PokemonTranslationStrategy
from src.services.client_translation_shakespeare import ClientTranslationShakespeare


class PokemonTranslationStrategyShakespeare(PokemonTranslationStrategy):

    def __init__(self):
        pass

    def translate(self, description):
        return ClientTranslationShakespeare().translate(description)
