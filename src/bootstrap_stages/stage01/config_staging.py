from datetime import timedelta

from src.bootstrap_stages.stage01.config_base import ConfigBase


class ConfigStaging(ConfigBase):
    # AWS Parameter store allows us to organize parameters into hierarchies
    # https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-paramstore-su-organize.html
    # path variable is used as the root of the hierarchy
    SSM_PATH = '/NFX_ARES/STAGING/'
    DEBUG = False
    TESTING = False
    SECRET_KEY = params['SECRET_KEY']

    TOKEN_ADMIN = params['TOKEN_ADMIN']
    SEGMENT_API_KEY = params['SEGMENT/API_KEY']

    JWT_SECRET_KEY = params['JWT/SECRET_KEY']
    JWT_BLACKLIST_ENABLED = Utils.str2bool(params['JWT/BLACKLIST_ENABLED'])
    JWT_BLACKLIST_TOKEN_CHECKS = params['JWT/BLACKLIST_TOKEN_CHECKS']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(params['JWT/ACCESS_TOKEN_EXPIRES']))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(params['JWT/REFRESH_TOKEN_EXPIRES']))
    JWT_AUTH_USERNAME_KEY = params['JWT/AUTH_USERNAME_KEY']
    PROPAGATE_EXCEPTIONS = True

    CLOUDFRONT_DOMAIN_NAME = 'd2g4npqfoc9mot.cloudfront.net'
