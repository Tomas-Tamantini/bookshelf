from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from bookshelf.api.dependencies import T_AuthorRepository, T_BookRepository
from bookshelf.api.dto import (
    CreateBookRequest,
    GetBooksQueryParameters,
    GetBooksResponse,
    PatchBookRequest,
)
from bookshelf.domain.book import Book

books_router = APIRouter(prefix="/books", tags=["books"])


@books_router.post("/", status_code=HTTPStatus.CREATED.value, response_model=Book)
def create_book(
    book: CreateBookRequest,
    book_repository: T_BookRepository,
    author_repository: T_AuthorRepository,
):
    if book_repository.title_exists(book.title):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Book with this title already exists",
        )
    elif not author_repository.id_exists(book.author_id):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Author with this ID does not exist",
        )
    else:
        return book_repository.add(book.sanitized())


@books_router.delete("/{book_id}", status_code=HTTPStatus.OK.value)
def delete_book(book_id: int, book_repository: T_BookRepository):
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
            return book_repository.update(book_id, book.updated(existing_book))


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
    db_query_parameters = query_parameters.sanitized()
    db_response = book_repository.get_filtered(db_query_parameters)
    return GetBooksResponse(
        limit=db_query_parameters.limit,
        offset=db_query_parameters.offset,
        title=db_query_parameters.title,
        author_id=db_query_parameters.author_id,
        year=db_query_parameters.year,
        **db_response.model_dump(),
    )
