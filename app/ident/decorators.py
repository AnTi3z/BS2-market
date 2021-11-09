from flask import request

from app.models import Token


def ident_token_required(func):
    def wrapper(*args, **kwargs):
        ident_token = request.args.get('auth')
        token = Token.get_by_str(ident_token)
        ident_status = token.status.text if token else "INVALID"

        if ident_status != 'VALID':
            return f"Ident token {ident_status}", 401
        else:
            return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper
