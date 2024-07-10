from typing import Protocol


class PasswordHandler(Protocol):
    def hash_password(self, password: str) -> str: ...

    def verify_password(self, plain_password: str, hashed_password: str) -> bool: ...


class PwdHandler:
    def hash_password(self, password: str) -> str:
        raise NotImplementedError()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        raise NotImplementedError()
