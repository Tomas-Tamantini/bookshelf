from fastapi import FastAPI

from bookshelf.api.routers.authors import authors_router
from bookshelf.api.routers.books import books_router
from bookshelf.api.routers.healthcheck import healthcheck_router
from bookshelf.api.routers.users import users_router


def set_all_routes(app: FastAPI) -> None:
    app.include_router(healthcheck_router)
    app.include_router(authors_router)
    app.include_router(books_router)
    app.include_router(users_router)
