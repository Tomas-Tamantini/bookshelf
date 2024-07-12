from pydantic import BaseModel

from bookshelf.domain.author import Author


class GetAuthorsDBQueryParameters(BaseModel):
    name: str
    limit: int
    offset: int
