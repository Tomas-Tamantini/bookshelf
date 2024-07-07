from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import Response

app = FastAPI()


@app.get("/health")
def health_check():
    return Response(status_code=HTTPStatus.NO_CONTENT)
