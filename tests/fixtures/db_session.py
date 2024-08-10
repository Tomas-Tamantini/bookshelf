import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from bookshelf.repositories.relational.tables import table_registry


@pytest.fixture(scope="session")
def db_engine():
    with PostgresContainer("postgres:16", driver="psycopg") as postgres:
        engine = create_engine(postgres.get_connection_url())
        with engine.begin():
            yield engine


@pytest.fixture
def db_session(db_engine):
    table_registry.metadata.create_all(db_engine)
    with Session(db_engine) as session:
        yield session
    table_registry.metadata.drop_all(db_engine)
