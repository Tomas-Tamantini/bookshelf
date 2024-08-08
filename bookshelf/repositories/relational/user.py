from typing import Optional

from sqlalchemy.orm import Query

from bookshelf.domain.user import User, UserCore
from bookshelf.repositories.dto import UserFilters
from bookshelf.repositories.relational.relational_repository import RelationalRepository
from bookshelf.repositories.relational.tables import UserDB


class RelationalUserRepository(
    RelationalRepository[UserCore, User, UserDB, UserFilters]
):
    @staticmethod
    def _db_to_domain(db_element: UserDB) -> User:
        return User(
            id=db_element.id,
            username=db_element.username,
            email=db_element.email,
            hashed_password=db_element.hashed_password,
        )

    @staticmethod
    def _domain_to_db(domain_element: UserCore) -> UserDB:
        return UserDB(**domain_element.model_dump())

    @staticmethod
    def _db_class() -> UserDB:
        return UserDB

    def _apply_filters(self, query: Query, filters: UserFilters) -> Query:
        if filters.username:
            query = query.where(UserDB.username.contains(filters.username))
        if filters.email:
            query = query.where(UserDB.email.contains(filters.email))
        return query

    def get_by_email(self, email: str) -> Optional[User]:
        user_db = self._query_table().filter_by(email=email).one_or_none()
        return self._db_to_domain(user_db) if user_db else None
