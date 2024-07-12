from typing import Optional

from pydantic import BaseModel


class GetUsersDBQueryParameters(BaseModel):
    limit: int
    offset: int
    username: Optional[str]
    email: Optional[str]
