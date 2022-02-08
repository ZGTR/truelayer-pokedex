# Order matters
from flask import Flask
from flask_babel import Babel
from flask_cors import CORS
from flask_restful import Api
from flask import url_for

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

def print_routes():
    links = []
    for rule in app.url_map.iter_rules():
        # url = url_for(rule.endpoint, **(rule.defaults or {}))
        # print("url=%s, endpoint=%s", url, rule.endpoint)
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            print('-----url={}'.format(rule.endpoint))
            url = url_for(rule.endpoint, **(rule.defaults or {}), _external=True)
            links.append((url, rule.endpoint))
            print('url={}, endpoint={}'.format(url, rule.endpoint))
        # links is now a list of url, endpoint tuples

print('---- Bootstrapping the app ----')

# Order matters
app = Flask(__name__)

from src.bootstrap_stages.stage01 import *
app.config.from_object(config)

CORS(app)
api = Api(app)
babel = Babel(app)

from src.bootstrap_stages.stage02 import *
from src.bootstrap_stages.stage02.error_handling import *
app.register_blueprint(errors)

from src.resources import *

app.register_blueprint(routes)

# print_routes()
app.app_context().push()


