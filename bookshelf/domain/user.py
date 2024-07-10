from pydantic import BaseModel, ConfigDict, EmailStr


class UserPublicInformation(BaseModel):
    model_config = ConfigDict(frozen=True)

    username: str
    email: EmailStr


class UserCore(UserPublicInformation):
    hashed_password: str


class User(UserCore):
    id: int
