from flask import Flask
from flask_peewee.db import Database
from app.poll_updates.update_waiter import UpdateWaiter
# from flask_marshmallow import Marshmallow
# from gevent.event import Event
from threading import Event

import config

db = None
vol_data = None
updates_waiter = UpdateWaiter(Event())
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

    from app.ident import bp as ident_bp
    app.register_blueprint(ident_bp)

    from app.market import bp as market_bp
    app.register_blueprint(market_bp)

    from app.poll_updates import bp as updates_bp
    app.register_blueprint(updates_bp)
    updates_waiter.init_app(app)

    return app
