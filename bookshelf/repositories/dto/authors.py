from pydantic import BaseModel


class GetAuthorsDBQueryParameters(BaseModel):
    name: str
    limit: int
    offset: int
