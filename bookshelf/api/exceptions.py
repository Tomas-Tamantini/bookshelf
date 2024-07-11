from http import HTTPStatus

from fastapi import HTTPException


class HttpConflictError(HTTPException):
    def __init__(self, resource_name: str, field: str):
        super().__init__(
            status_code=HTTPStatus.CONFLICT,
            detail=f"{resource_name} with this {field} already exists",
        )
