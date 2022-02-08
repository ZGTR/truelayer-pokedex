from typing import Mapping

from flask import request
from flask_babel import _
from flask_restful import Resource

from src.core.json_response import JsonResponse
from src.core.schema import BaseSchema
from src.bootstrap_stages.stage00.logger_setup import logger


class BaseResource(Resource):
    def __init__(self):
        self.decorate_method_schema()

    def decorate_method_schema(self):
        if isinstance(self.method_decorators, Mapping):
            decorators = self.method_decorators.get(request.method.lower(), [])
            new_decorators = self._decorate_schema(decorators)
            self.method_decorators[request.method.lower()] = new_decorators
        else:
            decorators = self.method_decorators
            new_decorators = self._decorate_schema(decorators)
            self.method_decorators = new_decorators

    @classmethod
    def _decorate_schema(cls, decorators):
        new_decorators = []
        for decorator in decorators:
            if isinstance(decorator, BaseSchema):
                decorator = decorator.decorator()
            new_decorators.append(decorator)
        return new_decorators


    @classmethod
    def _logAccess(cls, inputString):
        path = ""
        if hasattr(cls, "path"):
            path = cls.path
        elif hasattr(request, "path"):
            path = request.path
        else:
            path = "unknown"

        logger.error(f"Endpoint: {inputString} - Path: {path}")

    @classmethod
    def logRequest(cls):
        cls._logAccess("requested")

    @classmethod
    def _logResponse(cls, httpResponseCode):
        logString = "response created"
        logString += f" - HTTP response code: {httpResponseCode}"
        cls._logAccess(logString)


    @classmethod
    def respond(cls, body, code: int = 200):
        return cls.create_response(dict(**body, success=True), code)

    @classmethod
    def respond_items(cls, items, code: int = 200):
        return cls.create_response(dict(items=items, success=True), code)

    @classmethod
    def respond_item(cls, item, code: int = 200):
        return cls.create_response(dict(item=item, success=True), code)

    @classmethod
    def respond_msg(cls, msg, code: int = 200):
        return cls.create_response(dict(reply=msg, success=True), code)

    @classmethod
    def create_response(cls, body, code):
        cls._logResponse(code)
        return JsonResponse(response=body, status=code)

    @classmethod
    def respond_error(cls, msg=None, error_code: int = 500):
        cls._logResponse(error_code)
        body = dict(
            success=False,
            reply=msg if msg else _('An error happened while trying to make this operation.')
        )
        return cls.create_response(body, error_code)
