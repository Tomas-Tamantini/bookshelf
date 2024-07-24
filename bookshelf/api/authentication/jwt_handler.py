from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Protocol
from zoneinfo import ZoneInfo

from jwt import (
    DecodeError,
    ExpiredSignatureError,
    ImmatureSignatureError,
    decode,
    encode,
)

from bookshelf.api.exceptions import BadTokenError


@dataclass(frozen=True)
class Token:
    access_token: str
    token_type: str


@dataclass(frozen=True)
class TokenPair(Token):
    refresh_token: str


class JWTHandler(Protocol):
    def create_access_token(self, subject: str) -> Token: ...

    def create_token_pair(self, subject: str) -> TokenPair: ...

    def get_subject(self, token: str) -> str: ...


class PyJWTHandler:
    def __init__(
        self,
        secret: str,
        algorithm: str,
        access_token_expiration_minutes: int,
        refresh_token_expiration_minutes: int,
    ) -> None:
        self._secret = secret
        self._algorithm = algorithm
        self._access_token_expiration_minutes = access_token_expiration_minutes
        self._refresh_token_expiration_minutes = refresh_token_expiration_minutes

    def _expiration(self, duration_minutes: int) -> datetime:
        return datetime.now(tz=ZoneInfo("UTC")) + timedelta(minutes=duration_minutes)

    def _build_token(
        self,
        subject: str,
        expiration_minutes: int,
        not_before_minutes: Optional[int] = None,
    ) -> str:
        payload = {"sub": subject, "exp": self._expiration(expiration_minutes)}
        if not_before_minutes:
            payload["nbf"] = self._expiration(not_before_minutes)
        return encode(payload, self._secret, algorithm=self._algorithm)

    def create_access_token(self, subject: str) -> Token:
        access_token = self._build_token(
            subject, expiration_minutes=self._access_token_expiration_minutes
        )
        return Token(access_token=access_token, token_type="bearer")

    def create_token_pair(self, subject: str) -> TokenPair:
        refresh_token = self._build_token(
            subject,
            expiration_minutes=self._access_token_expiration_minutes
            + self._refresh_token_expiration_minutes,
            not_before_minutes=self._access_token_expiration_minutes,
        )
        token = self.create_access_token(subject)
        return TokenPair(
            access_token=token.access_token,
            refresh_token=refresh_token,
            token_type=token.token_type,
        )

    def get_subject(self, token: str) -> str:
        try:
            return decode(token, self._secret, algorithms=[self._algorithm])["sub"]
        except ExpiredSignatureError:
            raise BadTokenError("Token has expired")
        except ImmatureSignatureError:
            raise BadTokenError("Token is not yet valid")
        except DecodeError:
            raise BadTokenError("Token is invalid")
