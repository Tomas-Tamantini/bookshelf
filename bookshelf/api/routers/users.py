from http import HTTPStatus

from fastapi import APIRouter

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
    return user_repository.add(
        user.sanitized().hash_password(password_handler.hash_password)
    )
