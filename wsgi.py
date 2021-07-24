from core import create_app
from flask_migrate import Migrate
from core.extensions import db
from sqlalchemy import event
from core.models import *
import os
import sqlite3

# spatialite path
spatialite_path = os.getenv('spat_path')
os.environ['PATH'] = spatialite_path + ';' + os.environ['PATH']

# create server instance from app factory
app = create_app(os.getenv("FLASK_CONFIG") or "default")

# pass app instance to migrate
migrate = Migrate(app, db)

with app.app_context():
    @event.listens_for(db.engine, "connect")
    def load_spatialite(dbapi_conn, connection_record):
        dbapi_conn.enable_load_extension(True)
        dbapi_conn.load_extension('mod_spatialite')


# configuring flask shell
@app.shell_context_processor
def make_shell_context():
    return dict(
        app=app, migrate=migrate
    )


if __name__ == "__main__":
    app.run()
