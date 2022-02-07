from datetime import timedelta
from src.bootstrap_stages.stage01.config_base import ConfigBase


class ConfigLocal(ConfigBase):
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'very/secret'

    TOKEN_ADMIN = 'local-nfx-admin-123'
    SEGMENT_API_KEY = 'local/segment/key/123'

    JWT_SECRET_KEY = 'jwt/local/secret/key/'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    SERVER_NAME = 'localhost:3010'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=0.5)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=0.75)
    JWT_AUTH_USERNAME_KEY = 'username'
    PROPAGATE_EXCEPTIONS = True
