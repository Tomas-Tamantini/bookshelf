from pydantic import BaseModel


class AuthorFilters(BaseModel):
    name: str
