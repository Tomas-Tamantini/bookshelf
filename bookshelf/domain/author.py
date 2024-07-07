from pydantic import BaseModel, ConfigDict


class AuthorCore(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str


class Author(AuthorCore):
    id: int
