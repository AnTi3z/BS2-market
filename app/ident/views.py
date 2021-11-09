from flask import request

from bs_market import app
from app.models import Token


@app.route('/api/auth')
def handle_auth():
    token = request.args.get('token') or request.args.get('auth')
    ident_info = Token.get_by_str(token)
    if ident_info is None:
        return "Auth token INVALID", 404

    return ident_info.serialize()
