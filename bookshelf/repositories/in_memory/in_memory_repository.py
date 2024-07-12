from abc import ABC, abstractmethod
from bookshelf.repositories.exceptions import ConflictError
from typing import Iterator, Optional, Any, Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class RepositoryField[T, TWithId]:
    name: str
    value: Callable[[T | TWithId], Any]


class InMemoryRepository[T, TWithId](ABC):
    def __init__(self, unique_fields: list[RepositoryField[T, TWithId]]) -> None:
        super().__init__()
        self._elements = []
        self._unique_fields = unique_fields

    @abstractmethod
    def _put_id(self, element: T, element_id: int) -> TWithId:
        raise NotImplementedError("Abstract method")

    def _field_is_duplicate(
        self, element: T, field: RepositoryField[T, TWithId]
    ) -> bool:
        return any(
            field.value(element) == field.value(existing) for existing in self._elements
        )

    def _field_changed(
        self, element_id: int, new_element: T, field: RepositoryField[T, TWithId]
    ) -> bool:
        old_element = self.get_by_id(element_id)
        return field.value(old_element) != field.value(new_element)

    def _conflicting_fields(self, element: T) -> Iterator[RepositoryField[T, TWithId]]:
        for field in self._unique_fields:
            if self._field_is_duplicate(element, field):
                yield field

    @property
    def _next_id(self) -> int:
        return len(self._elements) + 1

    @abstractmethod
    def _get_id(self, element: TWithId) -> int:
        raise NotImplementedError("Abstract method")

    def add(self, element: T) -> TWithId:
        for field in self._conflicting_fields(element):
            raise ConflictError(field.name)
        element_with_id = self._put_id(element, self._next_id)
        self._elements.append(element_with_id)
        return element_with_id

    def id_exists(self, element_id: int) -> bool:
        return any(self._get_id(element) == element_id for element in self._elements)

    def get_by_id(self, element_id: int) -> Optional[TWithId]:
        return next(
            (
                element
                for element in self._elements
                if self._get_id(element) == element_id
            ),
            None,
        )

    def delete(self, element_id: int) -> None:
        self._elements = [
            element for element in self._elements if self._get_id(element) != element_id
        ]

    def update(self, element_id: int, element: T) -> TWithId:
        for field in self._conflicting_fields(element):
            if self._field_changed(element_id, element, field):
                raise ConflictError(field.name)
        updated = self._put_id(element, element_id)
        self._elements = [updated if e.id == element_id else e for e in self._elements]
        return updated
