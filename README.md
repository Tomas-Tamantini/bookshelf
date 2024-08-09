# bookshelf

An API to manage your favorite books. This is the final project for the awesome [FastAPI do Zero](https://fastapidozero.dunossauro.com/) course (see the project requirements [here](https://fastapidozero.dunossauro.com/14/#o-projeto)).

See the frontend application [here](https://github.com/Tomas-Tamantini/bookshelf-frontend).

## How to run the project

### Requirements

- [Python](https://www.python.org/) ^3.12

### With poetry

1. Install the dependencies:

```bash
poetry install
```

2. Run the application:

```bash
task run
```

3. Run the tests:

```bash
task test
```

## Main tools used in development

- [Python 3.12](https://www.python.org/) as the programming language.
- [Poetry](https://python-poetry.org/) to manage the dependencies.
- [FastAPI](https://fastapi.tiangolo.com/) to implement the endpoints.
- [SQLAlchemy](https://www.sqlalchemy.org/) to manage the database.
- [Pydantic](https://pydantic-docs.helpmanual.io/) to validate and convert the Data-Transfer-Objects and database models.
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) to manage the database migrations.
- [PostgreSQL](https://www.postgresql.org/) as the database.
- [Docker](https://www.docker.com/) to containerize the application.
- [Docker Compose](https://docs.docker.com/compose/) to manage the containers.
