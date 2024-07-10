from typing import Annotated

from fastapi import Depends

from bookshelf.api.authentication import PasswordHandler, PwdHandler


def get_password_handler() -> PasswordHandler:
    return PwdHandler()


T_PasswordHandler = Annotated[PasswordHandler, Depends(get_password_handler)]
