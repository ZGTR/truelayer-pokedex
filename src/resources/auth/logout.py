from flask_jwt_extended import (jwt_required, jwt_refresh_token_required,
                                get_raw_jwt)

from src.bootstrap.bootstrap_the_app import api
from src.core.resource import BaseResource


class RcUserLogoutAccess(BaseResource):
    path = '/v1/user/auth/logout/access'
    decorators = [jwt_required]

    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            # FIXME: revoke token
            return self.respond(dict(message='Access token has been revoked'))
        except:
            return self.respond_msg(msg='Something went wrong', code=500)


class UserLogoutRefresh(BaseResource):
    path = '/v1/user/auth/logout/refresh'

    @jwt_refresh_token_required
    def post(self):
        self.logRequest()
        jti = get_raw_jwt()['jti']
        # TODO: Uncomment the logic
        # try:
        #     revoked_token = RevokedTokenModel(jti=jti)
        #     revoked_token.add()
        #     return {'message': 'Refresh token has been revoked'}
        # except:
        #     return {'message': 'Something went wrong'}, 500


api.add_resource(RcUserLogoutAccess, RcUserLogoutAccess.path)
api.add_resource(UserLogoutRefresh, UserLogoutRefresh.path)
