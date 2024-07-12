from typing import Optional, Protocol, TypeVar

from bookshelf.repositories.dto import PaginationParameters, RepositoryPaginatedResponse

Element = TypeVar("Element")
ElementWithId = TypeVar("ElementWithId")
Filters = TypeVar("Filters")


class Repository(Protocol[Element, ElementWithId, Filters]):
    def add(self, element: Element) -> ElementWithId: ...

    def id_exists(self, element_id: int) -> bool: ...

    def delete(self, element_id: int) -> None: ...

    def update(self, element_id: int, element: Element) -> ElementWithId: ...

    def get_by_id(self, element_id: int) -> Optional[ElementWithId]: ...

    def get_filtered(
        self, pagination: PaginationParameters, filters: Filters
    ) -> RepositoryPaginatedResponse[ElementWithId]: ...
