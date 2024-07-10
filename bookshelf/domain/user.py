from pydantic import BaseModel, ConfigDict


class UserPublicInformation(BaseModel):
    model_config = ConfigDict(frozen=True)

    username: str
    email: str


class UserCore(UserPublicInformation):
    password: str
