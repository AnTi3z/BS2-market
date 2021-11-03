from flask import Flask
from flask_peewee.db import Database
# from flask_marshmallow import Marshmallow


import config

db = None
vol_data = None
# ma = Marshmallow()


def create_app(config_class=config.DevConfig):
    global db, vol_data

    app = Flask(__name__)
    app.config.from_object(config_class)

    app.logger.setLevel(app.config.get('LOG_LEVEL'))

    db = Database(app)
    # ma.init_app(app)

    from app.market.cached_dataset import VolDataset
    vol_data = VolDataset()

    from app.ident import views
    from app.market import views
    from app.poll_updates import views

    return app
