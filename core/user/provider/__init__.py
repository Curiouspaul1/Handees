from flask import Blueprint

provider = Blueprint('provider', __name__, url_prefix="/provider")

from . import views

