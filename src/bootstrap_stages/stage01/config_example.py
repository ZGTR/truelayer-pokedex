from datetime import timedelta
from src.bootstrap_stages.stage01.config_base import ConfigBase


class ConfigExample(ConfigBase):
    DEBUG = False
    TESTING = False
    BABEL_TRANSLATION_DIRECTORIES: str = Utils.get_project_root() + '/assets/i18n'
    BABEL_DEFAULT_LOCALE: str = 'en'
    LANGUAGES = ['en']
