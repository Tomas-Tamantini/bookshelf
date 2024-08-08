from sqlalchemy.orm import Query

from bookshelf.domain.book import Book, BookCore
from bookshelf.repositories.dto import BookFilters
from bookshelf.repositories.relational.relational_repository import RelationalRepository
from bookshelf.repositories.relational.tables import BookDB


class RelationalBookRepository(
    RelationalRepository[BookCore, Book, BookDB, BookFilters]
):
    @staticmethod
    def _db_to_domain(db_element: BookDB) -> Book:
        return Book(
            id=db_element.id,
            year=db_element.year,
            title=db_element.title,
            author_id=db_element.author_id,
        )

    @staticmethod
    def _domain_to_db(domain_element: BookCore) -> BookDB:
        return BookDB(**domain_element.model_dump())

    @staticmethod
    def _db_class() -> BookDB:
        return BookDB

    def _apply_filters(self, query: Query, filters: BookFilters) -> Query:
        if filters.title:
            query = query.where(BookDB.title.contains(filters.title))
        if filters.year:
            query = query.where(BookDB.year == filters.year)
        if filters.author_id:
            query = query.where(BookDB.author_id == filters.author_id)
        return query
