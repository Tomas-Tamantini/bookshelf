from typing import Iterator, Optional

from bookshelf.domain.user import User, UserCore
from bookshelf.repositories.dto import (
    GetUsersDBQueryParameters,
    RepositoryPaginatedResponse,
)
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

    def add(self, element: UserCore) -> User:
        for field in self._conflicting_fields(element):
            raise ConflictError(field)

        user = User(id=len(self._users) + 1, **element.model_dump())
        self._users.append(user)
        return user

    def id_exists(self, element_id: int) -> bool:
        return any(user.id == element_id for user in self._users)

    def _name_changed(self, user_id: int, user: UserCore) -> bool:
        old_user = self.get_by_id(user_id)
        return old_user.username != user.username

    def _email_changed(self, user_id: int, user: UserCore) -> bool:
        old_user = self.get_by_id(user_id)
        return old_user.email != user.email

    def update(self, element_id: int, element: UserCore) -> User:
        conflicting_fields = list(self._conflicting_fields(element))
        if self._name_changed(element_id, element) and "username" in conflicting_fields:
            raise ConflictError("username")
        if self._email_changed(element_id, element) and "email" in conflicting_fields:
            raise ConflictError("email")
        updated = User(id=element_id, **element.model_dump())
        self._users = [
            updated if user.id == element_id else user for user in self._users
        ]
        return updated

    def get_by_id(self, element_id: int) -> Optional[User]:
        return next((user for user in self._users if user.id == element_id), None)

    def delete(self, element_id: int) -> None:
        self._users = [user for user in self._users if user.id != element_id]

    def get_filtered(
        self, query_parameters: GetUsersDBQueryParameters
    ) -> RepositoryPaginatedResponse[User]:
        filtered = [
            user for user in self._users if self._matches(user, query_parameters)
        ]
        start_idx = query_parameters.offset
        end_idx = start_idx + query_parameters.limit
        return RepositoryPaginatedResponse[User](
            elements=filtered[start_idx:end_idx], total=len(filtered)
        )

    def _matches(self, user: User, query_parameters: GetUsersDBQueryParameters) -> bool:
        if (
            query_parameters.username is not None
            and query_parameters.username not in user.username
        ):
            return False
        if (
            query_parameters.email is not None
            and query_parameters.email not in user.email
        ):
            return False
        return True
