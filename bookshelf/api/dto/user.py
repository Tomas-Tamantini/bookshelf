from typing import Callable

from bookshelf.api.dto.sanitize import sanitize_name
from bookshelf.domain.user import UserCore, UserPublicInformation


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
