import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from bookshelf.repositories.relational.tables import table_registry


@pytest.fixture(scope="session")
def db_engine():
    return create_engine("sqlite:///:memory:")


@pytest.fixture
def db_session(db_engine):
    table_registry.metadata.create_all(db_engine)
    with Session(db_engine) as session:
        yield session
    table_registry.metadata.drop_all(db_engine)
