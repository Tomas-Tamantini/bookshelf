from typing import Optional

from pydantic import BaseModel


class GetBooksDBQueryParameters(BaseModel):
    limit: int
    offset: int
    title: Optional[str]
    author_id: Optional[int]
    year: Optional[int]
