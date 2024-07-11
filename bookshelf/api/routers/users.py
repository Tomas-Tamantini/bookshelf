from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from bookshelf.api.dependencies import T_PasswordHandler, T_UserRepository
from bookshelf.api.dto import CreateUserRequest, Message, UserResponse
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


@users_router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, user_repository: T_UserRepository):
    user = user_repository.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return user


@users_router.delete(
    "/{user_id}", status_code=HTTPStatus.OK.value, response_model=Message
)
def delete_user(user_id: int, user_repository: T_UserRepository):
    if not user_repository.id_exists(user_id):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    else:
        user_repository.delete(user_id)
        return Message(message="User deleted")
