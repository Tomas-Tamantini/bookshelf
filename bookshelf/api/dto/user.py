from bookshelf.api.dto.sanitize import sanitize_name
from bookshelf.domain.user import UserPublicInformation


class CreateUserRequest(UserPublicInformation):
    password: str

    def sanitized(self) -> "CreateUserRequest":
        return CreateUserRequest(
            email=self.email,
            username=sanitize_name(self.username),
            password=self.password,
        )


class UserResponse(UserPublicInformation):
    id: int
