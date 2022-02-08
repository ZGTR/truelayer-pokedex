import json

from src.auth.authorizers.api_clients import get_api_client_from_headers
from src.auth.authorizers.policy_maker import generate_default_policy
from src.bootstrap_stages.stage00.logger_setup import logger


def _get_principal_id(event):
    # Return a policy which allows this user to access to this api
    # this call is cached for all authenticated calls, so we need to give
    # access to the whole api. This could be done by having a policyDocument
    # for each available function.
    client = get_api_client_from_headers(event)

    if client:
        principal_id = client['client_id']
        return principal_id

    return None


def lambda_handler(event, context):
    principal_id = _get_principal_id(event)

    policy = generate_default_policy(event, principal_id)

    if principal_id:
        policy.allowAllMethods()
    else:
        logger.error("Not a recognizable client. You are not allowed here.")
        policy.denyAllMethods()

    built_policy = policy.build()

    print(f'build_policy = {built_policy}')

    return built_policy
