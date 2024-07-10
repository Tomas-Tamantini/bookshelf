from http import HTTPStatus

from fastapi import APIRouter

from bookshelf.api.dependencies import T_UserRepository
from bookshelf.api.dto import CreateUserRequest, UserResponse

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.post(
    "/", status_code=HTTPStatus.CREATED.value, response_model=UserResponse
)
def create_user(user: CreateUserRequest, user_repository: T_UserRepository):
    return user_repository.add(user)
