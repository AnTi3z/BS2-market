from app.models import Token


def get_ident(ident_token: str) -> Token:
    token = Token.get_or_none(Token.token == ident_token)
    return token


def check_ident(ident_token: str) -> str:
    token = get_ident(ident_token)
    return token.status.text if token else "INVALID"
