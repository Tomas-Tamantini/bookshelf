from fastapi import FastAPI

from bookshelf.api.routers import healthcheck_router

app = FastAPI()

app.include_router(healthcheck_router)
