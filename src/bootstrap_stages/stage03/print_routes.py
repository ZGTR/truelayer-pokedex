from flask import url_for
from src.bootstrap.bootstrap_the_app import app


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

