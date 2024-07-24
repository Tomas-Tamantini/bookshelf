from typing import Annotated

from fastapi import Depends

from bookshelf.domain.user import User


async def get_current_user() -> User:
    raise NotImplementedError()


T_CurrentUser = Annotated[User, Depends(get_current_user)]
