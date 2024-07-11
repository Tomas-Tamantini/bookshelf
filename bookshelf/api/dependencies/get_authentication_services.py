from typing import Annotated

from fastapi import Depends
from pwdlib import PasswordHash

from bookshelf.api.authentication import PasswordHandler


def get_password_handler() -> PasswordHandler:
    return PasswordHash.recommended()


T_PasswordHandler = Annotated[PasswordHandler, Depends(get_password_handler)]
