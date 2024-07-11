from typing import Annotated

from fastapi import Depends

from bookshelf.api.authentication import PasswordHandler
from pwdlib import PasswordHash


def get_password_handler() -> PasswordHandler:
    return PasswordHash.recommended()


T_PasswordHandler = Annotated[PasswordHandler, Depends(get_password_handler)]
