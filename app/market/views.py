from flask import jsonify

from app.market import bp, vol_data
from app.market.services import get_raw_data, get_grouped_data
from app.ident.decorators import ident_token_required
from app.argparser import *


@bp.route('/api/market')
@ident_token_required
def handle_market():
    res = get_res_arg()
    limit = get_limit_arg()
    from_datetime = get_datetime_arg()
    group = get_group_arg()

    if group:
        result = get_grouped_data(res, limit, group, from_datetime)
    else:
        result = get_raw_data(res, limit, from_datetime)

    return jsonify(result)


@bp.route('/api/market_avg')
@ident_token_required
def handle_market_avg():
    res = get_res_arg()
    day = get_day_arg()

    result = vol_data.get_limit(res, day)
    return jsonify(result)


@bp.route('/api/<res>/raw')
@ident_token_required
def handle_raw(res):
    check_res_arg(res)
    limit = get_limit_arg()
    from_datetime = get_datetime_arg()

    result = get_raw_data(res, limit, from_datetime)
    return {res: result}


@bp.route('/api/<res>/grouped')
@ident_token_required
def handle_grouped(res):
    check_res_arg(res)
    limit = get_limit_arg()
    from_datetime = get_datetime_arg()
    group = get_group_arg()

    result = get_grouped_data(res, limit, group, from_datetime)
    return {res: result}


@bp.route('/api/<res>/average')
@ident_token_required
def handle_average(res):
    check_res_arg(res)
    day = get_day_arg()

    result = vol_data.get_limit_arg(res, day)
    return {res: result}
