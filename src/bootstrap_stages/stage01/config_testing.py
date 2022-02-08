from datetime import timedelta

from src.bootstrap_stages.stage01.config_base import ConfigBase


class ConfigTesting(ConfigBase):
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'i/love/testing'
    PROPAGATE_EXCEPTIONS = True
