from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Query, Session

from bookshelf.repositories.dto import PaginationParameters, RepositoryPaginatedResponse
from bookshelf.repositories.exceptions import ConflictError


class RelationalRepository[Element, ElementWithId, ElementDB, Filters](ABC):
    def __init__(self, session: Session) -> None:
        self._session = session

    @abstractmethod
    def _db_to_domain(db_element: ElementDB) -> ElementWithId:
        raise NotImplementedError("Abstract method")

    @abstractmethod
    def _domain_to_db(domain_element: Element) -> ElementDB:
        raise NotImplementedError("Abstract method")

    @abstractmethod
    def _db_class(self) -> ElementDB:
        raise NotImplementedError("Abstract method")

    @abstractmethod
    def _apply_filters(self, query, filters: Filters):
        raise NotImplementedError("Abstract method")

    def _query_table(self) -> Query:
        return self._session.query(self._db_class())

    def _is_using_sqlite(self) -> bool:
        return "sqlite" in self._session.get_bind().dialect.name

    def _raise_conflict_error(self, e: IntegrityError) -> None:
        if self._is_using_sqlite():
            field = str(e.orig).split(".")[-1].strip()
        else:
            field = str(e.orig).split("(")[1].split(")")[0].strip()
        raise ConflictError(field)

    def add(self, element: Element) -> ElementWithId:
        element_db = self._domain_to_db(element)
        self._session.add(element_db)
        try:
            self._session.commit()
            self._session.refresh(element_db)
            return self._db_to_domain(element_db)
        except IntegrityError as e:
            self._session.rollback()
            self._raise_conflict_error(e)

    def id_exists(self, id: int) -> bool:
        return self._query_table().filter_by(id=id).count() > 0

    def delete(self, element_id: int) -> None:
        self._query_table().filter_by(id=element_id).delete()
        self._session.commit()

    def get_by_id(self, element_id: int) -> Optional[ElementWithId]:
        element_db = self._query_table().filter_by(id=element_id).one_or_none()
        return self._db_to_domain(element_db) if element_db else None

    def get_filtered(
        self, pagination: PaginationParameters, filters: Filters
    ) -> RepositoryPaginatedResponse[ElementWithId]:
        query = self._query_table()
        query = self._apply_filters(query, filters)
        total = query.count()
        query = query.limit(pagination.limit).offset(pagination.offset)
        elements = [self._db_to_domain(element) for element in query.all()]
        return RepositoryPaginatedResponse(elements, total=total)

    def update(self, element_id: int, element: Element) -> ElementWithId:
        try:
            self._query_table().filter(self._db_class().id == element_id).update(
                element.model_dump()
            )
            self._session.commit()
            element_db = self._query_table().filter_by(id=element_id).one()
            return self._db_to_domain(element_db)
        except IntegrityError as e:
            self._session.rollback()
            self._raise_conflict_error(e)
