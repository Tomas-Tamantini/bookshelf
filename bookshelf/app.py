from fastapi import FastAPI

from bookshelf.api.routers import authors_router, healthcheck_router

app = FastAPI()

app.include_router(healthcheck_router)
app.include_router(authors_router)
