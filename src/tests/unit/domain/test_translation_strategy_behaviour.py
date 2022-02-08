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

class TestTranslationStrategyBehaviour(BaseTest):
    # We can add test and mock the translation APIs here.
    # Since we've covered part of mocking in other tests, and since testing the actual
    # logic of translation is trivial and will mostly be mocked, this is left empty.
    pass

if __name__ == "__main__":
    unittest.main()