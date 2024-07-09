from http import HTTPStatus

from fastapi import APIRouter

from bookshelf.api.dependencies import T_BookRepository
from bookshelf.api.dto import CreateBookRequest
from bookshelf.domain.book import Book

books_router = APIRouter(prefix="/books", tags=["books"])


@books_router.post("/", status_code=HTTPStatus.CREATED.value, response_model=Book)
def create_book(book: CreateBookRequest, book_repository: T_BookRepository):
    return book_repository.add(book)
