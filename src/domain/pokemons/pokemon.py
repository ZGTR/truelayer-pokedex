from marshmallow import fields
from marshmallow.validate import OneOf

from src.bootstrap.bootstrap_the_app import api
from src.core.schema import BaseSchema
from src.domain import *


class Pokemon:
    def __init__(self, name, basic_description, habitat, is_legendary):
        self.name = name
        self.basic_description = basic_description
        self.habitat = habitat
        self.isLegendary = is_legendary

