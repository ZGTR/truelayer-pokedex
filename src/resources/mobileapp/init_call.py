from flask import url_for

from src.bootstrap.bootstrap_the_app import api
from src.core.resource import BaseResource


def get_mobileapp_init_resp():
    resp = dict(
        android=dict(
            latest=25,
            min_allowed=25,
            repeat_push=0
        ),
        ios=dict(
            latest=0,
            min_allowed=0,
            repeat_push=0
        ),
        actions={
            'forgot_activation_code': {
                'href': url_for('rcforgotactivationcode'),
                'params': dict(
                    email=None
                )
            },
            'me': {
                'href': url_for('rcmecall'),
            }
        },
    )
    return resp


# To delete
class RcMobileAppInitV1(BaseResource):
    path = "/v1/mobile-app/init"

    def get(self):
        self.logRequest()
        resp = get_mobileapp_init_resp()
        return self.respond(resp)


class RcMobileAppInitV2(BaseResource):
    path = "/v2/mobile-app/init"

    def get(self):
        self.logRequest()
        resp = get_mobileapp_init_resp()
        return self.respond(resp)


api.add_resource(RcMobileAppInitV1, RcMobileAppInitV1.path)
api.add_resource(RcMobileAppInitV2, RcMobileAppInitV2.path)
