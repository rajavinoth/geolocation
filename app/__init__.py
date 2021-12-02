from flask import Flask
from db.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
dbc = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    dbc.init_app(app)
    migrate.init_app(app, dbc)
    from app.main import blue_print
    app.register_blueprint(blue_print)
    return app

from app import models