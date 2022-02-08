from datetime import timedelta


class ConfigBase(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = None
    TOKEN_ADMIN = None

    PROPAGATE_EXCEPTIONS = True
    THIRD_PARTY_URL_POKEMON_BASIC_INFO = 'https://pokeapi.co/api/v2/pokemon-species'
    THIRD_PARTY_URL_POKEMON_TRANSLATION_SHAKESPEARE = 'https://api.funtranslations.com/translate/shakespeare'
    THIRD_PARTY_URL_POKEMON_TRANSLATION_YODA = 'https://api.funtranslations.com/translate/yoda'
