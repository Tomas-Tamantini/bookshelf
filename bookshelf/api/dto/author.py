from pydantic import BaseModel

from bookshelf.api.dto.sanitize import sanitize_name
from bookshelf.domain.author import Author, AuthorCore
from bookshelf.repositories.dto import GetAuthorsDBQueryParameters


class CreateAuthorRequest(AuthorCore):
    def sanitized(self) -> AuthorCore:
        return AuthorCore(name=sanitize_name(self.name))


class GetAuthorsQueryParameters(BaseModel):
    name: str
    limit: int = 20
    offset: int = 0

    def sanitized(self) -> GetAuthorsDBQueryParameters:
        return GetAuthorsDBQueryParameters(
            name=sanitize_name(self.name), limit=self.limit, offset=self.offset
        )


class GetAuthorsResponse(BaseModel):
    authors: list[Author]
    total: int
    limit: int
    offset: int
