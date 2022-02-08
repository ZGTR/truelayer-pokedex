from datetime import timedelta
from src.bootstrap_stages.stage01.config_base import ConfigBase


class ConfigLocal(ConfigBase):
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'very/secret'
    SERVER_NAME = 'localhost:3000'
    PROPAGATE_EXCEPTIONS = True
