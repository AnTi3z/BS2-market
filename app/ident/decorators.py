from flask import request

from .services import check_ident


def ident_token_required(func):
    def wrapper(*args, **kwargs):
        ident_token = request.args.get('auth')
        ident_status = check_ident(ident_token)

        if ident_status != 'VALID':
            return f"Ident token {ident_status}", 401
        else:
            return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper
