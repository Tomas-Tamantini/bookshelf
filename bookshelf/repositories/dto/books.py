from typing import Optional

from pydantic import BaseModel


class BookFilters(BaseModel):
    title: Optional[str]
    author_id: Optional[int]
    year: Optional[int]
