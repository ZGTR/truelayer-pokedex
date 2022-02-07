from datetime import timedelta
from src.bootstrap_stages.stage01.config_base import ConfigBase


class ConfigExample(ConfigBase):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'so-secret'

    TOKEN_ADMIN = 'token/admin'
    SEGMENT_API_KEY = 'key/segment'

    JWT_SECRET_KEY = 'another/secret/key/'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_AUTH_USERNAME_KEY = 'username'

    BABEL_TRANSLATION_DIRECTORIES: str = Utils.get_project_root() + '/assets/i18n'
    BABEL_DEFAULT_LOCALE: str = 'en'
    LANGUAGES = ['en']
