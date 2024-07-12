from typing import Callable, Optional

from pydantic import BaseModel

from bookshelf.api.dto.sanitize import sanitize_name
from bookshelf.domain.user import UserCore, UserPublicInformation
from bookshelf.repositories.dto import GetUsersDBQueryParameters


class CreateUserRequest(UserPublicInformation):
    password: str

    def sanitized(self) -> "CreateUserRequest":
        return CreateUserRequest(
            email=self.email,
            username=sanitize_name(self.username),
            password=self.password,
        )

    def hash_password(self, hash_method: Callable[[str], str]) -> UserCore:
        return UserCore(
            email=self.email,
            username=self.username,
            hashed_password=hash_method(self.password),
        )


class UserResponse(UserPublicInformation):
    id: int


class GetUsersQueryParameters(BaseModel):
    limit: int = 20
    offset: int = 0
    username: Optional[str] = None
    email: Optional[str] = None

    def sanitized(self) -> GetUsersDBQueryParameters:
        return GetUsersDBQueryParameters(
            limit=self.limit,
            offset=self.offset,
            username=(
                sanitize_name(self.username) if self.username is not None else None
            ),
            email=self.email.strip().lower() if self.email is not None else None,
        )


class GetUsersResponse(BaseModel):
    users: list[UserResponse]
    total: int
    limit: int
    offset: int
    username: Optional[str]
    email: Optional[str]
