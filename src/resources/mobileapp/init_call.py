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
        )
    )
    return resp



class RcMobileAppInitV1(BaseResource):
    path = "/v1/mobile-app/init"

    def get(self):
        print('----- in resource')
        resp = get_mobileapp_init_resp()
        return self.respond(resp)


api.add_resource(RcMobileAppInitV1, RcMobileAppInitV1.path)
