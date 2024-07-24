from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from bookshelf.api.dependencies import (
    T_AuthorRepository,
    T_BookRepository,
    T_CurrentUser,
)
from bookshelf.api.dto import (
    CreateBookRequest,
    GetBooksQueryParameters,
    GetBooksResponse,
    PatchBookRequest,
)
from bookshelf.api.exceptions import HttpConflictError
from bookshelf.domain.book import Book
from bookshelf.repositories.exceptions import ConflictError

books_router = APIRouter(prefix="/books", tags=["books"])


@books_router.post("/", status_code=HTTPStatus.CREATED.value, response_model=Book)
def create_book(
    book: CreateBookRequest,
    book_repository: T_BookRepository,
    author_repository: T_AuthorRepository,
    current_user: T_CurrentUser,
):
    if not author_repository.id_exists(book.author_id):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Author with this ID does not exist",
        )
    else:
        try:
            return book_repository.add(book.sanitized())
        except ConflictError as e:
            raise HttpConflictError("Book", e.field) from e


@books_router.delete("/{book_id}", status_code=HTTPStatus.OK.value)
def delete_book(
    book_id: int, book_repository: T_BookRepository, current_user: T_CurrentUser
):
    if not book_repository.id_exists(book_id):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    else:
        book_repository.delete(book_id)
        return {"message": "Book deleted"}


@books_router.patch("/{book_id}", response_model=Book)
def update_book(
    book_id: int,
    book: PatchBookRequest,
    book_repository: T_BookRepository,
    author_repository: T_AuthorRepository,
    current_user: T_CurrentUser,
):
    if book.author_id is not None and not author_repository.id_exists(book.author_id):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Author with this ID does not exist",
        )
    else:
        if (existing_book := book_repository.get_by_id(book_id)) is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
        else:
            try:
                return book_repository.update(book_id, book.updated(existing_book))
            except ConflictError as e:
                raise HttpConflictError("Book", e.field) from e


@books_router.get("/{book_id}", response_model=Book)
def get_book(book_id: int, book_repository: T_BookRepository):
    book = book_repository.get_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    else:
        return book


@books_router.get("/", status_code=HTTPStatus.OK, response_model=GetBooksResponse)
def get_books(
    book_repository: T_BookRepository,
    query_parameters: GetBooksQueryParameters = Depends(),
):
    pagination = query_parameters.pagination()
    filters = query_parameters.filters()
    db_response = book_repository.get_filtered(pagination, filters)
    return GetBooksResponse(
        books=db_response.elements,
        total=db_response.total,
        limit=pagination.limit,
        offset=pagination.offset,
        title=filters.title,
        author_id=filters.author_id,
        year=filters.year,
    )
