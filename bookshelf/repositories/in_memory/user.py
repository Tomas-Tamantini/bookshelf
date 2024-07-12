from bookshelf.domain.user import User, UserCore
from bookshelf.repositories.dto import (
    PaginationParameters,
    RepositoryPaginatedResponse,
    UserFilters,
)
from bookshelf.repositories.in_memory.in_memory_repository import (
    InMemoryRepository,
    RepositoryField,
)


class InMemoryUserRepository(InMemoryRepository[UserCore, User]):
    def __init__(self) -> None:
        unique_fields = [
            RepositoryField("username", lambda user: user.username),
            RepositoryField("email", lambda user: user.email),
        ]
        super().__init__(unique_fields)

    def _put_id(self, element: UserCore, element_id: int) -> User:
        return User(id=element_id, **element.model_dump())

    def _get_id(self, element: User) -> int:
        return element.id

    def get_filtered(
        self, pagination: PaginationParameters, filters: UserFilters
    ) -> RepositoryPaginatedResponse[User]:
        filtered = [user for user in self._elements if self._matches(user, filters)]
        start_idx = pagination.offset
        end_idx = start_idx + pagination.limit
        return RepositoryPaginatedResponse[User](
            elements=filtered[start_idx:end_idx], total=len(filtered)
        )

    def _matches(self, user: User, filters: UserFilters) -> bool:
        if filters.username is not None and filters.username not in user.username:
            return False
        if filters.email is not None and filters.email not in user.email:
            return False
        return True
