import json

from flask import Response

from src.core.enhanced_json_encoder import EnhancedJSONEncoder


class JsonResponse(Response):
    def __init__(self,
                 response=None,
                 status=None,
                 headers=None,
                 mimetype=None,
                 direct_passthrough=False
                 ):
        super().__init__(json.dumps(response, cls=EnhancedJSONEncoder), status, headers, mimetype, self.content_type,
                         direct_passthrough)

    @property
    def content_type(self):
        return 'application/json'
