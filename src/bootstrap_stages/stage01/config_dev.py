from datetime import timedelta

from src.bootstrap_stages.stage01.config_base import ConfigBase


class ConfigDev(ConfigBase):
    INFO = True
    TESTING = False
    PROPAGATE_EXCEPTIONS = True
