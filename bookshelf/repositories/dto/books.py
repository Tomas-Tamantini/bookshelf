from typing import Optional

from pydantic import BaseModel

from bookshelf.domain.book import Book


class GetBooksDBQueryParameters(BaseModel):
    limit: int
    offset: int
    title: Optional[str]
    author_id: Optional[int]
    year: Optional[int]
