from http import HTTPStatus

from fastapi import APIRouter

from bookshelf.api.dto import CreateAuthorRequest

authors_router = APIRouter(prefix="/authors", tags=["authors"])


@authors_router.post("/", status_code=HTTPStatus.OK.value)
def create_author(author: CreateAuthorRequest):
    return {}
