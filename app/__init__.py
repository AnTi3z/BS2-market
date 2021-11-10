from flask import Flask
from flask_peewee.db import Database
# from flask_marshmallow import Marshmallow

import config

db = None
# ma = Marshmallow()


def create_app(config_class=config.DevConfig):
    global db

    app = Flask(__name__)
    app.config.from_object(config_class)

    app.logger.setLevel(app.config.get('LOG_LEVEL'))

    db = Database(app)
    # ma.init_app(app)

    from app.ident import bp as ident_bp
    app.register_blueprint(ident_bp)

    from app.market import bp as market_bp
    app.register_blueprint(market_bp)

    from app.poll_updates import bp as updates_bp
    app.register_blueprint(updates_bp)

    return app
