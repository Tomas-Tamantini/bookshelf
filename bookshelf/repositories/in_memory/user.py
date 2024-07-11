from typing import Iterator, Optional

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

        user_with_id = User(id=len(self._users) + 1, **user.model_dump())
        self._users.append(user_with_id)
        return user_with_id

    def id_exists(self, user_id: int) -> bool:
        return any(user.id == user_id for user in self._users)

    def _name_changed(self, user_id: int, user: UserCore) -> bool:
        old_user = self.get_by_id(user_id)
        return old_user.username != user.username

    def _email_changed(self, user_id: int, user: UserCore) -> bool:
        old_user = self.get_by_id(user_id)
        return old_user.email != user.email

    def update(self, user_id: int, user: UserCore) -> User:
        conflicting_fields = list(self._conflicting_fields(user))
        if self._name_changed(user_id, user) and "username" in conflicting_fields:
            raise ConflictError("username")
        if self._email_changed(user_id, user) and "email" in conflicting_fields:
            raise ConflictError("email")
        updated = User(id=user_id, **user.model_dump())
        self._users = [updated if user.id == user_id else user for user in self._users]
        return updated

    def get_by_id(self, user_id: int) -> Optional[User]:
        return next((user for user in self._users if user.id == user_id), None)

    def delete(self, user_id: int) -> None:
        self._users = [user for user in self._users if user.id != user_id]
