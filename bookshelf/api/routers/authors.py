from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from bookshelf.api.dependencies import T_AuthorRepository
from bookshelf.api.dto import (
    CreateAuthorRequest,
    GetAuthorsQueryParameters,
    GetAuthorsResponse,
    Message,
)
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


@authors_router.put(
    "/{author_id}", status_code=HTTPStatus.OK.value, response_model=Author
)
def update_author(
    author_id: int, author: CreateAuthorRequest, author_repository: T_AuthorRepository
):
    if not author_repository.id_exists(author_id):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    elif author_repository.name_exists(author.name):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Author with this name already exists",
        )
    else:
        return author_repository.update(author_id, author.sanitized())


@authors_router.get("/{author_id}", response_model=Author)
def get_author(author_id: int, author_repository: T_AuthorRepository):
    author = author_repository.get_by_id(author_id)
    if author is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return author


@authors_router.get("/", status_code=HTTPStatus.OK, response_model=GetAuthorsResponse)
def get_authors(
    author_repository: T_AuthorRepository,
    query_parameters: GetAuthorsQueryParameters = Depends(),
):
    db_response = author_repository.get_filtered(query_parameters.sanitized())
    return GetAuthorsResponse(
        limit=query_parameters.limit,
        offset=query_parameters.offset,
        **db_response.model_dump()
    )
