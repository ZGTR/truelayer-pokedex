import json

from src.auth.authorizers.api_clients import get_api_client_from_form_data
from src.helpers.dumper import json_dumper
from src.bootstrap_stages.stage00.logger_setup import logger
from src.bootstrap_stages.stage01 import config
from src.auth.authorizers.policy_maker import _get_principal_id, _generate_default_policy


def lambda_handler(event, context):
    logger.error("---- authorizer_mobile_app_bearer. event: %s, context:%s", event, json.dumps(context, default=json_dumper))

    # TODO: JWT is handling the tokens check now. Move the check here?
    # is_valid, principal_id =_get_principal_id(event, 'token/123')
    principal_id = "nfx/user/actual"

    policy = _generate_default_policy(event, principal_id)
    policy.allowAllMethods()
    return policy.build()
