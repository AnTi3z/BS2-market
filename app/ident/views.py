from flask import request

from bs_market import app
from .services import get_ident


@app.route('/api/auth')
def handle_auth():
    token = request.args.get('token') or request.args.get('auth')
    ident_info = get_ident(token)
    if ident_info is None:
        return "Auth token INVALID", 404

    return ident_info.serialize()
