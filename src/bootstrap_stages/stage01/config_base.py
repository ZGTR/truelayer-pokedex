from datetime import timedelta


class ConfigBase(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = None

    TOKEN_ADMIN = None
    SEGMENT_API_KEY = None

    JWT_SECRET_KEY = None
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_AUTH_USERNAME_KEY = 'username'
    PROPAGATE_EXCEPTIONS = True

    THIRD_PARTY_URL_POKEMON_BASIC_INFO = 'https://pokeapi.co/api/v2/pokemon'
    THIRD_PARTY_URL_POKEMON_TRANSLATION_SHAKESPEARE = 'https://api.funtranslations.com/translate/shakespeare'
    THIRD_PARTY_URL_POKEMON_TRANSLATION_YODA = 'https://api.funtranslations.com/translate/yoda'
