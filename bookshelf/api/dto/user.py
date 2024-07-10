from bookshelf.domain.user import UserPublicInformation


class CreateUserRequest(UserPublicInformation):
    password: str


class UserResponse(UserPublicInformation):
    id: int
