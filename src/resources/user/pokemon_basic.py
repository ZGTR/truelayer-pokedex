from flask_restful import Resource
from flask import Flask, request, abort
from flask_restful import Resource, Api
from marshmallow import Schema, fields
from src.bootstrap.bootstrap_the_app import api
from src.core.schema import BaseSchema
from src.domain import *
from src.domain.pokemons.pokemon_factory import PokemonFactory


class RcPokemonBasic(Resource):
    # Better to create a BaseResource class which handles schemas (Marshmallow) abstractly with its errors.
    path = "/v1/pokemon/<string:pokemon_name>"

    def get(self, pokemon_name):
        pokemon = PokemonFactory.grab(pokemon_name)

        # We can return this directly from pokemon.__repr__ and JSONify it in 1 line.
        # But, since we want to separate between presentation API and business layer,
        # it's better to keep them separate for now.
        resp = {
            'name': pokemon.name,
            'description': pokemon.basic_description,
            'habitat': pokemon.habitat,
            'isLegendary': pokemon.is_legendary
        }

        return resp


api.add_resource(RcPokemonBasic, RcPokemonBasic.path)
