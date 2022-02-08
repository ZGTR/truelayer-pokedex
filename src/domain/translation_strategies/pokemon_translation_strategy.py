import abc
from marshmallow import fields
from marshmallow.validate import OneOf

from src.bootstrap.bootstrap_the_app import api
from src.core.schema import BaseSchema
from src.domain import *


class PokemonTranslationStrategy(object):

    def __init__(self):
        pass

    @abc.abstractmethod
    def translate(self, description):
        return None
