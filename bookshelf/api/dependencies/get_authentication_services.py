from typing import Annotated

from fastapi import Depends
from pwdlib import PasswordHash

from bookshelf.api.authentication import JWTHandler, PasswordHandler, PyJWTHandler
from bookshelf.settings import Settings


def get_password_handler() -> PasswordHandler:
    return PasswordHash.recommended()


T_PasswordHandler = Annotated[PasswordHandler, Depends(get_password_handler)]


def get_jwt_handler() -> JWTHandler:
    return PyJWTHandler(
        secret=Settings().JWT_SECRET,
        algorithm=Settings().JWT_ALGORITHM,
        access_token_expiration_minutes=Settings().ACCESS_TOKEN_EXPIRATION_MINUTES,
        refresh_token_expiration_minutes=Settings().REFRESH_TOKEN_EXPIRATION_MINUTES,
    )


T_JWTHandler = Annotated[JWTHandler, Depends(get_jwt_handler)]
