import os

from src.bootstrap_stages.stage00.logger_setup import logger
from src.bootstrap_stages.stage01.config_base import *


def set_config():
    stage = os.environ.get('stage')
    logger.error('Running with stage: %s', stage)

    # uncomment to debug tests in IDE
    # if stage is None:
    #     stage = 'test-api'
    # please do not check in uncommented!

    if stage == 'test-api':
        from src.bootstrap_stages.stage01.config_testing import ConfigTesting
        target = ConfigTesting
    elif stage == 'local-api':
        from src.bootstrap_stages.stage01.config_local import ConfigLocal
        target = ConfigLocal
    elif stage == 'dev-api':
        from src.bootstrap_stages.stage01.config_dev import ConfigDev
        target = ConfigDev
    elif stage == 'staging-api':
        from src.bootstrap_stages.stage01.config_staging import ConfigStaging
        target = ConfigStaging
    elif stage == 'prod-api':
        from src.bootstrap_stages.stage01.config_prod import ConfigProd
        target = ConfigProd
    else:
        raise ValueError('Invalid environment name')

    return target


config = set_config()
