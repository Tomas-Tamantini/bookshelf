from bookshelf.domain.author import AuthorCore
from bookshelf.api.dto.sanitize import sanitize_name


class CreateAuthorRequest(AuthorCore):
    def sanitized(self) -> AuthorCore:
        return AuthorCore(name=sanitize_name(self.name))
