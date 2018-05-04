from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .views import (
    bp_core,
    bp_apollo)

def create_app(config):
    print('*** Creating app with environment: {}'.format(config))
    app = Flask(__name__)
    config_objs = {'development': 'approot.config.DevConfig',
                   'production': 'approot.config.ProdConfig',
                   'test': 'approot.config.TestConfig'}
    app.config.from_object(config_objs[config])

    # Blueprints
    app.register_blueprint(bp_core)
    app.register_blueprint(bp_apollo)

    # Database
    db.init_app(app)

    return app
