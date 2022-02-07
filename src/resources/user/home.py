from flask_jwt_extended import jwt_required

from src.bootstrap.bootstrap_the_app import api
from src.core.resource import BaseResource
from src.domain import *
from src.models.nfx_astarte_game import NfxAstarteGameModel
from src.resources import get_mobileapp_init_resp


class RcHome(BaseResource):
    decorators = [jwt_required]
    path = '/v1/user/home'

    def get(self):
        self.logRequest()
        self.logRequest()
        resp = {
            'actions': self.get_actions(),
            'mobile_app_init': get_mobileapp_init_resp(),
            'games': {
                'available_games': NfxAstarteGameModel.get_all_temp_fix_for_home_v1()
            }
        }

        return self.respond(resp)

    def get_actions(self):
        actions = {
            'progress_week_current':
            {
                'href': url_for('rcprogressweekcurrent'),
            },
            'progress_day_current':
            {
                'href': url_for('rcprogressdaycurrent'),
            },
            'rankings_daily_all':
            {
                'href': url_for('rcuserrankingsdailyall'),
            },
            'rankings_daily_digest':
            {
                'href': url_for('rcuserrankingsdailydigest'),
            },
            'calibration':
            {
                'href': url_for('rccalibration'),
                'params': dict(
                    nfx_device_name=None,
                    raw_data=None,
                )
            },
            'request_goodie_email':
            {
                'href': url_for('rcnhsuseremail'),
                'params': dict(email=None)
            },
            'game_specific_leaderboard':
            {
                'href': url_for('rcgamespecificleaderboard'),
                'params': dict(game_type=None)
            }
        }

        return actions


api.add_resource(RcHome, RcHome.path)
