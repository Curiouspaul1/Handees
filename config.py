import os
from dotenv import load_dotenv


# set location for db
base_dir = os.path.abspath(os.getcwd())

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('secret')
    CLERK_KEY = os.getenv('clerk_dev_key')


class DevelopmentConfig(Config):
    load_dotenv(base_dir, '.env.development')
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{base_dir}/devdb.sqlite3"


class ProductionConfig(Config):
    load_dotenv(base_dir, '.env')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


config = {
    "default": DevelopmentConfig,
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
