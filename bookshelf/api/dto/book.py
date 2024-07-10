from typing import Optional

from pydantic import BaseModel, ConfigDict

from bookshelf.api.dto.sanitize import sanitize_name
from bookshelf.domain.book import Book, BookCore
from bookshelf.repositories.dto import GetBooksDBQueryParameters


class CreateBookRequest(BookCore):
    def sanitized(self) -> BookCore:
        return BookCore(
            title=sanitize_name(self.title),
            year=self.year,
            author_id=self.author_id,
        )


class PatchBookRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    year: Optional[int] = None
    title: Optional[str] = None
    author_id: Optional[int] = None

    def updated(self, existing_book: Book) -> BookCore:
        return BookCore(
            title=(
                sanitize_name(self.title)
                if self.title is not None
                else existing_book.title
            ),
            year=self.year if self.year is not None else existing_book.year,
            author_id=(
                self.author_id
                if self.author_id is not None
                else existing_book.author_id
            ),
        )


class GetBooksQueryParameters(BaseModel):
    limit: int = 20
    offset: int = 0
    title: Optional[str] = None
    author_id: Optional[int] = None
    year: Optional[int] = None

    def sanitized(self) -> GetBooksDBQueryParameters:
        return GetBooksDBQueryParameters(
            limit=self.limit,
            offset=self.offset,
            title=(sanitize_name(self.title) if self.title is not None else self.title),
            author_id=self.author_id,
            year=self.year,
        )


class GetBooksResponse(BaseModel):
    books: list[Book]
    total: int
    limit: int
    offset: int
    title: Optional[str]
    author_id: Optional[int]
    year: Optional[int]
