from typing import Annotated

from fastapi import Depends

from bookshelf.domain.authorization import (
    Authorization,
    DeleteUserAuthorization,
    UpdateUserAuthorization,
)


def get_delete_user_authorization(user_id: int) -> DeleteUserAuthorization:
    return DeleteUserAuthorization(target_id=user_id)


def get_update_user_authorization(user_id: int) -> UpdateUserAuthorization:
    return UpdateUserAuthorization(target_id=user_id)


T_DeleteUserAuthorization = Annotated[
    Authorization, Depends(get_delete_user_authorization)
]

T_UpdateUserAuthorization = Annotated[
    Authorization, Depends(get_update_user_authorization)
]
