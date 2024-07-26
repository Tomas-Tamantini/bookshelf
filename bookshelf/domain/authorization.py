from typing import Protocol

from bookshelf.domain.user import User


class Authorization(Protocol):
    def has_permission(self, user: User) -> bool:
        pass


class UpdateUserAuthorization:
    def __init__(self, target_id: int) -> None:
        self._target_id = target_id

    def has_permission(self, user: User) -> bool:
        return user.id == self._target_id


class DeleteUserAuthorization(UpdateUserAuthorization):
    pass
