from bookshelf.api.dto.sanitize import sanitize_name
from bookshelf.domain.author import AuthorCore


class CreateAuthorRequest(AuthorCore):
    def sanitized(self) -> AuthorCore:
        return AuthorCore(name=sanitize_name(self.name))
