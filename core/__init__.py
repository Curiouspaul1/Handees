from flask import Flask
from config import config
from .extensions import db

def create_app(config_name):
    # create flask app instance
    app = Flask(__name__)
    
    # set config using config name
    app.config.from_object(config[config_name])

    # pass app instance to extensions
    db.init_app(app)

    # register blueprints
    from .user import user 
    app.register_blueprint(user)

    return app
