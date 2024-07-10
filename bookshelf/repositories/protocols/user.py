from typing import Protocol

from bookshelf.domain.user import User, UserCore


class UserRepository(Protocol):
    def add(self, user: UserCore) -> User: ...

    def username_exists(self, username: str) -> bool: ...

    def email_exists(self, email: str) -> bool: ...
