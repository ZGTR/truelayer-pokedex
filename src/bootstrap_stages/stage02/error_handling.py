from http.client import HTTPException

import flask
from flask import Blueprint
from marshmallow import ValidationError

from src.bootstrap_stages.stage01 import config

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(ValidationError)
def on_validation_error(e):
    messages = e.messages
    message = ", ".join(map(lambda item: f"{item[0]}: {item[1]}", messages.items()))

    # FIXME: Error must be 422, not 400.
    return flask.jsonify(reply=f"Missing: {message}", success=False), 400


@errors.app_errorhandler(404)
def on_error_404(e):
    return flask.jsonify(error=404, text=str(e)), 404


@errors.app_errorhandler(403)
def on_error_403(e):
    return flask.jsonify(error=403, text=str(e)), 403


@errors.app_errorhandler(500)
def on_error_500(e):
    return flask.jsonify(error=500, text=str(e)), 500


if not config.DEBUG:
    @errors.app_errorhandler(Exception)
    def handle_root_exception(e):
        code = 500
        if isinstance(e, HTTPException):
            code = e.code
        return flask.jsonify(error=str(e)), code

# def get_http_exception_handler(my_app):
#     """Overrides the default http exception handler to return JSON."""
#     handle_http_exception = my_app.handle_http_exception
#
#     @wraps(handle_http_exception)
#     def ret_val(exception):
#         exc = handle_http_exception(exception)
#         return jsonify({'code': exc.code, 'message': exc.description}), exc.code
#
#     return ret_val
#
#
# app.handle_http_exception = get_http_exception_handler(app)
#
# app.register_error_handler(Exception, get_http_exception_handler)
