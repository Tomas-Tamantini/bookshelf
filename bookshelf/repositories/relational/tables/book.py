from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from bookshelf.repositories.relational.tables.table_registry import table_registry


@table_registry.mapped_as_dataclass
class BookDB:
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    year: Mapped[int] = mapped_column()
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
