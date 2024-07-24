from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from bookshelf.api.dependencies import T_AuthorRepository, T_CurrentUser
from bookshelf.api.dto import (
    CreateAuthorRequest,
    GetAuthorsQueryParameters,
    GetAuthorsResponse,
    Message,
)
from bookshelf.api.exceptions import HttpConflictError
from bookshelf.domain.author import Author
from bookshelf.repositories.exceptions import ConflictError

authors_router = APIRouter(prefix="/authors", tags=["authors"])


@authors_router.post("/", status_code=HTTPStatus.CREATED.value, response_model=Author)
def create_author(
    author: CreateAuthorRequest,
    author_repository: T_AuthorRepository,
    current_user: T_CurrentUser,
):
    try:
        return author_repository.add(author.sanitized())
    except ConflictError as e:
        raise HttpConflictError("Author", e.field) from e


@authors_router.delete(
    "/{author_id}", status_code=HTTPStatus.OK.value, response_model=Message
)
def delete_author(
    author_id: int, author_repository: T_AuthorRepository, current_user: T_CurrentUser
):
    if not author_repository.id_exists(author_id):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    else:
        author_repository.delete(author_id)
        return Message(message="Author deleted")


@authors_router.put(
    "/{author_id}", status_code=HTTPStatus.OK.value, response_model=Author
)
def update_author(
    author_id: int,
    author: CreateAuthorRequest,
    author_repository: T_AuthorRepository,
    current_user: T_CurrentUser,
):
    if not author_repository.id_exists(author_id):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    else:
        try:
            return author_repository.update(author_id, author.sanitized())
        except ConflictError as e:
            raise HttpConflictError("Author", e.field) from e


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
    pagination = query_parameters.pagination()
    filters = query_parameters.filters()
    db_response = author_repository.get_filtered(pagination, filters)
    return GetAuthorsResponse(
        authors=db_response.elements,
        total=db_response.total,
        limit=pagination.limit,
        offset=pagination.offset,
        name=filters.name,
    )
