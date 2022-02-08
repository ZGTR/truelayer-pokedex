"""
from https://github.com/awslabs/aws-apigateway-lambda-authorizer-blueprints/blob/master/blueprints/python/api-gateway-authorizer-python.py
"""

from src.auth.auth_policy import AuthPolicy, HttpVerb


def get_token(event):

    if 'authorizationToken' not in event:
        return False, None

    full_token = event['authorizationToken']

    split = full_token.split('Bearer')

    if len(split) != 2:
        return False, None
        # if process.env.DEBUG == 'true':
        #     console.log('AUTH: no token in Bearer');
        # callback('Unauthorized');

    token = split[1].strip()

    return True, token


def get_principal_id(event, const_token):
    is_valid, token = get_token(event)

    if not is_valid:
        return None

    if token != const_token:
        return None

    principal_id = "truelayer/user/actual"

    return principal_id


def generate_default_policy(event, principal_id):
    tmp = event['methodArn'].split(':')
    apiGatewayArnTmp = tmp[5].split('/')
    awsAccountId = tmp[4]

    policy = AuthPolicy(None, awsAccountId)
    policy.restApiId = apiGatewayArnTmp[0]
    policy.region = tmp[3]
    policy.stage = apiGatewayArnTmp[1]
    policy.principalId = principal_id

    return policy

