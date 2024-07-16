from freezegun import freeze_time
from jwt import decode

from bookshelf.api.authentication import PyJWTHandler

_DEFAULT_SECRET = "secret"
_DEFAULT_ALGORITHM = "HS256"


def _jwt_handler(
    access_token_expiration_minutes: int = 30,
    refresh_token_expiration_minutes: int = 30,
) -> PyJWTHandler:
    return PyJWTHandler(
        _DEFAULT_SECRET,
        _DEFAULT_ALGORITHM,
        access_token_expiration_minutes,
        refresh_token_expiration_minutes,
    )


def _decode(token: str) -> dict:
    return decode(
        token,
        _DEFAULT_SECRET,
        algorithms=[_DEFAULT_ALGORITHM],
        options={"verify_exp": False, "verify_nbf": False},
    )


def test_jwt_handler_creates_access_token_with_type_bearer():
    token = _jwt_handler().create_access_token("test-subject")
    assert token.token_type == "bearer"


def test_jwt_handler_creates_access_token_with_subject():
    token = _jwt_handler().create_access_token("test-subject")
    decoded = _decode(token.access_token)
    assert decoded["sub"] == "test-subject"


def test_jwt_access_token_expires_x_minutes_after_creation():
    with freeze_time("2021-01-01 00:00:00"):
        token = _jwt_handler(access_token_expiration_minutes=30).create_access_token(
            "test-subject"
        )
        decoded = _decode(token.access_token)
        assert decoded["exp"] == 1609461000


def test_jwt_handler_creates_access_and_refresh_token_with_type_bearer():
    token_pair = _jwt_handler().create_token_pair("test-subject")
    assert token_pair.token_type == "bearer"


def test_jwt_handler_creates_access_and_refresh_token_with_subject():
    token_pair = _jwt_handler().create_token_pair("test-subject")
    decoded_access = _decode(token_pair.access_token)
    decoded_refresh = _decode(token_pair.refresh_token)
    assert decoded_access["sub"] == decoded_refresh["sub"] == "test-subject"


def test_jwt_access_token_has_expiration_timestamp_equal_to_refresh_token_nbf_timestamp():
    with freeze_time("2021-01-01 00:00:00"):
        token_pair = _jwt_handler(access_token_expiration_minutes=30).create_token_pair(
            "test-subject"
        )
        decoded_access = _decode(token_pair.access_token)
        decoded_refresh = _decode(token_pair.refresh_token)
        assert "nbf" not in decoded_access
        assert decoded_access["exp"] == decoded_refresh["nbf"] == 1609461000


def test_jwt_refresh_token_expires_x_minutes_after_access_token():
    with freeze_time("2021-01-01 00:00:00"):
        token_pair = _jwt_handler(
            refresh_token_expiration_minutes=30
        ).create_token_pair("test-subject")
        decoded_refresh = _decode(token_pair.refresh_token)
        assert decoded_refresh["exp"] == 1609462800
