import json

from src.helpers.dumper import json_dumper
from src.bootstrap_stages.stage00.logger_setup import logger
from src.bootstrap_stages.stage01 import config
from src.auth.authorizers.policy_maker import _get_principal_id, _generate_default_policy


def lambda_handler(event, context):
    logger.error("---- authorizer_admin. event: %s, context:%s", event, json.dumps(context, default=json_dumper))

    principal_id = _get_principal_id(event, config.TOKEN_ADMIN)

    policy = _generate_default_policy(event, principal_id)

    policy.allowAllMethods() if principal_id else policy.denyAllMethods()

    return policy.build()
