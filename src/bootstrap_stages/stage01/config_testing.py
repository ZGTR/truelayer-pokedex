from datetime import timedelta

from src.bootstrap_stages.stage01.config_base import ConfigBase


class ConfigTesting(ConfigBase):
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'i/love/testing'

    TOKEN_ADMIN = 'testing-nfx-admin-123'
    SEGMENT_API_KEY = 'testing/segment/key/'

    JWT_SECRET_KEY = 'jwt/testing/secret/key'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_AUTH_USERNAME_KEY = 'username'
    PROPAGATE_EXCEPTIONS = True

    CLOUDFRONT_DOMAIN_NAME = 'content_bucket/cloud_front/domain_name'
