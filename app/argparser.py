from datetime import datetime, date
from flask import request, abort


_MAX_LIMIT_ = 50000
_MAX_GROUP_ = 2678400  # 60*60*24*31 (1 month)
_RES_LIST = ('wood', 'stone', 'food', 'horse')


def clamp(n, minn, maxn):
    return min(max(minn, n), maxn)


def get_res_arg():
    res = request.args.get('res')
    check_res_arg(res)
    return res


def check_res_arg(res):
    if res not in _RES_LIST:
        abort(404, "Queried resource name error")


def get_limit_arg():
    return clamp(request.args.get('limit', default=_MAX_LIMIT_, type=int), 1, _MAX_LIMIT_)


def get_group_arg():
    group = request.args.get('group', type=int)
    if group:
        group = clamp(group, 1, _MAX_GROUP_)
    return group


def get_datetime_arg():
    if request.args.get('from') == '0':
        from_datetime = datetime.min
    else:
        from_datetime = request.args.get('from', type=datetime.fromisoformat)
    return from_datetime


def get_day_arg():
    return request.args.get('day', type=date.fromisoformat)


def get_token_arg():
    return request.args.get('token') or request.args.get('auth')

