from flask_jwt_extended import current_user, jwt_required

from src.bootstrap.bootstrap_the_app import api
from src.core.resource import BaseResource
from src.domain import *


class RcMeCall(BaseResource):
    decorators = [jwt_required]
    path = '/v1/user/me'

    logger.error('---- current_user: %s', current_user)

    def get(self):
        self.logRequest()
        resp = {
            'actions':
            {
                'privacy_policy':
                {
                    'href': url_for('rcprivacypolicy'),
                },
                'impaired_hand_set':
                {
                    'href': url_for('rcimpairedhand'),
                    'params':
                        {
                            'impaired_hand': ''
                        }
                },
                'home':
                {
                    'href': url_for('rchome'),
                },
                "utc_offset_mins":
                {
                    'href': url_for("rcuserutcoffsetmins"),
                    'params':
                        {
                            'utc_offset_mins': ''
                        }
                }
            },
            'user': UserModel.get(hash_key=current_user.id,
                                  attributes_to_get=
                                  [
                                      'id',
                                      'username',
                                      'firstname',
                                      'lastname',
                                      'creation_date',
                                      'last_login',
                                      'email',
                                      "user_type",
                                      'impaired_hand',
                                      "utc_offset_mins"
                                  ]
                                  ),
        }

        return self.respond(resp)


api.add_resource(RcMeCall, RcMeCall.path)
