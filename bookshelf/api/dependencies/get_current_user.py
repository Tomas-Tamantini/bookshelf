from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from bookshelf.api.authentication import BadTokenError
from bookshelf.api.dependencies.get_authentication_services import T_JWTHandler
from bookshelf.api.dependencies.get_repositories import T_UserRepository
from bookshelf.api.exceptions import CredentialsError
from bookshelf.domain.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_current_user(
    jwt_handler: T_JWTHandler,
    user_repository: T_UserRepository,
    token: str = Depends(oauth2_scheme),
) -> User:
    try:
        user_email = jwt_handler.get_subject(token)
    except BadTokenError:
        raise CredentialsError()
    user = user_repository.get_by_email(user_email)
    if user is None:
        raise CredentialsError()
    else:
        return user


T_CurrentUser = Annotated[User, Depends(get_current_user)]
