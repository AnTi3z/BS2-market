#!/usr/local/www/cgi-bin/bs_market/venv/bin/python
import json
from datetime import datetime, date
import logging

import uwsgi
import gevent
import gevent.event
from flask import Flask, request, jsonify

from data_getter import get_update, get_raw_data, get_grouped_data
from auth import check_auth, get_auth, auth_info_to_dict
from market_avg import VolDataset
from db_models import db


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
# app.debug = True

app.logger.setLevel(logging.DEBUG)

_MAX_LIMIT_ = 50000
_MAX_GROUP_ = 2678400  # 60*60*24*31 (1 month)
_RES_LIST = ('wood', 'stone', 'food', 'horse')
vol_data = VolDataset()
newdata_event = gevent.event.Event()


# def debug_event(num):
#    app.logger.debug(f"Catched signal:{num} in {gevent.getcurrent()}")
#    newdata_event.set()

uwsgi.add_file_monitor(2, "/tmp/bs_market_updates")
uwsgi.register_signal(2, "", lambda _: newdata_event.set())
# uwsgi.register_signal(2, "workers", debug_event)


def clamp(n, minn, maxn):
    return min(max(minn, n), maxn)


def auth_token_required(func):
    def wrapper(*args, **kwargs):
        auth_token = request.args.get('auth')
        auth_status = check_auth(auth_token)

        if auth_status != 'VALID':
            return f"Auth token {auth_status}", 401
        else:
            return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


@app.before_request
def connect_db():
    db.connect()


@app.teardown_request
def close_db(exception=None):
    if not db.is_closed():
        db.close()


@app.route('/api/auth')
def handle_auth():
    token = request.args.get('token') or request.args.get('auth')
    auth_info = get_auth(token)
    if auth_info is None:
        return "Auth token INVALID", 404

    result = auth_info_to_dict(auth_info)
    return result


@app.route('/api/market')
@auth_token_required
def handle_market():
    res = request.args.get('res')
    if res not in ('wood', 'stone', 'food', 'horse'):
        return "Queried resource name error", 400

    limit = clamp(request.args.get('limit', default=_MAX_LIMIT_, type=int), 1, _MAX_LIMIT_)
    if request.args.get('from') == '0':
        from_datetime = datetime.min
    else:
        from_datetime = request.args.get('from', type=datetime.fromisoformat)
    group = request.args.get('group', type=int)

    if group:
        group = clamp(group, 1, _MAX_GROUP_)
        result = get_grouped_data(res, limit, group, from_datetime)
    else:
        result = get_raw_data(res, limit, from_datetime)

    return jsonify(result)


@app.route('/api/market_avg')
@auth_token_required
def handle_market_avg():
    res = request.args.get('res')
    if res not in _RES_LIST:
        return "Queried resource name error", 400

    day = request.args.get('day', type=date.fromisoformat)
    result = vol_data.get_limit(res, day)
    return jsonify(result)


@app.route('/api/<res>/raw')
@auth_token_required
def handle_raw(res):
    if res not in _RES_LIST:
        return "Queried resource name not found", 404

    limit = clamp(request.args.get('limit', default=_MAX_LIMIT_, type=int), 1, _MAX_LIMIT_)
    if request.args.get('from') == '0':
        from_datetime = datetime.min
    else:
        from_datetime = request.args.get('from', type=datetime.fromisoformat)

    result = get_raw_data(res, limit, from_datetime)
    return {res: result}


@app.route('/api/<res>/grouped')
@auth_token_required
def handle_grouped(res):
    if res not in _RES_LIST:
        return "Queried resource name not found", 404

    limit = clamp(request.args.get('limit', default=_MAX_LIMIT_, type=int), 1, _MAX_LIMIT_)
    group = clamp(request.args.get('group', default=60, type=int), 5, _MAX_GROUP_)
    if request.args.get('from') == '0':
        from_datetime = datetime.min
    else:
        from_datetime = request.args.get('from', type=datetime.fromisoformat)

    result = get_grouped_data(res, limit, group, from_datetime)
    return {res: result}


@app.route('/api/<res>/average')
@auth_token_required
def handle_average(res):
    if res not in _RES_LIST:
        return "Queried resource name not found", 404

    day = request.args.get('day', type=date.fromisoformat)
    result = vol_data.get_limit(res, day)
    return {res: result}


@app.route('/api/updates')
@auth_token_required
def handle_updates():
    if request.args.get('from') == '0':
        from_datetime = datetime.min
    else:
        from_datetime = request.args.get('from', type=datetime.fromisoformat)

    result = None
    # try to get new records from db
    if from_datetime:
        result = get_update(from_datetime)

    # if no new data in db then wait for new data
    if not result:
        db.close()
        result = update_wait()

    return result or ""


def update_wait():
    newdata_event.clear()
    app.logger.debug(f"newdata wait in {gevent.getcurrent()}")
    if newdata_event.wait(30.0):
        app.logger.debug(f"newdata catched in {gevent.getcurrent()}")
        with open("/tmp/bs_market_updates") as f:
            result = f.read()
        return json.loads(result, parse_float=lambda x: round(float(x), 3))
    else:
        app.logger.debug(f"newdata timeout in {gevent.getcurrent()}")
        return


if __name__ == "__main__":
    app.run()
