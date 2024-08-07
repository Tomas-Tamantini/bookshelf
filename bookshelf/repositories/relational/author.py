from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from bookshelf.domain.author import Author, AuthorCore
from bookshelf.repositories.dto import (
    AuthorFilters,
    PaginationParameters,
    RepositoryPaginatedResponse,
)
from bookshelf.repositories.exceptions import ConflictError
from bookshelf.repositories.relational.tables import AuthorDB


class RelationalAuthorRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    @staticmethod
    def _db_to_domain(db_element: AuthorDB) -> Author:
        return Author(id=db_element.id, name=db_element.name)

    @staticmethod
    def _raise_conflict_error(e: IntegrityError) -> None:
        field = str(e.orig).split(".")[-1].strip()
        raise ConflictError(field)

    def add(self, element: AuthorCore) -> Author:
        author_db = AuthorDB(**element.model_dump())
        self._session.add(author_db)
        try:
            self._session.commit()
            self._session.refresh(author_db)
            return self._db_to_domain(author_db)
        except IntegrityError as e:
            self._session.rollback()
            self._raise_conflict_error(e)

    def id_exists(self, id: int) -> bool:
        return self._session.query(AuthorDB).filter_by(id=id).count() > 0

    def delete(self, element_id: int) -> None:
        self._session.query(AuthorDB).filter_by(id=element_id).delete()
        self._session.commit()

    def update(self, element_id: int, element: AuthorCore) -> Author:
        author_db = self._session.query(AuthorDB).filter_by(id=element_id).one()
        author_db.name = element.name
        try:
            self._session.commit()
            return self._db_to_domain(author_db)
        except IntegrityError as e:
            self._session.rollback()
            self._raise_conflict_error(e)

    def get_by_id(self, element_id: int) -> Optional[Author]:
        author_db = self._session.query(AuthorDB).filter_by(id=element_id).one_or_none()
        return self._db_to_domain(author_db) if author_db else None

    def get_filtered(
        self, pagination: PaginationParameters, filters: AuthorFilters
    ) -> RepositoryPaginatedResponse[Author]:
        query = self._session.query(AuthorDB)
        if filters.name:
            query = query.where(AuthorDB.name.contains(filters.name))
        total = query.count()
        query = query.limit(pagination.limit).offset(pagination.offset)
        authors = [self._db_to_domain(author) for author in query.all()]
        return RepositoryPaginatedResponse(elements=authors, total=total)
