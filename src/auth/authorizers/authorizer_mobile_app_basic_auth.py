import json

from src.auth.authorizers.api_clients import get_api_client_from_headers
from src.auth.authorizers.policy_maker import _generate_default_policy
from src.bootstrap_stages.stage00.logger_setup import logger
from src.helpers.dumper import json_dumper


def _get_principal_id(event):
    client = get_api_client_from_headers(event)

    # All is well, return a policy which allows this user to access to this api
    # this call is cached for all authenticated calls, so we need to give
    # access to the whole api. This could be done by having a policyDocument
    # for each available function.

    if client:
        principal_id = client['client_id']
        return principal_id

    return False, None


def lambda_handler(event, context):
    logger.error("---- authorizer_mobile_app_basic_auth. event: %s, context:%s", event, json.dumps(context, default=json_dumper))

    principal_id = _get_principal_id(event)

    policy = _generate_default_policy(event, principal_id)

    if principal_id:
        policy.allowAllMethods()
    else:
        policy.denyAllMethods()
        logger.error("----- Not recognizable client. You are not allowed here.")

    return policy.build()
