from pydantic import BaseModel
from bookshelf.domain.author import AuthorCore


class CreateAuthorRequest(AuthorCore):
    pass
