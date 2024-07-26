from fastapi import FastAPI

from bookshelf.api.routers import set_all_routes

app = FastAPI()
set_all_routes(app)
