from typing import Optional

from pydantic import BaseModel

from bookshelf.domain.user import User


class GetUsersDBQueryParameters(BaseModel):
    limit: int
    offset: int
    username: Optional[str]
    email: Optional[str]
