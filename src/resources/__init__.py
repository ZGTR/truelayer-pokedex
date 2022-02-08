from flask import Blueprint
routes = Blueprint('resources', __name__)

# Important line for RESTful-flask to work
from src.bootstrap.bootstrap_the_app import app

from .app_init import *
from .user import *
from .auth import *
