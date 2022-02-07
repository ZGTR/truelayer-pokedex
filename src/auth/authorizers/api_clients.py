import base64

from src.models.api_client import ApiClientModel


def get_api_client_from_form_data(event):
    form = event['body']
    client_id = form['client_id']
    client_secret = form['client_secret']
    client = ApiClientModel.get_by_client_data(client_id, client_secret)
    return client


def get_api_client_from_headers(event):
    headers = event['headers']

    if 'Authorization' not in headers:
        return False

    authorization = headers['Authorization']

    b64_token = authorization.split(' ')[-1]

    # decode the base64 encoded header value
    client_id, client_secret = base64.b64decode(b64_token).decode("ascii").split(':')

    # check if the given api key actually exists
    client = ApiClientModel.get_by_client_data(client_id, client_secret)

    return client
