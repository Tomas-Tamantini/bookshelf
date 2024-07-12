from pydantic import BaseModel


class AuthorsFilter(BaseModel):
    name: str
