from flask import Blueprint

user = Blueprint('user', __name__, url_prefix="/user")

# import controller resources
from . import views

# register sub-blueprints
from .client import client
from .provider import provider

user.register_blueprint(client)
user.register_blueprint(provider)
