from sqlalchemy.orm import Query

from bookshelf.domain.author import Author, AuthorCore
from bookshelf.repositories.dto import AuthorFilters
from bookshelf.repositories.relational.relational_repository import RelationalRepository
from bookshelf.repositories.relational.tables import AuthorDB


class RelationalAuthorRepository(
    RelationalRepository[AuthorCore, Author, AuthorDB, AuthorFilters]
):
    @staticmethod
    def _db_to_domain(db_element: AuthorDB) -> Author:
        return Author(id=db_element.id, name=db_element.name)

    @staticmethod
    def _domain_to_db(domain_element: AuthorCore) -> AuthorDB:
        return AuthorDB(**domain_element.model_dump())

    @staticmethod
    def _db_class() -> AuthorDB:
        return AuthorDB

    def _apply_filters(self, query: Query, filters: AuthorFilters) -> Query:
        if filters.name:
            query = query.where(AuthorDB.name.contains(filters.name))
        return query
