from fastapi import FastAPI

from bookshelf.api.routers import (
    authors_router,
    books_router,
    healthcheck_router,
    users_router,
)

app = FastAPI()

app.include_router(healthcheck_router)
app.include_router(authors_router)
app.include_router(books_router)
app.include_router(users_router)
