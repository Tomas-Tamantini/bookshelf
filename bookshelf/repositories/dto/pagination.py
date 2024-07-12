from dataclasses import dataclass


@dataclass(frozen=True)
class RepositoryPaginatedResponse[T]:
    elements: list[T]
    total: int
