from flask import Flask
from config import config


def create_app(config_name):
    # create flask app instance
    app = Flask(__name__)
    
    # set config using config name
    app.config.from_object(config[config_name])

    # register blueprints
    from .user import user 
    app.register_blueprint(user)

    return app
