from datetime import timedelta

from src.bootstrap_stages.stage01.config_base import ConfigBase


class ConfigProd(ConfigBase):
    DEBUG = False
    TESTING = False
    SECRET_KEY = params['SECRET_KEY']
    TOKEN_ADMIN = params['TOKEN_ADMIN']
    PROPAGATE_EXCEPTIONS = True
