from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from bookshelf.api.dependencies import T_PasswordHandler, T_UserRepository
from bookshelf.api.dto import CreateUserRequest, UserResponse

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.post(
    "/", status_code=HTTPStatus.CREATED.value, response_model=UserResponse
)
def create_user(
    user: CreateUserRequest,
    user_repository: T_UserRepository,
    password_handler: T_PasswordHandler,
):
    if user_repository.username_exists(user.username):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="User with this username already exists",
        )
    elif user_repository.email_exists(user.email):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="User with this email already exists",
        )
    else:
        return user_repository.add(
            user.sanitized().hash_password(password_handler.hash_password)
        )
