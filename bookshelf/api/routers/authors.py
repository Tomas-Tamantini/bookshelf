from http import HTTPStatus

from fastapi import APIRouter

authors_router = APIRouter(prefix="/authors", tags=["authors"])


@authors_router.post("/", status_code=HTTPStatus.OK.value)
def create_author():
    return {}
