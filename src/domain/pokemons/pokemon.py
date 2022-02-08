from marshmallow import fields
from marshmallow.validate import OneOf

from src.bootstrap.bootstrap_the_app import api
from src.domain import *


class Pokemon:
    def __init__(self, name, basic_description, habitat, is_legendary):
        self.name = name
        self.basic_description = basic_description
        self.habitat = habitat
        self.is_legendary = is_legendary

