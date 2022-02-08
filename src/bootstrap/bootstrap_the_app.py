# Order matters
from flask import Flask
from flask_babel import Babel
from flask_cors import CORS
from flask_restful import Api

print('---- Bootstrapping the app ----')

# Order matters
app = Flask(__name__)

from src.bootstrap_stages.stage01 import *
app.config.from_object(config)

CORS(app)
api = Api(app)
babel = Babel(app)

from src.bootstrap_stages.stage02 import *
from src.bootstrap_stages.stage02.error_handling import *
app.register_blueprint(errors)

# from src.bootstrap_stages.stage03 import *
# from src.bootstrap_stages.stage04.flask_auth_manager import *

from src.resources import *
# api.init_app(routes)
app.register_blueprint(routes)

app.app_context().push()
