from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from bookshelf.domain.book import Book, BookCore
from bookshelf.repositories.dto import (
    BookFilters,
    PaginationParameters,
    RepositoryPaginatedResponse,
)
from bookshelf.repositories.exceptions import ConflictError
from bookshelf.repositories.relational.tables import BookDB


class RelationalBookRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    @staticmethod
    def _db_to_domain(db_element: BookDB) -> Book:
        return Book(
            id=db_element.id,
            year=db_element.year,
            title=db_element.title,
            author_id=db_element.author_id,
        )

    @staticmethod
    def _raise_conflict_error(e: IntegrityError) -> None:
        field = str(e.orig).split(".")[-1].strip()
        raise ConflictError(field)

    def add(self, element: BookCore) -> Book:
        book_db = BookDB(**element.model_dump())
        self._session.add(book_db)
        try:
            self._session.commit()
            self._session.refresh(book_db)
            return self._db_to_domain(book_db)
        except IntegrityError as e:
            self._session.rollback()
            self._raise_conflict_error(e)

    def id_exists(self, id: int) -> bool:
        return self._session.query(BookDB).filter_by(id=id).count() > 0

    def delete(self, element_id: int) -> None:
        self._session.query(BookDB).filter_by(id=element_id).delete()
        self._session.commit()

    def update(self, element_id: int, element: BookCore) -> Book:
        try:
            self._session.query(BookDB).filter(BookDB.id == element_id).update(
                element.model_dump()
            )
            self._session.commit()
            book_db = self._session.query(BookDB).filter_by(id=element_id).one()
            return self._db_to_domain(book_db)
        except IntegrityError as e:
            self._session.rollback()
            self._raise_conflict_error(e)

    def get_by_id(self, element_id: int) -> Optional[Book]:
        book_db = self._session.query(BookDB).filter_by(id=element_id).one_or_none()
        return self._db_to_domain(book_db) if book_db else None

    def get_filtered(
        self, pagination: PaginationParameters, filters: BookFilters
    ) -> RepositoryPaginatedResponse[Book]:
        query = self._session.query(BookDB)
        if filters.title:
            query = query.where(BookDB.title.contains(filters.title))
        if filters.year:
            query = query.where(BookDB.year == filters.year)
        if filters.author_id:
            query = query.where(BookDB.author_id == filters.author_id)
        total = query.count()
        query = query.limit(pagination.limit).offset(pagination.offset)
        books = [self._db_to_domain(book) for book in query.all()]
        return RepositoryPaginatedResponse(elements=books, total=total)
