import unittest
from unittest import skip
from unittest.mock import patch
import mock
from mock import patch

import requests

from src.domain.pokemons.pokemon import Pokemon
from src.domain.translation_strategies.pokemon_translation_factory import PokemonTranslationFactory
from src.domain.translation_strategies.pokemon_translation_strategy_shakespeare import \
    PokemonTranslationStrategyShakespeare
from src.domain.translation_strategies.pokemon_translation_strategy_standard import PokemonTranslationStrategyStandard
from src.domain.translation_strategies.pokemon_translation_strategy_yoda import PokemonTranslationStrategyYoda
from src.services import ClientPokeApi
from src.tests.base import BaseTest

class TestTranslationFactory(BaseTest):
    cave_and_legendary_pokemon = Pokemon(name='foo', description='bar', habitat='cave', is_legendary=True)
    cave_and_not_legendary_pokemon = Pokemon(name='foo', description='bar', habitat='cave', is_legendary=True)
    non_cave_and_legendary_pokemon = Pokemon(name='foo', description='bar', habitat='a-habitat', is_legendary=True)
    non_cave_and_not_legendary_pokemon = Pokemon(name='foo', description='bar', habitat='a-habitat', is_legendary=False)

    def test_cave_and_legendary_pokemon(self):
        strategy = PokemonTranslationFactory().create_strategy(pokemon=self.cave_and_legendary_pokemon)
        self.assertIsInstance(strategy, PokemonTranslationStrategyYoda)

    def test_cave_and_not_legendary_pokemon(self):
        strategy = PokemonTranslationFactory().create_strategy(pokemon=self.cave_and_not_legendary_pokemon)
        self.assertIsInstance(strategy, PokemonTranslationStrategyYoda)

    def test_non_rare_or_cave_and_legendary_pokemon(self):
        strategy = PokemonTranslationFactory().create_strategy(pokemon=self.non_cave_and_legendary_pokemon)
        self.assertIsInstance(strategy, PokemonTranslationStrategyYoda)

    def test_non_rare_or_cave_and_not_legendary_pokemon(self):
        strategy = PokemonTranslationFactory().create_strategy(pokemon=self.non_cave_and_not_legendary_pokemon)
        self.assertIsInstance(strategy, PokemonTranslationStrategyShakespeare)

if __name__ == "__main__":
    unittest.main()