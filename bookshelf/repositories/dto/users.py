from typing import Optional

from pydantic import BaseModel


class UserFilters(BaseModel):
    username: Optional[str]
    email: Optional[str]
