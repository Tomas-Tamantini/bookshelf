from typing import Optional, Protocol

from bookshelf.domain.user import User, UserCore
from bookshelf.repositories.dto import GetUsersDBQueryParameters, GetUsersDBResponse


class UserRepository(Protocol):
    def add(self, user: UserCore) -> User: ...

    def id_exists(self, user_id: int) -> bool: ...

    def update(self, user_id: int, user: UserCore) -> User: ...

    def get_by_id(self, user_id: int) -> Optional[User]: ...

    def delete(self, user_id: int) -> None: ...

    def get_filtered(
        self, query_parameters: GetUsersDBQueryParameters
    ) -> GetUsersDBResponse: ...
