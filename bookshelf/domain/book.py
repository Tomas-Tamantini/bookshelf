from pydantic import BaseModel, ConfigDict


class BookCore(BaseModel):
    model_config = ConfigDict(frozen=True)

    year: int
    title: str
    author_id: int


class Book(BookCore):
    id: int
