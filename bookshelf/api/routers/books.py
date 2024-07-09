from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from bookshelf.api.dependencies import T_BookRepository
from bookshelf.api.dto import CreateBookRequest
from bookshelf.domain.book import Book

books_router = APIRouter(prefix="/books", tags=["books"])


@books_router.post("/", status_code=HTTPStatus.CREATED.value, response_model=Book)
def create_book(book: CreateBookRequest, book_repository: T_BookRepository):
    if book_repository.title_exists(book.title):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Book with this title already exists",
        )
    else:
        return book_repository.add(book.sanitized())
