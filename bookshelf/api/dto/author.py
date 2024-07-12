from typing import Optional

from pydantic import BaseModel

from bookshelf.api.dto.sanitize import sanitize_name
from bookshelf.domain.author import Author, AuthorCore
from bookshelf.repositories.dto import AuthorFilters, PaginationParameters


class CreateAuthorRequest(AuthorCore):
    def sanitized(self) -> AuthorCore:
        return AuthorCore(name=sanitize_name(self.name))


class GetAuthorsQueryParameters(BaseModel):
    name: str
    limit: int = 20
    offset: int = 0

    def filters(self) -> AuthorFilters:
        return AuthorFilters(name=sanitize_name(self.name))

    def pagination(self) -> PaginationParameters:
        return PaginationParameters(limit=self.limit, offset=self.offset)


class GetAuthorsResponse(BaseModel):
    authors: list[Author]
    total: int
    limit: int
    offset: int
    name: Optional[str]
