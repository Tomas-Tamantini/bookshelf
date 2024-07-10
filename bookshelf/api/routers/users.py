from http import HTTPStatus

from fastapi import APIRouter

from bookshelf.api.dto import CreateUserRequest

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.post("/", status_code=HTTPStatus.CREATED.value)
def create_user(user: CreateUserRequest):
    pass
