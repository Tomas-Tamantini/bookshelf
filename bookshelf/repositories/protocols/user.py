from typing import Optional, Protocol

from bookshelf.domain.user import User, UserCore
from bookshelf.repositories.dto import UserFilters

from .repository import Repository


class UserRepository(Repository[UserCore, User, UserFilters], Protocol):
    def get_by_email(self, email: str) -> Optional[User]: ...
