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


class InMemoryUserRepository(InMemoryRepository[UserCore, User, UserFilters]):
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

    def _matches(self, element: User, filters: UserFilters) -> bool:
        if filters.username is not None and filters.username not in element.username:
            return False
        if filters.email is not None and filters.email not in element.email:
            return False
        return True
