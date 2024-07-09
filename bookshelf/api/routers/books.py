from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from bookshelf.api.dependencies import T_AuthorRepository, T_BookRepository
from bookshelf.api.dto import CreateBookRequest
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
