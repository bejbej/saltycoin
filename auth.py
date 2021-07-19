from quart import request
from os import getenv

api_keys_env = getenv('API_KEYS')
api_keys = api_keys_env.split(',') if api_keys_env is not None else []
api_keys = [x.strip() for x in api_keys]

def requires_auth(func):
    def wrapper():
        auth_header_name = 'x-api-key'
        if not request.headers.has_key(auth_header_name):
            return 'Header "x-api-key" was not present', 401
        if not request.headers[auth_header_name] in api_keys:
            return 'API key was invalid', 401
        return func()
    return wrapper
