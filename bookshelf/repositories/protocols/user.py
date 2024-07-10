from typing import Protocol

from bookshelf.domain.user import User, UserCore


class UserRepository(Protocol):
    def add(self, user: UserCore) -> User: ...
