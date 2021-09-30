from typing import Dict

from playhouse.shortcuts import model_to_dict

from db_models import Token


def get_auth(auth_token: str) -> Token:
    token = Token.get_or_none(Token.token == auth_token)
    return token


def check_auth(auth_token: str) -> str:
    token = get_auth(auth_token)
    return token.status.text if token else "INVALID"


def auth_info_to_dict(auth_info: Token) -> Dict[str, any]:
    return {'token': auth_info.token,
            'status': auth_info.status.text,
            'created': auth_info.created.isoformat(),
            'status_updated': auth_info.modified.isoformat(),
            'user': model_to_dict(auth_info.user)}
