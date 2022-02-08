
from src.bootstrap.bootstrap_the_app import api
from src.core.resource import BaseResource
from src.domain import *


class RcMeCall(BaseResource):
    path = '/v1/user/me'

    def get(self):
        resp = {
            'actions':
            {
                'impaired_hand_set':
                {
                    'href': url_for('rcimpairedhand'),
                    'params':
                        {
                            'impaired_hand': ''
                        }
                },

            }
        }

        return self.respond(resp)


api.add_resource(RcMeCall, RcMeCall.path)
