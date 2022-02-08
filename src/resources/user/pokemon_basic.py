from flask_restful import Resource
from flask import Flask, request, abort
from flask_restful import Resource, Api
from marshmallow import Schema, fields
from src.bootstrap.bootstrap_the_app import api
from src.core.schema import BaseSchema
from src.domain import *

class RcPokemonBasic(Resource):
    path = "/v1/pokemon/<string:pokemon_name>"

    def get(self, pokemon_name):
        # Better to have Base Resource class which handles schemas (Marshmallow) abstractly with its errors.

        resp = {
            'name': pokemon_name,
            'description': '',
            'habitat': '',
            'isLegendary': ''
        }
        return resp


api.add_resource(RcPokemonBasic, RcPokemonBasic.path)
