from typing import Iterator

from bookshelf.domain.user import User, UserCore
from bookshelf.repositories.exceptions import ConflictError


class InMemoryUserRepository:
    def __init__(self) -> None:
        self._users = []

    def _username_exists(self, username: str) -> bool:
        return any(user.username == username for user in self._users)

    def _email_exists(self, email: str) -> bool:
        return any(user.email == email for user in self._users)

    def _conflicting_fields(self, user: UserCore) -> Iterator[str]:
        if self._username_exists(user.username):
            yield "username"

        if self._email_exists(user.email):
            yield "email"

    def add(self, user: UserCore) -> User:
        for field in self._conflicting_fields(user):
            raise ConflictError(field)

        user = User(id=len(self._users) + 1, **user.model_dump())
        self._users.append(user)
        return user
