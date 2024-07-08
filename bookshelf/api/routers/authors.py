from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from bookshelf.api.dependencies import T_AuthorRepository
from bookshelf.api.dto import CreateAuthorRequest, Message
from bookshelf.domain.author import Author

authors_router = APIRouter(prefix="/authors", tags=["authors"])


@authors_router.post("/", status_code=HTTPStatus.CREATED.value, response_model=Author)
def create_author(author: CreateAuthorRequest, author_repository: T_AuthorRepository):
    if author_repository.name_exists(author.name):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Author with this name already exists",
        )
    else:
        return author_repository.add(author.sanitized())


@authors_router.delete(
    "/{author_id}", status_code=HTTPStatus.OK.value, response_model=Message
)
def delete_author(author_id: int, author_repository: T_AuthorRepository):
    if not author_repository.id_exists(author_id):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    else:
        author_repository.delete(author_id)
        return Message(message="Author deleted")
