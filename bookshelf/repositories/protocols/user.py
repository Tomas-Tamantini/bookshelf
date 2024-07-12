from typing import Protocol

from bookshelf.domain.user import User, UserCore
from bookshelf.repositories.dto import UserFilters

from .repository import Repository


class UserRepository(Repository[UserCore, User, UserFilters], Protocol):
    pass
