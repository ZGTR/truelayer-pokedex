from flask_restful import Resource
from flask import Flask, request, abort
from flask_restful import Resource, Api
from marshmallow import Schema, fields
from src.bootstrap.bootstrap_the_app import api
from src.core.base_resource import BaseResource
from src.domain import *
from src.domain.pokemons.pokemon_basic_factory import PokemonBasicFactory


class RcPokemonBasic(BaseResource):
    # Better to create logic in TrueLayerResource class which handles schemas (Marshmallow) abstractly with its errors.
    path = "/v1/pokemon/<string:pokemon_name>"

    def get(self, pokemon_name):
        try:
            pokemon = PokemonBasicFactory().grab(pokemon_name)

            # We can return this directly from pokemon.__dict__ and JSONify it in 1 line.
            # But, since we want to separate between presentation API and business layer,
            # it's better to keep them separate for now.
            resp = {
                'name': pokemon.name,
                'description': pokemon.description,
                'habitat': pokemon.habitat,
                'isLegendary': pokemon.is_legendary
            }

            return self.respond(resp)
        except Exception as e:
            return self.respond_error(message=str(e), error_code=500)


api.add_resource(RcPokemonBasic, RcPokemonBasic.path)
