from datetime import timedelta

from src.bootstrap_stages.stage01.config_base import ConfigBase


class ConfigStaging(ConfigBase):
    DEBUG = False
    TESTING = False
    SECRET_KEY = params['SECRET_KEY']
    PROPAGATE_EXCEPTIONS = True
