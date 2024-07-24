from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from bookshelf.api.authentication import BadTokenError, Token, TokenPair
from bookshelf.api.dependencies import T_JWTHandler, T_PasswordHandler, T_UserRepository
from bookshelf.api.dto import RefreshTokenRequest

authentication_router = APIRouter(prefix="/auth", tags=["auth"])


@authentication_router.post("/login", response_model=TokenPair)
def login(
    user_repository: T_UserRepository,
    password_handler: T_PasswordHandler,
    jwt_handler: T_JWTHandler,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = user_repository.get_by_email(form_data.username)
    if user is None or not password_handler.verify(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    else:
        return jwt_handler.create_token_pair(user.id)


@authentication_router.post("/refresh", response_model=Token)
def refresh(request: RefreshTokenRequest, jwt_handler: T_JWTHandler):
    try:
        subject = jwt_handler.get_subject(request.refresh_token)
    except BadTokenError as e:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=str(e),
        )
    else:
        return jwt_handler.create_access_token(subject)
