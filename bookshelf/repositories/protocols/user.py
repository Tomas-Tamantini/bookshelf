from typing import Optional, Protocol

from bookshelf.domain.user import User, UserCore
from bookshelf.repositories.dto import (
    PaginationParameters,
    RepositoryPaginatedResponse,
    UserFilters,
)


class UserRepository(Protocol):
    def add(self, element: UserCore) -> User: ...

    def id_exists(self, element_id: int) -> bool: ...

    def update(self, element_id: int, element: UserCore) -> User: ...

    def get_by_id(self, element_id: int) -> Optional[User]: ...

    def delete(self, element_id: int) -> None: ...

    def get_filtered(
        self, pagination: PaginationParameters, filters: UserFilters
    ) -> RepositoryPaginatedResponse[User]: ...
