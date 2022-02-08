from typing import Mapping

from flask import request
from flask_babel import _
from flask_restful import Resource

from src.core.json_response import JsonResponse


class BaseResource(Resource):

    def respond(self, body, code: int = 200):
        return self._create_response(body, code)

    def respond_msg(self, message, code: int = 200):
        return self._create_response(dict(message=message), code)

    def respond_error(self, message=None, error_code: int = 500):
        body = dict(
            message=message if message else _('An error happened while trying to make this operation.')
        )
        return self._create_response(body, error_code)

    @classmethod
    def _create_response(cls, body=None, code=200):
        return JsonResponse(response=body, status=code)
