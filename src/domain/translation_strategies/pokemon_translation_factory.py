from marshmallow import fields
from marshmallow.validate import OneOf

from src.bootstrap.bootstrap_the_app import api
from src.core.resource import BaseResource
from src.core.schema import BaseSchema
from src.domain import *


class PokemonTranslationFactory:
    def __init__(self):
        pass

    def create_strategy(self, pokemon):

