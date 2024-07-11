from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from bookshelf.api.dependencies import T_PasswordHandler, T_UserRepository
from bookshelf.api.dto import CreateUserRequest, UserResponse
from bookshelf.api.exceptions import HttpConflictError
from bookshelf.repositories.exceptions import ConflictError

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.post(
    "/", status_code=HTTPStatus.CREATED.value, response_model=UserResponse
)
def create_user(
    user: CreateUserRequest,
    user_repository: T_UserRepository,
    password_handler: T_PasswordHandler,
):
    try:
        return user_repository.add(
            user.sanitized().hash_password(password_handler.hash)
        )
    except ConflictError as e:
        raise HttpConflictError("User", e.field) from e


@users_router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user: CreateUserRequest,
    user_repository: T_UserRepository,
    password_handler: T_PasswordHandler,
):
    if not user_repository.id_exists(user_id):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    try:
        return user_repository.update(
            user_id, user.sanitized().hash_password(password_handler.hash)
        )
    except ConflictError as e:
        raise HttpConflictError("User", e.field) from e
