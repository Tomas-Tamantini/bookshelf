from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Iterator, Optional

from bookshelf.repositories.dto import PaginationParameters, RepositoryPaginatedResponse
from bookshelf.repositories.exceptions import ConflictError


@dataclass(frozen=True)
class RepositoryField[T, TWithId]:
    name: str
    value: Callable[[T | TWithId], Any]


class InMemoryRepository[Element, ElementWithId, Filters](ABC):
    def __init__(
        self, unique_fields: list[RepositoryField[Element, ElementWithId]]
    ) -> None:
        super().__init__()
        self._elements = []
        self._unique_fields = unique_fields

    @abstractmethod
    def _put_id(self, element: Element, element_id: int) -> ElementWithId:
        raise NotImplementedError("Abstract method")

    @abstractmethod
    def _get_id(self, element: ElementWithId) -> int:
        raise NotImplementedError("Abstract method")

    @abstractmethod
    def _matches(self, element: ElementWithId, filters: Filters) -> bool:
        raise NotImplementedError("Abstract method")

    def _field_is_duplicate(
        self, element: Element, field: RepositoryField[Element, ElementWithId]
    ) -> bool:
        return any(
            field.value(element) == field.value(existing) for existing in self._elements
        )

    def _field_changed(
        self,
        element_id: int,
        new_element: Element,
        field: RepositoryField[Element, ElementWithId],
    ) -> bool:
        old_element = self.get_by_id(element_id)
        return field.value(old_element) != field.value(new_element)

    def _conflicting_fields(
        self, element: Element
    ) -> Iterator[RepositoryField[Element, ElementWithId]]:
        for field in self._unique_fields:
            if self._field_is_duplicate(element, field):
                yield field

    @property
    def _next_id(self) -> int:
        return len(self._elements) + 1

    def add(self, element: Element) -> ElementWithId:
        for field in self._conflicting_fields(element):
            raise ConflictError(field.name)
        element_with_id = self._put_id(element, self._next_id)
        self._elements.append(element_with_id)
        return element_with_id

    def id_exists(self, element_id: int) -> bool:
        return any(self._get_id(element) == element_id for element in self._elements)

    def get_by_id(self, element_id: int) -> Optional[ElementWithId]:
        return next(
            (e for e in self._elements if self._get_id(e) == element_id),
            None,
        )

    def delete(self, element_id: int) -> None:
        self._elements = [
            element for element in self._elements if self._get_id(element) != element_id
        ]

    def update(self, element_id: int, element: Element) -> ElementWithId:
        for field in self._conflicting_fields(element):
            if self._field_changed(element_id, element, field):
                raise ConflictError(field.name)
        updated = self._put_id(element, element_id)
        self._elements = [updated if e.id == element_id else e for e in self._elements]
        return updated

    def get_filtered(
        self, pagination: PaginationParameters, filters: Filters
    ) -> RepositoryPaginatedResponse[ElementWithId]:
        filtered = [e for e in self._elements if self._matches(e, filters)]
        start_idx = pagination.offset
        end_idx = start_idx + pagination.limit
        return RepositoryPaginatedResponse[ElementWithId](
            elements=filtered[start_idx:end_idx], total=len(filtered)
        )
