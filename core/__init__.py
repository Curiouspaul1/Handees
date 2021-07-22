from flask import Flask
from config import config
from .extensions import (
    db, migrate
)
import os

def create_app(config_name):
    # create flask app instance
    app = Flask(__name__)
    
    # set config using config name
    app.config.from_object(config[config_name])

    # register extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # register blueprints
    # from .user import 

    return app