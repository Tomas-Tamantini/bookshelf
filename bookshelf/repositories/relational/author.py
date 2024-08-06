from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from bookshelf.domain.author import Author, AuthorCore
from bookshelf.repositories.exceptions import ConflictError
from bookshelf.repositories.relational.tables import AuthorDB


class RelationalAuthorRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, element: AuthorCore) -> Author:
        author_db = AuthorDB(**element.model_dump())
        self._session.add(author_db)
        try:
            self._session.commit()
            self._session.refresh(author_db)
            return Author(id=author_db.id, name=author_db.name)
        except IntegrityError as e:
            self._session.rollback()
            field = str(e.orig).split(".")[-1].strip()
            raise ConflictError(field)

    def id_exists(self, id: int) -> bool:
        return self._session.query(AuthorDB).filter_by(id=id).count() > 0
