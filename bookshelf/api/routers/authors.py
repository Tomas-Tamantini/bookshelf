from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from bookshelf.api.dependencies import T_AuthorRepository
from bookshelf.api.dto import CreateAuthorRequest
from bookshelf.domain.author import Author

authors_router = APIRouter(prefix="/authors", tags=["authors"])


@authors_router.post("/", status_code=HTTPStatus.OK.value, response_model=Author)
def create_author(author: CreateAuthorRequest, author_repository: T_AuthorRepository):
    if author_repository.name_exists(author.name):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Author with this name already exists",
        )
    else:
        return author_repository.add(author.sanitized())
