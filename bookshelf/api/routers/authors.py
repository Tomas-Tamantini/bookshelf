from http import HTTPStatus

from fastapi import APIRouter

from bookshelf.api.dto import CreateAuthorRequest
from bookshelf.domain.author import Author

authors_router = APIRouter(prefix="/authors", tags=["authors"])


@authors_router.post("/", status_code=HTTPStatus.OK.value, response_model=Author)
def create_author(author: CreateAuthorRequest):
    return Author(id=1, **author.model_dump())
